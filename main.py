# Import neccessary libraries
import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Annotated
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from datetime import datetime, timedelta, timezone
import time


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


# Database connection
DB_URL = os.getenv("NEON_MAIN_URL")
engine = create_engine(DB_URL)
localSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db= localSession()
    try:
        yield db
    finally:
        db.close()


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)

class CreateUser(BaseModel):
    username: str
    password: str

class taskItem(BaseModel):
    title: str
    description: str
    completed: bool = False

    class ConfigDict:
        from_attributes = True

class TaskDB(Base):
    __tablename__ =  "tasks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    completed = Column(Boolean, default=False)
    owner = Column(String)

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= 'token')
pwd_context = CryptContext(schemes= ['bcrypt'],deprecated = 'auto')


def verify_pw(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_pw(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
    
def authenticate_user(db: Session, username, password):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_pw(password,user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_token

def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
):
    credential_exception = HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except (jwt.PyJWTError,InvalidTokenError):
        raise credential_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    return user

    
app = FastAPI()

@app.middleware('http')
async def log_errors_to_file(request: Request, call_next_function):
    start_time = time.perf_counter()
    response = await call_next_function(request)
    duration = time.perf_counter() - start_time

    status = response.status_code

    if status == 200:
        return response
    elif status == 400:
        log_type = "BAD REQUEST"
    elif status == 401:
        log_type = "UNAUTHORIZED"
    elif status == 403:
        log_type = "FORBIDDEN"
    elif status == 404:
        log_type = "NOT FOUND"
    elif status >= 500:
        log_type = "SERVER ERROR"
    else:
        log_type = "OTHER ERROR"

    log_entry = (
        f"({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
        f"{request.client.host} - {request.method} {request.url.path}"
        f"{status} ({log_type}) ({duration:.4f}s)\n"
    )

    try:
        with open('log.txt', 'a') as logfile:
            logfile.write(log_entry)
    except Exception as e:
        print(f"Logging error: {e}")

    return response

#User registration

@app.post('/register')
def register_user(
    user: CreateUser,
    db: Annotated[Session, Depends(get_db)]
):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code= 400,
            detail= f"User with this username: {user.username} is already exist!"
        )
    hashed_password = hash_pw(user.password)
    db_user = User(username = user.username, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'message': f"User with username: {user.username} was created! Registration completed!"}

@app.post('/token')
def login_to_get_access_token(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
) -> Token:
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {'sub':user.username}, expires_delta=access_token_expire)
    return Token(access_token=access_token, token_type= 'bearer')

@app.post('/tasks/', response_model=taskItem)
def create_task(
    task: taskItem,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    db_task = TaskDB(title = task.title, description = task.description, completed = task.completed, owner = current_user.username)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get('/tasks', response_model=List[taskItem])
def get_all_task(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    return db.query(TaskDB).filter(TaskDB.owner == current_user.username).all()

@app.get('/tasks/{task_id}', response_model= taskItem)
def get_task(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.owner == current_user.username).first()
    if not db_task:
        raise HTTPException(
            status_code= 404,
            detail= f"Task with this ID: {task_id} cannot be found!"
        )
    return db_task

@app.put('/tasks/{task_id}',response_model= taskItem)
def update_task(
    task_id: int,
    updated_task: taskItem,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.owner == current_user.username).first()
    if not db_task:
        raise HTTPException(
            status_code= 404,
            detail= f"Task with this ID: {task_id} cannot be found!"
        )
    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.completed = updated_task.completed
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete('/tasks/{task_id}')
def delete_task(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id, TaskDB.owner == current_user.username).first()
    if not db_task:
        raise HTTPException(
            status_code= 404,
            detail= f"Task with this ID: {task_id} cannot be found!"
        )
    db.delete(db_task)
    db.commit()
    return {"message": f"Task with this ID: {task_id} was deleted!"}
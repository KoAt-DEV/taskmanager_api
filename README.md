# Task Manager API

A secure REST API for task management built with FastAPI, featuring JWT authentication, Neon PostgreSQL database, Docker containerization, and automated CI/CD pipeline with deployment to Render.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Task Management**: Full CRUD operations for tasks
- **User Isolation**: Users can only access their own tasks
- **Error Logging**: Custom middleware for logging errors and request monitoring
- **Secure**: Password hashing with bcrypt, environment variable configuration
- **Cloud Database**: Neon PostgreSQL integration with SQLAlchemy ORM
- **Containerized**: Docker support for easy deployment and development
- **Testing**: Comprehensive test suite with pytest and separate test database
- **CI/CD**: Automated testing with GitHub Actions
- **Production Ready**: Deployed on Render with automated deployments

## Tech Stack

- **Backend**: FastAPI
- **Database**: Neon PostgreSQL (Cloud)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt via passlib
- **Containerization**: Docker
- **Testing**: pytest, TestClient
- **Environment Management**: python-dotenv
- **Logging**: Custom middleware for error tracking and performance monitoring
- **CI/CD**: GitHub Actions for automated testing
- **Deployment**: Render

## Project Structure

```
task-manager/
├── main.py              # Main application file with API endpoints

├── test.py              # Comprehensive test suite

├── requirements.txt     # Python dependencies

├── Dockerfile           # Docker configuration

├── .env                 # Environment variables (not included in repo)

├── .github/

│   └── workflows/

│           └── ci.yml       # GitHub Actions CI pipeline
└── README.md            # This file
```

## Installation & Setup

### Option 1: Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <https://github.com/KoAt-DEV/taskmanager_api>
   cd task-manager
   ```

2. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   NEON_MAIN_URL=your_neon_main_database_connection_string
   NEON_TEST_URL=your_neon_test_database_connection_string
   SECRET_KEY=your_super_secret_jwt_key
   ```

3. **Build and run with Docker**
   ```bash
   # Build the Docker image
   docker build -t task-manager .
   
   # Run the container
   docker run -p 8000:8000 --env-file .env task-manager
   ```

### Option 2: Local Development

1. **Clone the repository**
   ```bash
   git clone <https://github.com/KoAt-DEV/taskmanager_api>
   cd task-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (same as above)

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## Database Setup

### Neon PostgreSQL

This project uses [Neon](https://neon.tech/) as the cloud PostgreSQL database provider.

1. **Create a Neon account** at [neon.tech](https://neon.tech/)
2. **Create two databases**:
   - Main database for the application
   - Test database for running tests
3. **Get connection strings** from your Neon dashboard
4. **Add to environment variables** as `NEON_MAIN_URL` and `NEON_TEST_URL`

## Usage

### Live Demo

🚀 **The API is deployed and running at**: [https://taskmanager-api-tgu8.onrender.com]

### Local Development

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints

#### Authentication
- `POST /register` - Register a new user
- `POST /token` - Login and get access token

#### Tasks
- `POST /tasks/` - Create a new task
- `GET /tasks` - Get all tasks for authenticated user
- `GET /tasks/{task_id}` - Get specific task by ID
- `PUT /tasks/{task_id}` - Update a task
- `DELETE /tasks/{task_id}` - Delete a task

## Testing

### Local Testing

#### With Docker
```bash
# Run tests in Docker container
docker run --env-file .env task-manager pytest test.py -v
```

#### Without Docker
```bash
# Run tests locally
pytest test.py -v
```

### Continuous Integration

This project uses GitHub Actions for automated testing. The CI pipeline:

- **Triggers**: Runs on pushes to main branch and all pull requests
- **Environment**: Ubuntu latest with Python 3.11
- **Database**: Neon PostgreSQL for testing
- **Tests**: Automatically runs the full pytest suite

#### CI Pipeline Features

- **Automated Testing**: Every push and pull request triggers the test suite
- **Cloud Database Integration**: Uses Neon PostgreSQL for realistic testing
- **Environment Isolation**: Tests run in clean, isolated environment
- **Dependency Management**: Automatically installs all required dependencies

#### CI Configuration

The pipeline requires the following GitHub repository secrets:
- `NEON_MAIN_URL`: Main database connection string
- `NEON_TEST_URL`: Test database connection string
- `SECRET_KEY`: JWT secret key for testing

### Test Coverage

The test suite covers:
- User registration and authentication
- Task creation, retrieval, updating, and deletion
- User isolation (users cannot access other users' tasks)
- Error handling for non-existent resources
- Invalid authentication attempts

## Deployment

### Render Deployment

This application is deployed on [Render](https://render.com/) with automatic deployments.

#### Deployment Features
- **Automatic Deployments**: Deploys automatically on pushes to main branch
- **Docker Support**: Uses the provided Dockerfile for containerization
- **Environment Variables**: Configured through Render's dashboard
- **Health Checks**: Automatic health monitoring
- **HTTPS**: Secure HTTPS endpoints

#### Environment Variables on Render
Set these environment variables in your Render service:
- `NEON_MAIN_URL`: Your Neon main database connection string
- `SECRET_KEY`: Your JWT secret key

## Docker Configuration

### Dockerfile Details
- **Base Image**: Python 3.11 slim
- **Port**: Exposes port 8000
- **Command**: Runs uvicorn with host 0.0.0.0 for containerization
- **Dependencies**: Automatically installs from requirements.txt

### Docker Commands
```bash
# Build image
docker build -t task-manager .

# Run container
docker run -p 8000:8000 --env-file .env task-manager

# Run with custom port
docker run -p 3000:8000 --env-file .env task-manager
```

## Logging & Monitoring

The application includes comprehensive request logging and error tracking:

### Error Logging Features
- **Automatic Error Logging**: All non-200 HTTP responses are logged to log.txt
- **Performance Monitoring**: Request duration tracking for all endpoints
- **Detailed Log Format**: Timestamp, client IP, HTTP method, path, status code, and response time
- **Error Categorization**: Clear classification of error types (BAD REQUEST, UNAUTHORIZED, NOT FOUND, etc.)

### Log File Format (example):
```
(2024-12-28 15:30:45) 127.0.0.1 - POST /tasks/999 404 (NOT FOUND) (0.0234s)
(2024-12-28 15:31:12) 192.168.1.100 - GET /tasks 401 (UNAUTHORIZED) (0.0156s)
```

### Monitoring Benefits
- **Debugging**: Easily identify failed requests and their causes
- **Performance Analysis**: Track slow endpoints and optimize accordingly
- **Security Monitoring**: Monitor unauthorized access attempts
- **Usage Analytics**: Understand API usage patterns

*Note: The log.txt file is automatically created when the first error occurs. Consider adding it to your .gitignore for production deployments.*

## Database Schema

### Users Table
- `id`: Primary key (Integer)
- `username`: Unique username (String)
- `hashed_password`: Bcrypt hashed password (String)

### Tasks Table
- `id`: Primary key (Integer)
- `title`: Task title (String)
- `description`: Task description (String)
- `completed`: Task completion status (Boolean)
- `owner`: Username of task owner (String)

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **JWT Tokens**: Secure token-based authentication with 30-minute expiration
- **User Isolation**: Users can only access their own tasks
- **Environment Variables**: Sensitive data stored in environment variables
- **Request Logging**: All errors and performance metrics logged for monitoring
- **Cloud Database**: Secure connection to Neon PostgreSQL with SSL

## Environment Variables

### Required Variables
```env
NEON_MAIN_URL=postgresql://username:password@host/database
NEON_TEST_URL=postgresql://username:password@host/test_database
SECRET_KEY=your_super_secret_jwt_key_here
```

### Getting Neon Connection Strings
1. Log in to your [Neon Console](https://console.neon.tech/)
2. Select your project
3. Go to the "Connection Details" section
4. Copy the connection string
5. Create separate databases for main and test environments

## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

### Common Issues

- **Database Connection Error**: Ensure your Neon connection strings are correct and databases are active
- **JWT Token Invalid**: Check if token has expired (30-minute lifetime)
- **Docker Build Fails**: Make sure Docker is installed and running
- **Import Errors**: Make sure all dependencies are installed (`pip install -r requirements.txt`)
- **CI Failures**: Check that all required repository secrets are configured correctly

### Environment Setup

- Make sure your `.env` file is properly configured and not committed to version control
- Add `.env` to your `.gitignore` file
- For CI/CD, ensure all required secrets are added to your GitHub repository settings
- For Render deployment, configure environment variables in the Render dashboard

### Docker Issues

- **Port conflicts**: Change the host port if 8000 is already in use: `docker run -p 3000:8000 --env-file .env task-manager`
- **Permission errors**: Make sure Docker has proper permissions
- **Build cache issues**: Use `docker build --no-cache -t task-manager .` to rebuild from scratch
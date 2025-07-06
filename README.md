# Task Manager API

A secure REST API for task management built with FastAPI, featuring JWT authentication, PostgreSQL database integration, comprehensive testing, and automated CI/CD pipeline.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Task Management**: Full CRUD operations for tasks
- **User Isolation**: Users can only access their own tasks
- **Error Logging**: Custom middleware for logging errors and request monitoring
- **Secure**: Password hashing with bcrypt, environment variable configuration
- **Database**: PostgreSQL integration with SQLAlchemy ORM
- **Testing**: Comprehensive test suite with pytest and separate test database
- **CI/CD**: Automated testing with GitHub Actions

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt via passlib
- **Testing**: pytest, TestClient
- **Environment Management**: python-dotenv
- **Logging**: Custom middleware for error tracking and performance monitoring
- **CI/CD**: GitHub Actions for automated testing

## Project Structure

task-manager/
├── main.py          # Main application file with API endpoints
├── test.py          # Comprehensive test suite
├── requirements.txt # Python dependencies
├── .env             # Environment variables (not included in repo)
├── .github/
│   └── workflows/
│       └── ci.yml   # GitHub Actions CI pipeline
└── README.md        # This file

## Installation

1. **Clone the repository**
   ```bash
   git clone <https://github.com/KoAt-DEV/task_manager_api>
   cd task-manager
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL databases**
   - Create a main database for the application
   - Create a separate test database for running tests

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DB_USERNAME=your_db_username
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=your_main_database_name
   TEST_DB_NAME=your_test_database_name
   SECRET_KEY=your_super_secret_jwt_key
   ```

## Usage

### Starting the Server

```bash
uvicorn main:app --reload
```

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

Run the test suite locally:

```bash
pytest test.py -v
```

### Continuous Integration

This project uses GitHub Actions for automated testing. The CI pipeline:

- **Triggers**: Runs on pushes to main branch and all pull requests
- **Environment**: Ubuntu latest with Python 3.11
- **Database**: PostgreSQL 13 service container for testing
- **Tests**: Automatically runs the full pytest suite

#### CI Pipeline Features

- **Automated Testing**: Every push and pull request triggers the test suite
- **PostgreSQL Integration**: Uses PostgreSQL service container for realistic testing
- **Environment Isolation**: Tests run in clean, isolated environment
- **Dependency Management**: Automatically installs all required dependencies
- **Health Checks**: PostgreSQL service includes health checks to ensure database readiness

#### CI Configuration

The pipeline requires the following GitHub repository secrets:
- `TEST_DB_USER`: PostgreSQL username for testing
- `TEST_DB_PASSWORD`: PostgreSQL password for testing  
- `TEST_DB_NAME`: Test database name
- `TEST_DB_HOST`: Database host (typically localhost in CI)
- `TEST_DB_PORT`: Database port (typically 5432)
- `SECRET_KEY`: JWT secret key for testing

### Test Coverage

The test suite covers:
- User registration and authentication
- Task creation, retrieval, updating, and deletion
- User isolation (users cannot access other users' tasks)
- Error handling for non-existent resources
- Invalid authentication attempts

### Logging & Monitoring

The application includes comprehensive request logging and error tracking:

Error Logging Features
- Automatic Error Logging: All non-200 HTTP responses are logged to log.txt
- Performance Monitoring: Request duration tracking for all endpoints
- Detailed Log Format: Timestamp, client IP, HTTP method, path, status code, and response time
- Error Categorization: Clear classification of error types (BAD REQUEST, UNAUTHORIZED, NOT FOUND, etc.)

Log File Format(example):
(2024-12-28 15:30:45) 127.0.0.1 - POST /tasks/999 404 (NOT FOUND) (0.0234s)
(2024-12-28 15:31:12) 192.168.1.100 - GET /tasks 401 (UNAUTHORIZED) (0.0156s)

Monitoring Benefits:

- Debugging: Easily identify failed requests and their causes
- Performance Analysis: Track slow endpoints and optimize accordingly
- Security Monitoring: Monitor unauthorized access attempts
- Usage Analytics: Understand API usage patterns

Note: The log.txt file is automatically created when the first error occurs. Consider adding it to your .gitignore for production deployments.

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


## License

This project is open source and available under the [MIT License](LICENSE).

## Troubleshooting

### Common Issues

- **Database Connection Error**: Ensure PostgreSQL is running and credentials in `.env` are correct
- **JWT Token Invalid**: Check if token has expired (30-minute lifetime)
- **Import Errors**: Make sure all dependencies are installed
- **CI Failures**: Check that all required repository secrets are configured correctly

### Environment Setup

Make sure your `.env` file is properly configured and not committed to version control. Add `.env` to your `.gitignore` file.

For CI/CD, ensure all required secrets are added to your GitHub repository settings.
## Future Enhancements

# Tender and Quotation Assessment System

## Abstract

The Tender and Quotation Assessment System is developed using Python and FastAPI to simplify and automate the tendering and quotation management process. The system provides a centralized platform for admin to create, publish, and manage tenders, while registered vendors can view available tenders and submit their quotations within the specified deadlines.

It maintains structured records of users, vendors, tenders, quotations, and evaluations using PostgreSQL and SQLAlchemy ORM. The system incorporates JWT-based authentication and role-based authorization to ensure secure access to functionalities. Alembic is used for database schema migration, while logging and middleware provide request monitoring and error tracking.


The application also includes automated testing using Pytest to validate business logic, database operations, and API endpoints.

## Main Features 

- User registration and login.
- JWT-based authentication with access and refresh tokens.
- Role-based access for administrators and vendors.
- Vendor registration as user with company profile details.
- Tender creation and management.
- Tender search, filtering and pagination.
- Quotation submission by registered vendors.
- PDF document upload with file validation.
- Quotation evaluation based on eligibility and vendor details.
- Evaluation decisions: approve, reject and pending.
- Tender sanction management.
- Sanctioned quotation and tender details retrieval.
- Report generation for tender and quotation information.
- Email notification send to admin on quotation submission and to winning mail send to vendor on successful sanction.
- Custom exception handling.
- Request logging and monitoring.
- Request ID and processing-time tracking.
- Database health check.
- Unit, integration and API testing using Pytest.


## Folder Structure

```text
 Tender and Quotation Assessment System
├
│   
|    
├───alembic
│   ├───versions
|   ├── env.py
│   └── script.py.mako
|
|
├───app
│   ├───api
│   │   ├───dependencies/
|   |   |   ├───auth_dependency.py
│   │   │   ├───database.py
│   │   │   ├───service_dependencies.py
│   │   │  
│   │   └───routers/
|   |       ├─── auth_router.py
│   │       ├─── evaluation_router.py
│   │       ├─── health_router.py
│   │       ├─── quotation_router.py
│   │       ├─── report_router.py
│   │       ├─── sanction_router.py
│   │       ├─── tender_router.py
│   │     
│   ├───core/
│   |   ├─── config.py
│   │   ├─── logging_config.py
│   │   ├─── security.py  
│   │   ├───exceptions
│   │       ├─── exception.py
│   │       ├─── exception_handler.py
│   │    
│   │   
│   ├───database/
│   │   ├─── base.py
│   │   ├─── database.py
│   │ 
│   ├───middleware/
|   |   ├─── observability.py
│   │   
│   ├───models/
│   │   ├── evaluation_model.py
│   │   ├── quotation_model.py
│   │   ├── refresh_token_model.py
│   │   ├── sanction_model.py
│   │   ├── tender_model.py
│   │   ├── user_model.py
│   │   ├── vendor_model.py
│   │   
│   ├───repositories
│   │   ├───implementations/
|   |   |   evaluation_repository.py
│   │   │   ├─── quotation_repository.py
│   │   │   ├─── report_repository.py
│   │   │   ├─── sanction_repository.py
│   │   │   ├─── tender_repository.py
│   │   │   ├─── user_repository.py
│   │   │  
│   │   └───interfaces/
│   │       ├─── evaluation_repository_interface.py
│   │       ├─── quotation_repository_interface.py
│   │       ├─── report_repository_interface.py
│   │       ├─── sanction_repository_interface.py
│   │       ├─── tender_repository_interface.py
│   │       ├─── user_interface.py
│   │       
│   ├───schemas/
│   │   ├─── evaluation_schema.py
│   │   ├─── quotation_schema.py
│   │   ├─── sanction_schema.py
│   │   ├─── tender_schema.py
│   │   ├─── user_schema.py
│   │   ├─── vendor_schema.py
│   │  
│   ├───scripts/
|   |   ├─── create_admin.py
|   |   
│   ├───services/
│   │   ├─── auth_service.py
│   │   ├─── evaluation_service.py
│   │   ├─── quotation_service.py
│   │   ├─── report_service.py
│   │   ├─── sanction_service.py
│   │   ├─── tender_service.py
|   | 
│   ├───utilities/
│   │   ├─── email_service.py
│   │   ├─── file_storage.py
|   |
|   └─ main.py
|
├───logs
|   ├───application.log
|   
├───tests
│   ├───api/
|   |
│   ├───integration/
|   |
│   ├───unit/
|   
├── uploads
|   └───quotations/
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Folder and File Descriptions

| Folder / File | Description |
|---|---|
| `app/` | Contains the application source code. |
| `app/main.py` | Creates the FastAPI application, registers middleware, exception handling and routers, and manages application startup and shutdown. |
| `app/api/routers/` | Contains API endpoints for authentication, vendors, tenders, quotations, evaluations, sanctions, reports and health checks. |
| `app/api/dependencies/` | Contains database and authentication dependencies. |
| `app/core/` | Contains application configuration, security, custom exceptions and logging configuration. |
| `app/database/` | Handles database connections and SQLAlchemy model metadata. |
| `app/middleware/` | Contains request logging and observability middleware. |
| `app/models/` | Defines database tables and relationships using SQLAlchemy ORM. |
| `app/repositories/interfaces/` | Defines repository interfaces. |
| `app/repositories/implementations/` | Contains database operation implementations. |
| `app/schemas/` | Defines request and response schemas using Pydantic. |
| `app/services/` | Contains application business logic. |
| `alembic/` | Contains database migration files. |
| `tests/unit/` | Contains unit tests for business logic. |
| `tests/integration/` | Contains integration tests for application components and database operations. |
| `tests/api/` | Contains API endpoint tests. |
| `tests/conftest.py` | Contains shared Pytest fixtures. |
| `logs/` | Stores application and error logs. |
| `.env` | Contains environment-specific configuration values. |
| `alembic.ini` | Contains Alembic configuration. |
| `requirements.txt` | Lists project dependencies. |
| `README.md` | Contains project documentation. |


## Application Architecture

The application follows a layered architecture.

- **Router Layer:** Handles incoming API requests and responses.
- **Schema Layer:** Validates request data and structures response data using Pydantic.
- **Service Layer:** Handles application business logic and validations.
- **Repository Layer:** Handles database operations through repository interfaces and implementations.
- **Model Layer:** Defines database tables, columns, constraints and relationships using SQLAlchemy.
- **Database Layer:** Manages database connections and sessions.

## Database Tables

The application uses PostgreSQL with SQLAlchemy ORM.

| Table Name | Primary Key | Description |
|---|---|---|
| `users` | `id` | Stores user login details, email, password hash and role. |
| `vendors` | `id` | Stores registered vendor and company information. |
| `tenders` | `id` | Stores tender details, eligibility criteria, estimated cost, deadlines and status. |
| `quotations` | `id` | Stores vendor quotations, quoted amounts, proposals and uploaded document information. |
| `evaluations` | `id` | Stores quotation evaluation scores, decisions and evaluation dates. |
| `sanctions` | `id` | Stores sanctioned quotation details, tender references, sanctioned amounts and dates. |
| `refresh_tokens` | `id` | Stores refresh token information for authentication. |


### Stored Procedure and Trigger
 
- **Stored Procedure:** `close_expired_tenders` is used to close the tender after the end date.
- **Trigger:** ` trg_reject_other_quotations` used to trigger the other quotation to reject status after the sanction.

## Application Workflow

1. Administartor logs in and creates the tenders.
2. Vendor register and provides the company details.
3. Vendors log in and view available tenders.
4. Vendors submit quotations with their proposed amount, proposal and supporting PDF document.
5. The administrator reviews and evaluates submitted quotations.
6. Evaluation scores and decisions are recorded.
7. The administrator sanctions an eligible quotation.
8. Sanction details are stored in the database.
9. The email is sent to the sanctioned company mail id.
10. Administrators can retrieve tender, quotation, evaluation and sanction reports.


## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | REST API development |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Alembic | Database migrations |
| Pydantic | Request and response validation |
| JWT | Authentication and token management |
| Pytest | Unit and integration testing |
| HTTPX | API testing |
| Uvicorn | ASGI application server |
| Ruff | Code linting and formatting |



## Prerequisites

Install the following before running the application:

- Python 3.14 or a compatible supported version.
- PostgreSQL.
- Git.


## Setup and Installation

### 1. Clone the repository

```powershell
git clone <https://github.com/Devasree-k/Tender_and_Quotation_Assessment_System.git>

cd Tender_and_Quotation_Assessment_System
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv

.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip

pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and configure the required database and authentication settings.

Update the values according to your local PostgreSQL configuration.

### 5. Prepare the PostgreSQL database

Create a PostgreSQL database and configure its connection details in `.env`.

Run the Alembic migrations:

```powershell
alembic upgrade head
```

### 6. Start the application

```powershell
uvicorn app.main:app --reload
```

The application will run at:

`http://127.0.0.1:8000`


## Database Migration with Alembic

Alembic is used to manage database schema changes.

### Create a new migration

After changing the SQLAlchemy models:

```powershell
alembic revision --autogenerate -m "description_of_change"
```

### Apply all migrations

```powershell
alembic upgrade head
```

### Check the current migration

```powershell
alembic current
```

### View migration history

```powershell
alembic history
```

### Roll back the latest migration

```powershell
alembic downgrade -1
```

### Roll back to a specific revision

```powershell
alembic downgrade <revision_id>
```



## Running Tests

Pytest is used to test application functionality.

Run all tests from the project root:

```powershell
python -m pytest -v
```

Run unit tests:

```powershell
python -m pytest tests/unit -v
```

Run integration tests:

```powershell
python -m pytest tests/integration -v
```

Run API tests:

```powershell
python -m pytest tests/api -v
```

The tests cover business logic, database operations, authentication, authorization and API endpoints.

## Code Quality

Ruff is used for code linting and formatting.

Check code using Ruff:

```powershell
ruff check .
```

Format the project:

```powershell
ruff format .
```


## API documentation

FastAPI provides Swagger UI for testing and exploring the API endpoints.

Swagger UI:
`http://127.0.0.1:8000/docs`


## Authorization

Protected endpoints require a valid JWT access token.

1. Register or log in using the authentication API.
2. Copy the returned `access_token`.
3. Open Swagger UI.
4. Click **Authorize**.
5. Enter the access token.
6. Click Authorize.

### User Roles

- **Admin:** Can manage tenders, review quotations, evaluate submissions, manage sanctions and access reports.
- **Vendor:** Can manage vendor-related information, view available tenders and submit quotations.

## 1. Authentication APIs

Base URL: `/api/auth`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Registers a new vendor. |
| POST | `/login` | Authenticates a user and generates tokens. |
| POST | `/refresh` | Generates a new access token using a refresh token. |
| POST | `/logout` | Logs out the authenticated user. |
| GET | `/get my profile` | Retrieves the logged-in user's information. |

## 2. Tender APIs

Base URL: `/api/tenders`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/Create Tender` | Creates a new tender. |
| GET | `/List Tender` | Retrieves tenders with search, filters and pagination. |
| GET | `/List open Tender` | Retrives only the opened tender with pagination. |
| GET | `/{tender_id}` | Retrieves a tender by ID. |
| PUT | `/{tender_id}` | To update by tender ID. |
| PATCH | `/{tender_id}` | Updates tender information. |
| DELETE | `/{tender_id}` | Deletes a tender. |

Tender management operations are available to administrators, while vendors can retrieve available tenders.

## 3. Quotation APIs

Base URL: `/api/quotations`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/` | Submits a quotation. |
| GET | `/` | Retrieves quotations. |
| GET | `/get my quotation` | Get the current user Quotation. |
| GET | `/{quotation_id}` | Retrieves a quotation by ID. |
| PATCH | `/{quotation_id}` | Withdraw Quotation. |

Vendors submit quotations against available tenders with the quoted amount, proposal and supporting PDF document.

## 4. Evaluation APIs

Base URL: `/api/evaluations`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/{quotation_id}` | Creates an evaluation for a quotation. |
| GET | `/` | Retrieves all evaluations. |
| GET | `/{quotation_id}` | Get by quotation ID. |
| GET | `/{evaluation_id}` | Retrieves an evaluation by ID. |
| GET | `/{tender_id}` | Get approved quotations by tender ID.|


Evaluations contain scores, decisions and evaluation dates. Administrators review quotation details and vendor eligibility before making evaluation decisions.

## 5. Sanction APIs

Base URL: `/api/sanctions`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/` | Creates a sanction for an approved quotation. |
| GET | `/` | Retrieves sanction records. |
| GET | `/` | To get sanction detail based on tender ID. |
| GET | `/{sanction_id}` | Retrieves sanction information by ID. |

Sanction records contain the selected quotation, associated tender, sanctioned amount and sanction date.

## 6. Report APIs

Base URL: `/api/reports`

Provides report information related to tender assessment operations.

Reports include information about tenders, quotations, evaluations and sanctions.

These reports help administrators review tender and quotation assessment activities.

## 7. Health Check API

Base URL: `/api/health`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks application and database health. |

The health check endpoint verifies whether the application and PostgreSQL database are functioning correctly.

## 8. Home API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the API application is running. |

## Logging and Monitoring

The application uses Python logging to record application activities and errors.

Observability middleware is implemented to monitor incoming API requests.

The middleware tracks:

- HTTP request method.
- Request URL.
- Response status code.
- Request ID.
- Request processing time.

The response includes:

- `X-Request-ID`
- `X-Process-Time-ms`

Application startup and shutdown operations are managed using FastAPI lifespan.

## Exception Handling

Custom exceptions are implemented to handle application-specific errors.

The application handles situations such as:

- Resource not found.
- Duplicate records.
- Invalid input.
- Unauthorized access.
- Forbidden operations.
- Invalid or expired tokens.
- Database-related errors.
- Invalid uploaded PDF documents.




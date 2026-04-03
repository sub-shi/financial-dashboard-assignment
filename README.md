# Objective

This project implements a backend system for a financial dashboard application. It demonstrates backend design, data modeling, role-based access control, and aggregation APIs for analytics.

The system allows different users (admin, analyst, viewer) to interact with financial data based on their permissions.

## Features

- RESTful APIs using Flask
- SQLite database with SQLAlchemy ORM
- JWT-based authentication
- Role-Based Access Control (RBAC)
- Financial record management (CRUD + filtering)
- Dashboard analytics APIs:
    - Total income / expenses / balance\
    - Category-wise breakdown
    - Category-wise breakdown
    - Monthly trends
- User endpoints: create, list, update
- Record endpoints: create, list, update, delete, filter by type/category/date

## Architecture

The project follows a modular and scalable structure:

models/     → Database models
routes/     → API endpoints
utils/      → Helpers, decorators, JWT logic
- models/ → Database models
- Business logic is separated from routing
- RBAC is implemented using a reusable decorator

## Authentication & Authorization

- JWT tokens are issued on login
- Each request is validated using a custom decorator
- Each request is validated using a custom decorator

## Role Permissions
Role	Permissions
Admin	Full access (users, records, dashboard)
Analyst	Read records + dashboard insights
Viewer	Dashboard access only

## User & Role Management
- Create and manage users
- Assign roles (admin, analyst, viewer)
- Assign roles (admin, analyst, viewer)
- Prevent duplicate users (email-based)


## Financial Records
- Each record contains:
    - Amount
    - Type (income / expense)
    - Category
    - Date
    - Notes
## Supported Operations
- Create, update, delete records 
- Filter by type, category, and date range


## Dashboard APIs
- Designed to provide aggregated insights:
    - Total income
    - Total expenses
    - Net balance
    - Category-wise totals
    - Monthly trends
    - Recent transactions
- Aggregation is performed at the database level using SQL functions.


## Tech Stack
- Python
- Flask
- SQLAlchemy
- SQLite
- PyJWT

## Setup
1. Clone repository

```bash
cd d:\Financial-Dashboard-Assignment
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app

```bash
python app.py
```

3. Open `http://localhost:5000` to confirm service is running:

```json
{"message": "Finance Backend Running"}
```

## Authentication

### Login

POST `/auth/login`

Body JSON:

```json
{
  "email": "admin@example.com"
}
```

Response:

```json
{
  "token": "<jwt-token>",
  "user": { ... }
}
```

Use header on protected endpoints:

`Authorization: Bearer <jwt-token>`

## Roles & Permissions

- `admin`: full access (users + records + dashboard)
- `analyst`: records read + dashboard data
- `viewer`: dashboard read only

## API Endpoints

### Users (`/users`)
- `GET /users` (admin)
- `POST /users` (admin)
- `PUT /users/<id>` (admin)

### Records (`/records`)
- `POST /` (admin)
- `GET /` (admin, analyst)
  - query params: `type`, `category`, `start_date`, `end_date`
- `PUT /<id>` (admin)
- `DELETE /<id>` (admin)

### Dashboard (`/dashboard`)
- `GET /summary` (admin, analyst, viewer)
- `GET /categories` (admin, analyst)
- `GET /trends` (admin, analyst)
- `GET /recent` (admin, analyst, viewer)

## Models

### User
- `id`, `name`, `email`, `role_id`, `is_active`
- relation to `Record`

### Role
- `id`, `name`
- relation to `User`

### Record
- `id`, `amount`, `type` (`income`/`expense`), `category`, `date`, `note`, `user_id`

## Data Validations

- Input validation for all APIs
- Proper HTTP status codes (400, 401, 403, 404)
- Protection against invalid or unauthorized operations
- Centralized JSON validation helper
- `amount` must be positive
- `type` must be `income` or `expense`
- required JSON on requests

## Notes

- `SECRET_KEY` is static in `config.py`; update for production.
- Database is SQLite and created at startup in the current working folder.
- No password management: login only with user email for prototype/demo.

## Data Persistence

- SQLite is used for simplicity and ease of setup.
- SQLAlchemy ORM ensures clean and maintainable database interactions.


## Assumptions

- Authentication is simplified (email-based login)
- No password handling for demo purposes
- SQLite is sufficient for this assignment
- System is designed for demonstration, not production scale

## Future Improvements

- Add password hashing/signup flow
- Add user password authentication + refresh tokens
- Add tests and input schema validation
- Add migrations via Flask-Migrate


## Conclusion
This project demonstrates a well-structured backend system with proper separation of concerns, role-based access control, and efficient data aggregation for analytics.
# Freelancing Platform Backend API

A role-based backend API for a freelancing marketplace where **Clients** can publish projects and manage proposals, while **Freelancers** can browse projects, submit proposals, and manage accepted work.

This project was developed as part of **Backend Development Internship – Phase 2, Problem 2**.

## Tech Stack

- Python
- Django
- Django REST Framework
- MySQL
- JWT Authentication
- Django CORS Headers
- Pillow
- Postman
- Git & GitHub

## User Roles

### Client

Clients can:

- Create projects
- View projects
- Update their own projects
- Delete their own projects
- View proposals for their projects
- Accept proposals
- Reject proposals
- Start projects
- Complete projects
- Cancel projects
- View their dashboard

### Freelancer

Freelancers can:

- Browse projects
- Search projects
- Filter projects by category
- Submit proposals
- View their submitted proposals
- Withdraw their proposals
- Complete projects assigned to them
- View their dashboard

## Core Features

### Authentication

- User signup
- User login
- JWT access and refresh tokens
- Password hashing
- Client/Freelancer role selection
- Duplicate email validation
- Role validation

### Project Management

Projects contain:

- Title
- Category
- Budget
- Description
- Required skills
- Deadline
- Experience level
- Status
- Client
- Assigned freelancer
- Creation timestamp

Project statuses:

- `open`
- `in_progress`
- `completed`
- `cancelled`

### Proposal Management

Proposals contain:

- Project
- Freelancer
- Bid amount
- Cover letter
- Delivery time
- Status
- Submission time

Proposal statuses:

- `pending`
- `accepted`
- `rejected`
- `withdrawn`

The system prevents duplicate proposals from the same freelancer for the same project.

### Project Workflow

The main workflow is:

```text
Open
  ↓
Proposal Submitted
  ↓
Client Accepts Proposal
  ↓
Freelancer Assigned
  ↓
In Progress
  ↓
Completed
```

A project can also be cancelled while it is `open` or `in_progress`.

When a proposal is accepted:

- The selected proposal becomes `accepted`
- Other pending proposals become `rejected`
- The freelancer is assigned to the project
- The project becomes `in_progress`

### Dashboards

Client dashboard:

- Total projects
- Active projects
- Completed projects
- Total proposals received

Freelancer dashboard:

- Applied projects
- Active projects
- Completed projects
- Accepted proposals

## API Endpoints

### Authentication

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/signup/` | Public |
| POST | `/api/login/` | Public |
| POST | `/api/token/refresh/` | Public |

### Projects

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/projects/` | Client |
| GET | `/api/projects/` | Authenticated |
| GET | `/api/projects/<id>/` | Authenticated |
| PUT | `/api/projects/<id>/` | Project owner |
| DELETE | `/api/projects/<id>/` | Project owner |

Project browsing supports:

```text
GET /api/projects/?search=django
GET /api/projects/?category=Backend Development
```

### Proposals

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/projects/<id>/proposal/` | Freelancer |
| GET | `/api/my-proposals/` | Freelancer |
| GET | `/api/projects/<id>/proposals/` | Project owner |
| PUT | `/api/proposal/<id>/accept/` | Project owner |
| PUT | `/api/proposal/<id>/reject/` | Project owner |
| DELETE | `/api/proposal/<id>/` | Proposal owner |

### Project Status

| Method | Endpoint | Access |
|---|---|---|
| PUT | `/api/project/<id>/start/` | Project owner |
| PUT | `/api/project/<id>/complete/` | Client or assigned Freelancer |
| PUT | `/api/project/<id>/cancel/` | Project owner |

### Dashboards

| Method | Endpoint | Access |
|---|---|---|
| GET | `/api/client/dashboard/` | Client |
| GET | `/api/freelancer/dashboard/` | Freelancer |

## Project Structure

```text
freelancing-platform-backend/
│
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py
│
├── projects/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py
│
├── proposals/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py
│
└── dashboard/
    ├── views.py
    └── urls.py
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Freelancing-Platform-Backend.git
cd Freelancing-Platform-Backend
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Create a MySQL database, for example:

```sql
CREATE DATABASE freelancing_db;
```

### 5. Configure environment variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=freelancing_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Do not commit `.env` to GitHub.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Testing

The complete API was tested using **Postman**.

Testing covered:

- Signup and login
- JWT authentication
- Role-based access control
- Project CRUD
- Project search
- Category filtering
- Proposal submission
- Duplicate proposal prevention
- Proposal withdrawal
- Proposal acceptance and rejection
- Freelancer assignment
- Project completion and cancellation
- Client dashboard
- Freelancer dashboard
- Ownership protection
- Unauthenticated access
- Invalid input handling

## Security

The backend includes:

- JWT authentication
- Password hashing
- Role-based permissions
- Project ownership verification
- Proposal ownership verification
- Input validation
- Secure environment configuration
- CORS configuration
- Protected API routes


## 👨‍💻 Author

**Jubair Bin Hasan**

Computer Science & Engineering
University of Asia Pacific

---

## 📄 License

This project was developed for educational and internship purposes.
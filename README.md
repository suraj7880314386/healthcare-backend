# Healthcare Backend

A backend for a healthcare app built with Django, Django REST Framework and PostgreSQL.
Users can register, log in with JWT, and manage patients, doctors and patient-doctor mappings.

## Tech stack

- Django + Django REST Framework
- PostgreSQL
- JWT auth with `djangorestframework-simplejwt`
- `python-decouple` for environment variables

## Project structure

```
healthcare_backend/
├── config/        settings, root urls, custom error handler, tests
├── accounts/      custom user model, register and login
├── patients/      patient model and APIs
├── doctors/       doctor model and APIs
├── mappings/      patient-doctor assignments
├── manage.py
├── requirements.txt
└── .env.example
```

## Setup

1. Create a virtual environment and install packages

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Create the database in PostgreSQL

```sql
CREATE DATABASE healthcare_db;
```

3. Copy the env file and fill in your values

```bash
cp .env.example .env
```

4. Create tables and run the server

```bash
python manage.py makemigrations accounts patients doctors mappings
python manage.py migrate
python manage.py runserver
```

The API is now live at `http://127.0.0.1:8000/api/`.

## API endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| POST | `/api/auth/register/` | Register with name, email, password |
| POST | `/api/auth/login/` | Log in, returns access and refresh tokens |
| POST | `/api/auth/refresh/` | Get a new access token |
| POST | `/api/patients/` | Add a patient |
| GET | `/api/patients/` | List your patients |
| GET | `/api/patients/<id>/` | Patient details |
| PUT | `/api/patients/<id>/` | Update a patient |
| DELETE | `/api/patients/<id>/` | Delete a patient |
| POST | `/api/doctors/` | Add a doctor |
| GET | `/api/doctors/` | List all doctors |
| GET | `/api/doctors/<id>/` | Doctor details |
| PUT | `/api/doctors/<id>/` | Update a doctor (creator only) |
| DELETE | `/api/doctors/<id>/` | Delete a doctor (creator only) |
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List mappings of your patients |
| GET | `/api/mappings/<patient_id>/` | Doctors assigned to one patient |
| DELETE | `/api/mappings/<id>/` | Remove a doctor from a patient |

All endpoints except register, login and refresh need this header:

```
Authorization: Bearer <access_token>
```

## Example requests

Register

```json
POST /api/auth/register/
{ "name": "Suraj Singh", "email": "surajsingh7880@gmail.com", "password": "Suraj@7880" }
```

Login

```json
POST /api/auth/login/
{ "email": "surajsingh7880@gmail.com", "password": "Suraj@7880" }
```

Add a patient

```json
POST /api/patients/
{ "name": "Ravi Kumar", "age": 30, "gender": "M", "phone": "9876543210", "address": "Delhi" }
```

Add a doctor

```json
POST /api/doctors/
{ "name": "Mehta", "specialization": "Cardiology", "email": "mehtasingh1234@gmail.com", "phone": "9123456780", "experience": 10 }
```

Assign the doctor to the patient

```json
POST /api/mappings/
{ "patient": 1, "doctor": 1 }
```

## Design notes

- Email is the login field, so a custom user model is used.
- Patients are private. Each user only sees and edits the patients they created, and other users get a 404.
- Doctors are shared. Everyone logged in can view all doctors, but only the creator can edit or delete.
- A user can only assign doctors to their own patients, and the same doctor cannot be assigned to a patient twice.
- Every error comes back in one format: `{"success": false, "errors": {...}}`.
- Secrets and database details stay in `.env`, which is git-ignored.

## Running the tests

```bash
python manage.py test
```

The Postgres user needs the CREATEDB permission for this. For a quick run without Postgres, set `USE_SQLITE=True` in `.env`.

## Testing with Postman

Import `postman_collection.json`. Run **Login** first, it saves the token automatically for the other requests.

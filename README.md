# Voice AI Patient Registration API

A FastAPI-based REST API for voice-driven patient registration and management. Designed to integrate with voice AI systems for automated patient data collection.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Directory Structure](#directory-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Setup & Installation](#setup--installation)
- [Running the Application](#running-the-application)
- [Data Validation](#data-validation)
- [Response Format](#response-format)
- [Examples](#examples)

---

## Project Overview

**Purpose:** A FastAPI-based REST API for managing patient registration records through voice AI interactions.

**Tech Stack:**
- **Framework:** FastAPI (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Server:** Uvicorn ASGI server
- **Tunneling:** ngrok (for external access)
- **Validation:** Pydantic with custom validators

**Current Status:** ✅ Running (Uvicorn + ngrok active)

---

## Architecture

```
Voice AI Patient Registration API
    ├── FastAPI Application (main.py)
    ├── Database Layer (SQLAlchemy ORM)
    │   └── SQLite Database (patients.db)
    ├── CRUD Operations Layer
    ├── API Routes (Patient Management)
    ├── Data Schemas & Validation
    └── Error Handling (Custom Validation Handler)
```

**Flow:**
1. Request arrives at FastAPI app
2. Validation via Pydantic schemas
3. CRUD operations via SQLAlchemy ORM
4. Response wrapped in standard envelope
5. Uvicorn serves API, ngrok exposes publicly

---

## Directory Structure

```
d:\Voice Agent\
├── README.md                           # This file
├── patients.db                         # SQLite database (auto-created)
└── venv/                               # Python virtual environment
    ├── .gitignore
    ├── pyvenv.cfg
    ├── Scripts/                        # Python executables
    ├── Include/                        # Python headers
    ├── Lib/                            # Installed packages
    └── app/                            # Main application package
        ├── __pycache__/
        ├── main.py                     # FastAPI app entry point
        ├── database.py                 # SQLAlchemy setup & session management
        ├── models.py                   # SQLAlchemy Patient ORM model
        ├── schemas.py                  # Pydantic validation schemas
        ├── crud.py                     # Create, Read, Update, Delete operations
        └── routes/
            ├── __pycache__/
            └── patients.py             # Patient API endpoints
```

---

## Database Schema

### Patient Table (`patients`)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `patient_id` | UUID (String) | PRIMARY KEY | Auto-generated unique identifier |
| `first_name` | String(50) | NOT NULL | Patient's first name |
| `last_name` | String(50) | NOT NULL | Patient's last name |
| `date_of_birth` | Date | NOT NULL | Patient's date of birth |
| `sex` | String(30) | NOT NULL | Male, Female, Other, Decline to Answer |
| `phone_number` | String(10) | NOT NULL, INDEXED | US 10-digit phone (normalized) |
| `email` | String(255) | NULLABLE | Valid email address |
| `address_line_1` | String(255) | NOT NULL | Primary address |
| `address_line_2` | String(255) | NULLABLE | Secondary address |
| `city` | String(100) | NOT NULL | City name |
| `state` | String(2) | NOT NULL | US state abbreviation (AL-WI, DC) |
| `zip_code` | String(10) | NOT NULL | 5-digit or ZIP+4 format |
| `insurance_provider` | String(255) | NULLABLE | Insurance company name |
| `insurance_member_id` | String(100) | NULLABLE | Insurance member ID |
| `preferred_language` | String(50) | DEFAULT='English' | Patient's preferred language |
| `emergency_contact_name` | String(255) | NULLABLE | Emergency contact person |
| `emergency_contact_phone` | String(10) | NULLABLE | Emergency contact phone |
| `created_at` | DateTime | NOT NULL | Record creation timestamp (UTC) |
| `updated_at` | DateTime | NOT NULL | Last update timestamp (UTC) |
| `deleted_at` | DateTime | NULLABLE | Soft delete timestamp (if deleted) |

**Note:** Phone numbers are stored as normalized 10-digit strings. Deleted records are flagged with `deleted_at` timestamp (soft delete).

---

## API Endpoints

### Health & Status

#### `GET /` - Root
```
Returns API status message
Response: {"message": "Voice AI Patient Registration API is running"}
```

#### `GET /health` - Health Check
```
Returns API health status
Response: {"status": "healthy"}
```

---

### Patient Management (`/patients`)

#### 1. `POST /patients` - Create Patient
**Creates a new patient record.**

```bash
POST /patients
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "sex": "Male",
  "phone_number": "5551234567",
  "email": "john.doe@example.com",
  "address_line_1": "123 Main St",
  "address_line_2": "Apt 4B",
  "city": "Springfield",
  "state": "IL",
  "zip_code": "62701",
  "insurance_provider": "BlueCross",
  "insurance_member_id": "BC123456789",
  "preferred_language": "English",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "5559876543"
}
```

**Response (201 Created):**
```json
{
  "data": {
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-15",
    "sex": "Male",
    "phone_number": "5551234567",
    "email": "john.doe@example.com",
    "address_line_1": "123 Main St",
    "address_line_2": "Apt 4B",
    "city": "Springfield",
    "state": "IL",
    "zip_code": "62701",
    "insurance_provider": "BlueCross",
    "insurance_member_id": "BC123456789",
    "preferred_language": "English",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "5559876543",
    "created_at": "2026-08-11T10:30:00Z",
    "updated_at": "2026-08-11T10:30:00Z",
    "deleted_at": null
  },
  "error": null
}
```

**Error Response (409 Conflict):**
```json
{
  "data": null,
  "error": "A patient with this phone number already exists."
}
```

---

#### 2. `GET /patients` - List Patients
**Retrieves all active patients with optional filtering.**

```bash
GET /patients
GET /patients?last_name=Doe
GET /patients?date_of_birth=1990-01-15
GET /patients?phone_number=5551234567
```

**Query Parameters:**
- `last_name` (string, optional) - Filter by last name (partial match, case-insensitive)
- `date_of_birth` (date, optional) - Filter by DOB (YYYY-MM-DD)
- `phone_number` (string, optional) - Filter by phone (must be exact 10-digit)

**Response (200 OK):**
```json
{
  "data": [
    {
      "patient_id": "550e8400-e29b-41d4-a716-446655440000",
      "first_name": "John",
      "last_name": "Doe",
      ...
    },
    {
      "patient_id": "660f9511-f40c-52e5-b827-557766551111",
      "first_name": "Jane",
      "last_name": "Smith",
      ...
    }
  ],
  "error": null
}
```

---

#### 3. `GET /patients/{patient_id}` - Get Patient by ID
**Retrieves a specific patient record by UUID.**

```bash
GET /patients/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
{
  "data": {
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "first_name": "John",
    "last_name": "Doe",
    ...
  },
  "error": null
}
```

**Response (404 Not Found):**
```json
{
  "data": null,
  "error": "Patient not found."
}
```

---

#### 4. `PUT /patients/{patient_id}` - Update Patient
**Updates one or more fields of an existing patient (partial updates supported).**

```bash
PUT /patients/550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json

{
  "phone_number": "5559999999",
  "email": "newemail@example.com",
  "preferred_language": "Spanish"
}
```

**Response (200 OK):**
```json
{
  "data": {
    "patient_id": "550e8400-e29b-41d4-a716-446655440000",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "5559999999",
    "email": "newemail@example.com",
    "preferred_language": "Spanish",
    "updated_at": "2026-08-11T11:45:00Z",
    ...
  },
  "error": null
}
```

---

#### 5. `DELETE /patients/{patient_id}` - Delete Patient
**Soft-deletes a patient (sets `deleted_at` timestamp, record not actually removed).**

```bash
DELETE /patients/550e8400-e29b-41d4-a716-446655440000
```

**Response (200 OK):**
```json
{
  "data": {},
  "error": null
}
```

---

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Windows/Linux/macOS

### 1. Create Virtual Environment
```bash
cd "d:\Voice Agent"
python -m venv venv
```

### 2. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy pydantic[email]
```

### 4. Database Setup
The SQLite database is auto-created on first run. No manual setup needed.

```bash
# The patients.db will be created automatically in the project root
```

---

## Running the Application

### 1. Start Uvicorn Server
```bash
cd "d:\Voice Agent"
venv\Scripts\activate
uvicorn venv.app.main:app --reload --host 0.0.0.0 --port 8000
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 2. Expose via ngrok (in separate terminal)
```bash
ngrok http 8000
```

**Output:**
```
ngrok                                       (Ctrl+C to quit)
Public URL: https://xxxxxxxx-xxxx.ngrok.io
```

### 3. Access API
- **Local:** http://localhost:8000
- **Public:** https://xxxxxxxx-xxxx.ngrok.io (via ngrok)
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Alternative Docs:** http://localhost:8000/redoc (ReDoc)

---

## Data Validation

All input data is validated using Pydantic schemas with custom validators.

### Field Validation Rules

| Field | Rules |
|-------|-------|
| `first_name`, `last_name` | 1-50 chars, letters/spaces/hyphens/apostrophes only |
| `date_of_birth` | Valid date, cannot be in the future |
| `sex` | One of: Male, Female, Other, Decline to Answer |
| `phone_number` | US 10-digit number (accepts multiple formats) |
| `email` | Valid email format (optional) |
| `state` | Valid US state abbreviation (AL-WI, DC) |
| `zip_code` | 5-digit or ZIP+4 format (XXXXX or XXXXX-XXXX) |
| `emergency_contact_phone` | US 10-digit number (optional) |

### Phone Number Normalization
Accepts multiple formats, automatically normalizes to 10 digits:
- `5551234567` → `5551234567`
- `(555) 123-4567` → `5551234567`
- `555-123-4567` → `5551234567`
- `+1 555 123 4567` → `5551234567`

### Validation Error Response
```json
{
  "data": null,
  "error": [
    {
      "type": "value_error",
      "loc": ["body", "phone_number"],
      "msg": "Phone number must be a valid US 10-digit number.",
      "input": "invalid"
    }
  ]
}
```

---

## Response Format

All API responses follow a standard envelope format:

```json
{
  "data": {
    // Success: actual data; Failure: null
  },
  "error": null  // Success: null; Failure: error message or array
}
```

### Success Response Example
```json
{
  "data": { "patient_id": "...", "first_name": "John", ... },
  "error": null
}
```

### Error Response Example
```json
{
  "data": null,
  "error": "Patient not found."
}
```

---

## Examples

### Example 1: Create a Patient via cURL

```bash
curl -X POST "http://localhost:8000/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Johnson",
    "date_of_birth": "1985-05-20",
    "sex": "Female",
    "phone_number": "2125551234",
    "email": "alice@example.com",
    "address_line_1": "456 Oak Ave",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001"
  }'
```

### Example 2: Search Patients by Last Name

```bash
curl "http://localhost:8000/patients?last_name=Johnson"
```

### Example 3: Update Patient Email

```bash
curl -X PUT "http://localhost:8000/patients/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{"email": "newalice@example.com"}'
```

### Example 4: Delete Patient

```bash
curl -X DELETE "http://localhost:8000/patients/550e8400-e29b-41d4-a716-446655440000"
```

---

## Project Files Overview

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app initialization, error handlers, root routes |
| `database.py` | SQLAlchemy engine, session management, base class |
| `models.py` | SQLAlchemy ORM Patient model definition |
| `schemas.py` | Pydantic schemas with validation (Create, Update, Response) |
| `crud.py` | Database CRUD operations (Create, Read, Update, Delete) |
| `routes/patients.py` | API endpoint definitions for patient management |

---

## Notes

- Records are soft-deleted (flagged with `deleted_at` timestamp)
- All timestamps are in UTC timezone
- Phone numbers must be US numbers (10-digit format)
- Concurrent requests are supported via Uvicorn
- FastAPI auto-generates interactive API docs at `/docs`

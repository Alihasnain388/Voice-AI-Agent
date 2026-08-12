# Voice Agent Patient Registration System

A voice-powered patient registration system that allows users to provide their information through a natural phone conversation. The AI agent collects and confirms patient details, then stores them through a FastAPI backend.

## Architecture

```text
Caller
   ↓
Vapi Voice AI Agent
   ↓
FastAPI REST API
   ↓
SQLite Database
```

**ngrok** is used to expose the local FastAPI server through a public HTTPS endpoint for Vapi integration.

## Tech Stack

* **Vapi** — Voice AI, telephony, STT & TTS
* **FastAPI** — REST API and backend
* **Python** — Backend development
* **SQLite** — Persistent patient data storage
* **ngrok** — Public API tunneling

## Features

* Natural conversational patient registration
* Patient demographic data collection
* Input validation
* Confirmation before saving
* Persistent SQLite storage
* REST API for patient records
* Vapi → FastAPI integration
* Error handling for invalid inputs and failed requests

## API Endpoints

| Method | Endpoint         | Description           |
| ------ | ---------------- | --------------------- |
| GET    | `/patients`      | List all patients     |
| GET    | `/patients/{id}` | Get a patient by ID   |
| POST   | `/patients`      | Create a patient      |
| PUT    | `/patients/{id}` | Update a patient      |
| DELETE | `/patients/{id}` | Soft-delete a patient |

## Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the FastAPI server

```bash
uvicorn main:app --reload
```

### Start ngrok

```bash
ngrok http 8000
```

Use the generated HTTPS URL when configuring the Vapi tools/webhooks.

## Vapi Workflow

1. Greets the caller.
2. Collects patient information.
3. Handles corrections and invalid inputs.
4. Confirms the collected information.
5. Sends the confirmed data to the FastAPI API.
6. FastAPI stores the patient in SQLite.
7. The agent confirms successful registration.

## API Documentation

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```





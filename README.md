# Voice AI Patient Registration System

A voice-powered patient registration system that allows users to provide their information through a natural phone conversation. The AI agent collects and confirms patient details, then stores them through a FastAPI backend.

## Architecture

```text
Caller
   ↓
Vapi Voice AI Agent
   ↓
FastAPI REST API
   ↓
Database
```

**ngrok** is used to expose the local FastAPI server through a public HTTPS endpoint for Vapi integration.

## Tech Stack

* **Vapi** — Voice AI, telephony, STT & TTS
* **FastAPI** — Backend REST API
* **Python** — Backend development
* **Database** — Persistent patient data storage
* **ngrok** — Public API tunneling

## Features

* Natural conversational patient registration
* Collects patient demographic information
* Validates user input
* Confirms information before saving
* Persistent patient records
* REST API for managing patient data
* Voice AI → FastAPI integration
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

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file and add the required API keys and configuration.

```env
VAPI_API_KEY=your_api_key
# Add other required variables
```

### 4. Start the FastAPI server

```bash
uvicorn main:app --reload
```

### 5. Start ngrok

```bash
ngrok http 8000
```

Use the generated HTTPS URL when configuring the Vapi tools/webhooks.

## Vapi Workflow

The voice agent:

1. Greets the caller.
2. Collects the required patient information.
3. Handles corrections and invalid inputs.
4. Reads the information back for confirmation.
5. Sends the confirmed data to the FastAPI API.
6. Confirms successful registration to the caller.

## API Documentation

FastAPI automatically provides interactive API documentation:

```text
http://localhost:8000/docs
```



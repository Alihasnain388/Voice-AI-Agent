Voice AI Agent for Patient Registration System

A voice-powered patient registration system that allows users to provide their information through a natural phone conversation. The AI agent collects and confirms patient details, then stores them through a FastAPI backend.

Architecture
Caller
   ↓
Vapi Voice AI Agent
   ↓
FastAPI REST API
   ↓
Database

ngrok is used to expose the local FastAPI server through a public HTTPS endpoint for Vapi integration.

Tech Stack
Vapi — Voice AI, telephony, STT & TTS
FastAPI — Backend REST API
Python — Backend development
Database — Persistent patient data storage
ngrok — Public API tunneling

Features
Natural conversational patient registration
Collects patient demographic information
Validates user input
Confirms information before saving
Persistent patient records
REST API for managing patient data
Voice AI → FastAPI integration
Error handling for invalid inputs and failed requests

API Endpoints
Method	Endpoint	Description
GET	/patients	List all patients
GET	/patients/{id}	Get a patient by ID
POST	/patients	Create a patient
PUT	/patients/{id}	Update a patient
DELETE	/patients/{id}	Soft-delete a patient

Setup
1. Clone the repository
git clone <repository-url>
cd <project-folder>
2. Install dependencies
pip install -r requirements.txt
4. Start the FastAPI server
uvicorn main:app --reload
5. Start ngrok
ngrok http 8000

Use the generated HTTPS URL when configuring the Vapi tools/webhooks.

Vapi Workflow

The voice agent:

Greets the caller.
Collects the required patient information.
Handles corrections and invalid inputs.
Reads the information back for confirmation.
Sends the confirmed data to the FastAPI API.
Confirms successful registration to the caller.
API Documentation

FastAPI automatically provides interactive API documentation:

http://localhost:8000/docs

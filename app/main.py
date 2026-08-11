from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .database import Base, engine
from . import models
from .routes.patients import router as patients_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Voice AI Patient Registration API",
    version="1.0.0"
)


# ============================================================
# VALIDATION ERROR HANDLER
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():

        clean_error = {
            "type": error.get("type"),
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "input": error.get("input"),
        }

        errors.append(clean_error)

    print("VALIDATION ERROR:")
    print(errors)

    return JSONResponse(
        status_code=422,
        content={
            "data": None,
            "error": errors
        }
    )


# ============================================================
# ROUTERS
# ============================================================

app.include_router(patients_router)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Voice AI Patient Registration API is running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
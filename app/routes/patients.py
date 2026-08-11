from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db
from ..schemas import (
    PatientCreate,
    PatientResponse,
    PatientUpdate,
    ResponseEnvelope,
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post(
    "",
    response_model=ResponseEnvelope[PatientResponse],
    status_code=status.HTTP_201_CREATED
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    existing_patient = crud.get_patient_by_phone(
        db,
        patient.phone_number
    )

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A patient with this phone number already exists."
        )

    db_patient = crud.create_patient(db, patient)

    return ResponseEnvelope(
        data=db_patient,
        error=None
    )


@router.get(
    "",
    response_model=ResponseEnvelope[list[PatientResponse]]
)
def list_patients(
    last_name: str | None = None,
    date_of_birth: date | None = None,
    phone_number: str | None = None,
    db: Session = Depends(get_db)
):
    patients = crud.get_patients(
        db,
        last_name=last_name,
        date_of_birth=date_of_birth,
        phone_number=phone_number,
    )

    return ResponseEnvelope(
        data=patients,
        error=None
    )


@router.get(
    "/{patient_id}",
    response_model=ResponseEnvelope[PatientResponse]
)
def get_patient(
    patient_id: UUID,
    db: Session = Depends(get_db)
):
    patient = crud.get_patient(
        db,
        str(patient_id)
    )

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found."
        )

    return ResponseEnvelope(
        data=patient,
        error=None
    )


@router.put(
    "/{patient_id}",
    response_model=ResponseEnvelope[PatientResponse]
)
def update_patient(
    patient_id: UUID,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db)
):
    patient = crud.get_patient(
        db,
        str(patient_id)
    )

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found."
        )

    updated_patient = crud.update_patient(
        db,
        patient,
        patient_data
    )

    return ResponseEnvelope(
        data=updated_patient,
        error=None
    )


@router.delete(
    "/{patient_id}",
    response_model=ResponseEnvelope[dict]
)
def delete_patient(
    patient_id: UUID,
    db: Session = Depends(get_db)
):
    patient = crud.get_patient(
        db,
        str(patient_id)
    )

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found."
        )

    deleted_patient = crud.delete_patient(
        db,
        patient
    )

    return ResponseEnvelope(
        data={
            "patient_id": deleted_patient.patient_id,
            "deleted_at": deleted_patient.deleted_at
        },
        error=None
    )
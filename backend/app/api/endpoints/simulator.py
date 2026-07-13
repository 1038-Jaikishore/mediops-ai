from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio
import random
import time
import json
import logging

logger = logging.getLogger("app")
router = APIRouter()

# --- Pydantic Schemas ---

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PatientProfile(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    allergies: List[str]
    history: List[str]

class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_name: str
    department: str
    appointment_time: str

class AppointmentResponse(BaseModel):
    appointment_id: str
    patient_id: str
    doctor_name: str
    department: str
    appointment_time: str
    status: str = "confirmed"

class LabTestResult(BaseModel):
    test_id: str
    patient_id: str
    test_type: str
    results: dict
    status: str = "completed"

class InvoiceCreate(BaseModel):
    patient_id: str
    amount: float
    description: str

class InvoiceResponse(BaseModel):
    invoice_id: str
    patient_id: str
    amount: float
    description: str
    payment_status: str = "pending"

class PrescriptionResponse(BaseModel):
    prescription_id: str
    patient_id: str
    medications: List[str]
    status: str = "filled"

# --- Helper function for structured logging ---

def log_structured(service: str, action: str, status_str: str, latency_ms: float, extra: dict) -> None:
    log_payload = {
        "service": service,
        "action": action,
        "status": status_str,
        "latency_ms": round(latency_ms, 2),
        **extra
    }
    # Log as raw JSON for structured parser collection
    logger.info(json.dumps(log_payload))

# --- Endpoints ---

@router.post("/auth/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest):
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.01, 0.04))  # Simulate network latency
    
    if payload.username == "admin" and payload.password == "mediops_secure_pass_2026":
        latency = (time.time() - start_time) * 1000
        log_structured(
            service="authentication",
            action="user_login",
            status_str="success",
            latency_ms=latency,
            extra={"username": payload.username}
        )
        return {"access_token": "mock-hms-jwt-token-2026", "token_type": "bearer"}
    
    latency = (time.time() - start_time) * 1000
    log_structured(
        service="authentication",
        action="user_login",
        status_str="unauthorized",
        latency_ms=latency,
        extra={"username": payload.username}
    )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )


@router.get("/patient/{patient_id}", response_model=PatientProfile, status_code=status.HTTP_200_OK)
async def get_patient_profile(patient_id: str):
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.01, 0.05))
    
    # Simple simulated profiles
    patients = {
        "PT-101": {
            "patient_id": "PT-101",
            "name": "Sarah Connor",
            "age": 42,
            "gender": "Female",
            "allergies": ["Penicillin"],
            "history": ["Hypertension", "Fractured Clavicle"]
        },
        "PT-102": {
            "patient_id": "PT-102",
            "name": "John Doe",
            "age": 35,
            "gender": "Male",
            "allergies": [],
            "history": ["Asthma"]
        }
    }
    
    profile = patients.get(patient_id)
    latency = (time.time() - start_time) * 1000
    
    if profile:
        log_structured(
            service="patient_portal",
            action="retrieve_profile",
            status_str="success",
            latency_ms=latency,
            extra={"patient_id": patient_id}
        )
        return profile
    
    log_structured(
        service="patient_portal",
        action="retrieve_profile",
        status_str="not_found",
        latency_ms=latency,
        extra={"patient_id": patient_id}
    )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Patient profile not found"
    )


@router.post("/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(payload: AppointmentCreate):
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.02, 0.06))
    
    appointment_id = f"APP-{random.randint(1000, 9999)}"
    latency = (time.time() - start_time) * 1000
    
    log_structured(
        service="appointments",
        action="schedule_appointment",
        status_str="success",
        latency_ms=latency,
        extra={
            "patient_id": payload.patient_id,
            "doctor": payload.doctor_name,
            "department": payload.department,
            "appointment_id": appointment_id
        }
    )
    return {
        "appointment_id": appointment_id,
        "patient_id": payload.patient_id,
        "doctor_name": payload.doctor_name,
        "department": payload.department,
        "appointment_time": payload.appointment_time,
        "status": "confirmed"
    }


@router.get("/laboratory/tests/{test_id}", response_model=LabTestResult, status_code=status.HTTP_200_OK)
async def get_lab_results(test_id: str):
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.03, 0.08))
    
    latency = (time.time() - start_time) * 1000
    
    # Simulate a database timeout scenario for test ID starting with LAB-ERR
    if test_id.startswith("LAB-ERR"):
        log_structured(
            service="laboratory",
            action="retrieve_results",
            status_str="timeout",
            latency_ms=latency,
            extra={"test_id": test_id}
        )
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Database connection lock during result fetch"
        )
        
    log_structured(
        service="laboratory",
        action="retrieve_results",
        status_str="success",
        latency_ms=latency,
        extra={"test_id": test_id, "patient_id": "PT-101"}
    )
    return {
        "test_id": test_id,
        "patient_id": "PT-101",
        "test_type": "Complete Blood Count",
        "results": {"WBC": 7.2, "RBC": 4.8, "Hemoglobin": 14.2, "Platelets": 250},
        "status": "completed"
    }


@router.post("/billing/invoice", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_invoice(payload: InvoiceCreate):
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.01, 0.05))
    
    invoice_id = f"INV-{random.randint(10000, 99999)}"
    latency = (time.time() - start_time) * 1000
    
    log_structured(
        service="billing",
        action="generate_invoice",
        status_str="success",
        latency_ms=latency,
        extra={
            "patient_id": payload.patient_id,
            "amount": payload.amount,
            "invoice_id": invoice_id
        }
    )
    return {
        "invoice_id": invoice_id,
        "patient_id": payload.patient_id,
        "amount": payload.amount,
        "description": payload.description,
        "payment_status": "pending"
    }


@router.get("/pharmacy/prescriptions/{prescription_id}", response_model=PrescriptionResponse, status_code=status.HTTP_200_OK)
async def get_prescription(prescription_id: str):
    start_time = time.time()
    await asyncio.sleep(random.uniform(0.01, 0.04))
    
    latency = (time.time() - start_time) * 1000
    
    log_structured(
        service="pharmacy",
        action="dispense_prescription",
        status_str="success",
        latency_ms=latency,
        extra={"prescription_id": prescription_id, "patient_id": "PT-102"}
    )
    return {
        "prescription_id": prescription_id,
        "patient_id": "PT-102",
        "medications": ["Albuterol Inhaler", "Amoxicillin 500mg"],
        "status": "filled"
    }

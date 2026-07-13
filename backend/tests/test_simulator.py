from fastapi.testclient import TestClient


def test_auth_login_success(client: TestClient):
    response = client.post(
        "/api/v1/simulator/auth/login",
        json={"username": "admin", "password": "mediops_secure_pass_2026"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_auth_login_unauthorized(client: TestClient):
    response = client.post(
        "/api/v1/simulator/auth/login",
        json={"username": "admin", "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_get_patient_profile_success(client: TestClient):
    response = client.get("/api/v1/simulator/patient/PT-101")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == "PT-101"
    assert data["name"] == "Sarah Connor"
    assert "Penicillin" in data["allergies"]


def test_get_patient_profile_not_found(client: TestClient):
    response = client.get("/api/v1/simulator/patient/PT-UNKNOWN")
    assert response.status_code == 404
    assert response.json()["detail"] == "Patient profile not found"


def test_create_appointment(client: TestClient):
    response = client.post(
        "/api/v1/simulator/appointments",
        json={
            "patient_id": "PT-101",
            "doctor_name": "Dr. Gregory House",
            "department": "Diagnostics",
            "appointment_time": "2026-07-13 14:00:00"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["appointment_id"].startswith("APP-")
    assert data["status"] == "confirmed"


def test_get_lab_results_success(client: TestClient):
    response = client.get("/api/v1/simulator/laboratory/tests/LAB-567")
    assert response.status_code == 200
    data = response.json()
    assert data["test_id"] == "LAB-567"
    assert data["test_type"] == "Complete Blood Count"
    assert data["status"] == "completed"


def test_get_lab_results_timeout(client: TestClient):
    response = client.get("/api/v1/simulator/laboratory/tests/LAB-ERR-999")
    assert response.status_code == 504
    assert response.json()["detail"] == "Database connection lock during result fetch"


def test_create_invoice(client: TestClient):
    response = client.post(
        "/api/v1/simulator/billing/invoice",
        json={
            "patient_id": "PT-102",
            "amount": 250.75,
            "description": "Lab Work and Consult Fee"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["invoice_id"].startswith("INV-")
    assert data["payment_status"] == "pending"


def test_get_prescription(client: TestClient):
    response = client.get("/api/v1/simulator/pharmacy/prescriptions/RX-701")
    assert response.status_code == 200
    data = response.json()
    assert data["prescription_id"] == "RX-701"
    assert "Albuterol Inhaler" in data["medications"]
    assert data["status"] == "filled"

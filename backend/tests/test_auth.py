from fastapi.testclient import TestClient


def test_auth_flow_and_rbac(client: TestClient):
    # 1. Test Login (Success for all roles)
    roles = ["admin", "operator", "viewer"]
    tokens = {}
    
    for role in roles:
        response = client.post(
            "/api/v1/auth/login",
            json={"username": role, "password": "mediops_secure_pass_2026"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        tokens[role] = data
        
    # 2. Test Login (Failure)
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong_password"}
    )
    assert response.status_code == 401
    
    # 3. Test Profile (/me) for Admin
    admin_headers = {"Authorization": f"Bearer {tokens['admin']['access_token']}"}
    response = client.get("/api/v1/auth/me", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert "admin" in data["roles"]

    # 4. Test Profile (/me) Unauthenticated
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    
    # 5. Test Token Refresh
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["admin"]["refresh_token"]}
    )
    assert response.status_code == 200
    refresh_data = response.json()
    assert "access_token" in refresh_data
    
    # 6. Test RBAC: Admin-Only endpoint accessed by Admin (Success)
    response = client.get("/api/v1/auth/admin-only", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome Admin"

    # 7. Test RBAC: Admin-Only endpoint accessed by Operator (403 Forbidden)
    operator_headers = {"Authorization": f"Bearer {tokens['operator']['access_token']}"}
    response = client.get("/api/v1/auth/admin-only", headers=operator_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions to access this resource"

    # 8. Test RBAC: Admin-Only endpoint accessed by Viewer (403 Forbidden)
    viewer_headers = {"Authorization": f"Bearer {tokens['viewer']['access_token']}"}
    response = client.get("/api/v1/auth/admin-only", headers=viewer_headers)
    assert response.status_code == 403
    
    # 9. Test RBAC: Admin-Only endpoint accessed Unauthenticated (401 Unauthorized)
    response = client.get("/api/v1/auth/admin-only")
    assert response.status_code == 401

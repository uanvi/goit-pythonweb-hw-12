import pytest
from fastapi import status

class TestAuthAPI:
    """Test authentication API endpoints."""
    
    def test_register_user_success(self, client, test_user_data):
        """Test successful user registration."""
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert data["is_verified"] is False
        assert "id" in data

    def test_register_user_duplicate_email(self, client, test_user_data):
        """Test registration with duplicate email."""
        # First registration
        client.post("/auth/register", json=test_user_data)
        
        # Second registration with same email
        response = client.post("/auth/register", json=test_user_data)
        
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]

    def test_login_success(self, client, test_user_data):
        """Test successful login."""
        # Register user first
        client.post("/auth/register", json=test_user_data)
        
        # Login
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user_data):
        """Test login with wrong password."""
        # Register user first
        client.post("/auth/register", json=test_user_data)
        
        # Login with wrong password
        login_data = {
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "somepassword"
        }
        response = client.post("/auth/login", json=login_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, client, authenticated_user):
        """Test getting current user info."""
        response = client.get("/auth/me", headers=authenticated_user["headers"])
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "username" in data
        assert "email" in data
        assert "id" in data

    def test_get_current_user_no_token(self, client):
        """Test getting current user without token."""
        response = client.get("/auth/me")
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_verify_email(self, client, test_user_data):
        """Test email verification."""
        # Register user
        response = client.post("/auth/register", json=test_user_data)
        user_id = response.json()["id"]
        
        # Verify email
        response = client.post(f"/auth/verify/{user_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "verified" in response.json()["message"]

    def test_verify_email_nonexistent_user(self, client):
        """Test verifying non-existent user."""
        response = client.post("/auth/verify/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
import pytest
from src.core.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    verify_token
)
from fastapi import HTTPException

class TestPasswordHashing:
    """Test password hashing functions."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert len(hashed) > 20
        assert hashed.startswith("$2b$")

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with wrong password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False

class TestJWTTokens:
    """Test JWT token functions."""
    
    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 20
        assert token.count(".") == 2  # JWT has 3 parts

    def test_verify_token_valid(self):
        """Test token verification with valid token."""
        email = "test@example.com"
        data = {"sub": email}
        token = create_access_token(data)
        
        decoded_email = verify_token(token)
        assert decoded_email == email

    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        invalid_token = "invalid.jwt.token"
        
        with pytest.raises(HTTPException) as exc:
            verify_token(invalid_token)
        assert exc.value.status_code == 401

    def test_verify_token_no_subject(self):
        """Test token verification with no subject."""
        data = {"user": "test@example.com"}  # Wrong key
        token = create_access_token(data)
        
        with pytest.raises(HTTPException) as exc:
            verify_token(token)
        assert exc.value.status_code == 401
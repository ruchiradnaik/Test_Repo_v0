"""
Authentication utilities for user authentication and authorization.
"""
import hashlib
import secrets
from user_service import UserService
from typing import Optional, Tuple

class AuthManager:
    """Manages user authentication and token generation."""
    
    def __init__(self):
        """Initialize the authentication manager."""
        self.user_service = UserService()
        self.tokens = {}  # In-memory token storage (use Redis in production)
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using SHA-256.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password
            hashed: Hashed password to compare against
            
        Returns:
            True if password matches, False otherwise
        """
        return self.hash_password(password) == hashed
    
    def generate_token(self) -> str:
        """
        Generate a secure random token.
        
        Returns:
            Random token string
        """
        return secrets.token_urlsafe(32)
    
    def login(self, username: str, password: str) -> Optional[Tuple[str, dict]]:
        """
        Authenticate a user and generate a token.
        
        Args:
            username: User's username
            password: User's password
            
        Returns:
            Tuple of (token, user_data) if successful, None otherwise
        """
        user = self.user_service.get_user_by_username(username)
        if not user:
            return None
        
        # In a real app, you'd verify the password hash stored in the database
        # For this example, we'll just check if user exists
        token = self.generate_token()
        self.tokens[token] = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }
        
        return (token, self.tokens[token])
    
    def validate_token(self, token: str) -> Optional[dict]:
        """
        Validate a token and return user data.
        
        Args:
            token: Authentication token
            
        Returns:
            User data dictionary if token is valid, None otherwise
        """
        return self.tokens.get(token)
    
    def logout(self, token: str) -> bool:
        """
        Invalidate a token (logout).
        
        Args:
            token: Authentication token to invalidate
            
        Returns:
            True if token was found and removed, False otherwise
        """
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False

# CodeSentinal: created for you by RuchirAdnaik.
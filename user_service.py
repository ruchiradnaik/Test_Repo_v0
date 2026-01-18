"""
User service for managing user operations.
"""
from database import db_manager, User
from typing import Optional, List

class UserService:
    """Service class for user-related operations."""
    
    def __init__(self):
        """Initialize the user service with database connection."""
        self.db = db_manager
    
    def create_user(self, username: str, email: str) -> User:
        """
        Create a new user.
        
        Args:
            username: Username for the new user
            email: Email address for the new user
            
        Returns:
            Created User object
        """
        session = self.db.get_session()
        try:
            # Check if user already exists
            existing_user = session.query(User).filter(User.username == username).first()
            if existing_user:
                raise ValueError(f"User with username '{username}' already exists")
            
            new_user = User(username=username, email=email)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.
        
        Args:
            user_id: The user's ID
            
        Returns:
            User object if found, None otherwise
        """
        session = self.db.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            return user
        finally:
            session.close()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by their username.
        
        Args:
            username: The user's username
            
        Returns:
            User object if found, None otherwise
        """
        session = self.db.get_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            return user
        finally:
            session.close()
    
    def list_all_users(self) -> List[User]:
        """
        Get all users from the database.
        
        Returns:
            List of all User objects
        """
        session = self.db.get_session()
        try:
            users = session.query(User).all()
            return users
        finally:
            session.close()
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by their ID.
        
        Args:
            user_id: The user's ID
            
        Returns:
            True if user was deleted, False if not found
        """
        session = self.db.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

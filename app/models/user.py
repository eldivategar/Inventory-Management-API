import sqlite3
import os
import hashlib
from app.database.connection import get_db_connection

class User:
    def __init__(self, username=None, password=None) -> None:
        self.username = username
        self.password = password
        
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password with salt using hashlib.
        """
        # Generate a random salt
        salt = os.urandom(16)
        # Hash the password with salt using SHA-256
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        # Store the salt and password hash as a single value
        return salt.hex() + password_hash.hex()

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """
        Verify if provided password matches the stored hashed password.
        """
        # Extract the salt from the stored password
        salt = bytes.fromhex(stored_password[:32])
        stored_hash = stored_password[32:]
        
        # Hash the provided password using the same salt
        provided_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000).hex()
        
        # Compare the stored hash with the provided hash
        return stored_hash == provided_hash
        
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT username, password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return User(username=user['username'], password=user['password'])
        return None

    @staticmethod
    def create(username, password):
        if not username or not password:
            raise ValueError("Username and password are required")
        
        # Hash the password before storing
        hashed_password = User.hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return User(username=username, password=hashed_password)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise ValueError(f"User with username '{username}' already exists")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def authenticate(username, password):
        """
        Authenticate a user by verifying the username and password.
        """
        user = User.get_by_username(username)
        if user and User.verify_password(user.password, password):
            return True
        return False
    
    def to_dict(self):
        return {
            'username': self.username
        }
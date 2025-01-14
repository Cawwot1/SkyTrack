import hashlib
import secrets
from asyncio import *

class User():
    def __init__(self, email, first_name, last_name, password_input):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.__hash_password(password_input)
        self.session_token = self.generate_token()[0]
        self.csrf_token = self.generate_token()[1]
    
    def __hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode('ascii')).hexdigest()
        return hashed_password

    def generate_token(self):
        """Generate a cryptographically secure session token, and CSRF token
        
        Returns: (session_token, csrf token)
        """
        session_token = secrets.token_hex(16)
        csrf_token = hashlib.sha256(session_token.encode()).hexdigest()
        return session_token, csrf_token
    
    def assign_tokens(self):
        """Generates tokens and assigns them as parameters."""
        self.session_token = self.generate_token()[0]
        self.csrf_token = self.generate_token()[1]

    async def revoke_tokens(self):
        """Removes session token and CSRF token"""
        self.session_token = None
        self.csrf_token = None

    async def verify_password(self, password_input):
        """Check that provided password matches stored password hash"""
        return (self.password_hash == self.__hash_password(password_input))
    
    async def validate_tokens(self, session_token, csrf_token):
        """Checks if both tokens match stored tokens"""
        return (await self.validate_session_token(session_token) 
                and await self.validate_csrf_token(csrf_token))

    async def validate_session_token(self, session_token_input):
        """Checks if the provided session token matches the stored session token"""
        return (session_token_input == self.session_token)
    
    async def validate_csrf_token(self, csrf_token_input):
        """Checks if the provided CSRF token matches the stored CSRF token""" 
        return (csrf_token_input == self.csrf_token)
        
    async def user_data(self): 
        """Returns dictionary containing user data"""
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
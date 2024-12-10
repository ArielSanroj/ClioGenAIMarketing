import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional 
import streamlit as st
from passlib.context import CryptContext
from jose import JWTError, jwt
import secrets
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.session_manager import clear_user_session, initialize_user_session

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db_connection():
    """Get database connection using environment variables"""
    return psycopg2.connect(
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"]
    )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def register_user(email: str, password: str, name: str, surname: str, 
                 cellphone: str, purpose: str) -> Dict:
    """Register a new user"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Check if user exists
                cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                if cur.fetchone():
                    return {"error": "User already exists"}
                
                # Insert new user
                cur.execute("""
                    INSERT INTO users (email, password_hash, name, surname, 
                                     cellphone, purpose)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id, email
                """, (email, get_password_hash(password), name, surname, 
                      cellphone, purpose))
                user = cur.fetchone()
                conn.commit()
                
                # Create access token
                access_token = create_access_token(
                    data={"sub": user["email"]},
                    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                )

                # Initialize user session state
                initialize_user_session(str(user["id"]))
                
                return {
                    "message": "Registration successful",
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_id": user["id"],
                    "email": user["email"]
                }
                
    except Exception as e:
        return {"error": str(e)}

def authenticate_user(email: str, password: str) -> Dict:
    """Authenticate user and create access token"""
    try:
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, email, password_hash 
                    FROM users WHERE email = %s
                """, (email,))
                user = cur.fetchone()
                
                if not user:
                    return {"error": "Invalid credentials"}
                
                if not verify_password(password, user["password_hash"]):
                    return {"error": "Invalid credentials"}
                
                # Create access token
                access_token = create_access_token(
                    data={"sub": user["email"]},
                    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                )
                
                # Update last login
                cur.execute("""
                    UPDATE users 
                    SET last_login = CURRENT_TIMESTAMP 
                    WHERE id = %s
                """, (user["id"],))
                conn.commit()

                # Initialize user session state
                initialize_user_session(str(user["id"]))
                
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user_id": user["id"],
                    "email": user["email"]
                }
                
    except Exception as e:
        return {"error": str(e)}

def logout_user():
    """Logout current user and clear their session state"""
    if "user_id" in st.session_state:
        user_id = st.session_state.user_id
        clear_user_session(str(user_id))
        del st.session_state.user_id
        del st.session_state.user_email
        if "access_token" in st.session_state:
            del st.session_state.access_token

def is_authenticated() -> bool:
    """Check if user is authenticated in current session"""
    return bool(st.session_state.get("user_id"))

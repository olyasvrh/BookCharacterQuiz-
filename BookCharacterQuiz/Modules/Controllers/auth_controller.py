from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["Auth"])

users_db = {}


@router.post("/register")
async def register(username: str, email: str, password: str):
    
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user_id = len(users_db) + 1
    users_db[username] = {
        'id': user_id,
        'username': username,
        'email': email,
        'password': password,
        'created_at': datetime.now().isoformat(),
        'quiz_history': [],
        'favourites': []
    }
    
    return {
        'success': True,
        'user': {
            'id': user_id,
            'username': username,
            'email': email
        }
    }


@router.post("/login")
async def login(username: str, password: str):
    
    user = users_db.get(username)
    if not user or user['password'] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = f"token_{user['id']}_{datetime.now().timestamp()}"
    
    return {
        'success': True,
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }
    }


@router.get("/me")
async def get_current_user(token: str):

    for user in users_db.values():
        if f"token_{user['id']}" in token:
            return {
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
            }
    
    raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/logout")
async def logout(token: str):
    
    return {
        'success': True,
        'message': 'Logged out successfully'
    }
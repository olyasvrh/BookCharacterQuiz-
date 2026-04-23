"""
Контролер для обраного
Ендпоінти: /api/favourites
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/api/favourites", tags=["Favourites"])

# Тимчасове сховище обраного
favourites_db: Dict[int, List[Dict]] = {}


@router.get("/{user_id}")
async def get_favourites(user_id: int):
    """Отримати всі обрані елементи користувача"""
    
    user_favourites = favourites_db.get(user_id, [])
    
    return {
        'success': True,
        'favourites': user_favourites,
        'count': len(user_favourites)
    }


@router.post("/add")
async def add_favourite(user_id: int, item_type: str, item_id: int, item_data: Dict = None):
    """Додати в обране"""
    
    if user_id not in favourites_db:
        favourites_db[user_id] = []
    
    # Перевірка чи вже є в обраному
    existing = next(
        (item for item in favourites_db[user_id] 
         if item['item_type'] == item_type and item['item_id'] == item_id),
        None
    )
    
    if existing:
        raise HTTPException(status_code=400, detail="Item already in favourites")
    
    favourite_item = {
        'item_type': item_type,  # 'book', 'character', 'quiz'
        'item_id': item_id,
        'added_at': datetime.now().isoformat(),
        'item_data': item_data or {}
    }
    
    favourites_db[user_id].append(favourite_item)
    
    return {
        'success': True,
        'favourite': favourite_item
    }


@router.delete("/remove")
async def remove_favourite(user_id: int, item_type: str, item_id: int):
    """Видалити з обраного"""
    
    if user_id not in favourites_db:
        raise HTTPException(status_code=404, detail="No favourites found")
    
    initial_length = len(favourites_db[user_id])
    favourites_db[user_id] = [
        item for item in favourites_db[user_id]
        if not (item['item_type'] == item_type and item['item_id'] == item_id)
    ]
    
    if len(favourites_db[user_id]) == initial_length:
        raise HTTPException(status_code=404, detail="Item not found in favourites")
    
    return {
        'success': True,
        'message': 'Removed from favourites'
    }


@router.get("/check/{user_id}")
async def check_favourite(user_id: int, item_type: str, item_id: int):
    """Перевірити чи елемент в обраному"""
    
    user_favourites = favourites_db.get(user_id, [])
    is_favourite = any(
        item['item_type'] == item_type and item['item_id'] == item_id
        for item in user_favourites
    )
    
    return {
        'success': True,
        'is_favourite': is_favourite
    }
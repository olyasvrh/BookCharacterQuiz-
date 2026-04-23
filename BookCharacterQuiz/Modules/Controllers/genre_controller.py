"""
Контролер для жанрів книг
Ендпоінти: /api/genres
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/api/genres", tags=["Genres"])

# Приклад даних
genres_db = [
    {'id': 1, 'name': 'Фентезі', 'description': 'Магія, міфічні істоти, фантастичні світи'},
    {'id': 2, 'name': 'Пригоди', 'description': 'Подорожі, пошуки скарбів, небезпечні місії'},
    {'id': 3, 'name': 'Детектив', 'description': 'Розслідування, загадки, злочини'},
    {'id': 4, 'name': 'Роман', 'description': 'Любов, стосунки, емоції'},
    {'id': 5, 'name': 'Наукова фантастика', 'description': 'Технології, космос, майбутнє'},
    {'id': 6, 'name': 'Філософія', 'description': 'Роздуми, сенс життя, мудрість'},
    {'id': 7, 'name': 'Сімейна сага', 'description': 'Родина, покоління, традиції'}
]


@router.get("/")
async def get_all_genres():
    """Отримати всі жанри"""
    
    return {
        'success': True,
        'genres': genres_db,
        'count': len(genres_db)
    }


@router.get("/{genre_id}")
async def get_genre(genre_id: int):
    """Отримати жанр за ID"""
    
    genre = next((g for g in genres_db if g['id'] == genre_id), None)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    return {
        'success': True,
        'genre': genre
    }


@router.get("/books/{genre_id}")
async def get_books_by_genre(genre_id: int):
    """Отримати книги за жанром"""
    
    # Перевіряємо чи існує жанр
    genre = next((g for g in genres_db if g['id'] == genre_id), None)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    # В реальному проекті тут буде запит до БД
    books = [
        {'id': 1, 'title': 'Приклад книги', 'author': 'Автор'}
    ]
    
    return {
        'success': True,
        'genre': genre,
        'books': books,
        'count': len(books)
    }


@router.get("/recommend/{genre_id}")
async def recommend_books(genre_id: int, limit: int = 5):
    """Рекомендація книг за жанром"""
    
    genre = next((g for g in genres_db if g['id'] == genre_id), None)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    # В реальному проекті тут буде алгоритм рекомендацій
    recommendations = []
    
    return {
        'success': True,
        'genre': genre,
        'recommendations': recommendations[:limit]
    }
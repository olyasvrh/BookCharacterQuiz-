"""
Контролер для AI-функцій
Ендпоінти: /api/ai
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
import random

router = APIRouter(prefix="/api/ai", tags=["AI"])


@router.post("/recommend-books")
async def recommend_books(
    user_id: int,
    character_id: int = None,
    genre_ids: List[int] = None,
    limit: int = 5
):
    """AI-рекомендація книг на основі персонажа або жанрів"""
    
    recommendations = []
    
    # Якщо є персонаж, рекомендуємо книги з його світу
    if character_id:
        character_books = {
            1: ['Володар перснів', 'Хоббіт', 'Сильмариліон'],
            2: ['Володар перснів', 'Діти Гуріна'],
            3: ['Володар перснів', 'Незакінчені сказання'],
            4: ['Гаррі Поттер і філософський камінь', 'Гаррі Поттер і таємна кімната']
        }
        
        books = character_books.get(character_id, [])
        recommendations = [
            {'title': book, 'reason': f'Схоже на твого персонажа!'}
            for book in books[:limit]
        ]
    
    # Якщо є жанри, додаємо рекомендації за жанрами
    if genre_ids:
        genre_books = {
            1: ['Володар перснів', 'Хроніки Нарнії', 'Гра престолів'],
            2: ['Острів скарбів', 'Подорож до центру Землі'],
            3: ['Шерлок Холмс', 'Вбивство в Східному експресі']
        }
        
        for genre_id in genre_ids:
            if genre_id in genre_books:
                for book in genre_books[genre_id][:limit]:
                    recommendations.append({
                        'title': book,
                        'reason': 'Рекомендовано за жанром'
                    })
    
    # Якщо немає рекомендацій, даємо випадкові
    if not recommendations:
        default_books = [
            'Майстер і Маргарита',
            'Злочин і кара',
            '1984',
            'Мандри Гуллівера',
            'Аліса в Країні Чудес'
        ]
        
        recommendations = [
            {'title': book, 'reason': 'Вам може сподобатися!'}
            for book in random.sample(default_books, min(limit, len(default_books)))
        ]
    
    return {
        'success': True,
        'recommendations': recommendations[:limit],
        'based_on': {
            'character_id': character_id,
            'genre_ids': genre_ids
        }
    }


@router.post("/generate-quiz")
async def generate_quiz(
    book_title: str = None,
    genre: str = None,
    num_questions: int = 5
):
    """AI-генерація тесту на основі книги або жанру"""
    
    if not book_title and not genre:
        raise HTTPException(
            status_code=400,
            detail="Either book_title or genre is required"
        )
    
    # Генеруємо питання на основі вхідних даних
    questions = []
    
    if book_title:
        # Генерація питань про конкретну книгу
        questions = [
            {
                'id': i + 1,
                'text': f'Питання {i + 1} про книгу "{book_title}"',
                'answers': [
                    {'id': 1, 'text': 'Варіант A'},
                    {'id': 2, 'text': 'Варіант B'},
                    {'id': 3, 'text': 'Варіант C'},
                    {'id': 4, 'text': 'Варіант D'}
                ]
            }
            for i in range(num_questions)
        ]
    
    return {
        'success': True,
        'quiz': {
            'title': f'Тест: {book_title or genre}',
            'description': f'Перевір свої знання про {book_title or genre}!',
            'total_questions': num_questions,
            'questions': questions
        }
    }


@router.post("/analyze-result")
async def analyze_result(session_id: str):
    """AI-аналіз результатів тесту"""
    
    # В реальному проекті тут буде аналіз відповідей
    
    analysis = {
        'strengths': [
            'Добре розумієш мотивацію персонажів',
            'Відчуваєш емоційний зв\'язок з героями'
        ],
        'weaknesses': [
            'Можеш краще запам\'ятовувати другорядних персонажів'
        ],
        'recommendations': [
            'Прочитай більше книг цього жанру',
            'Спробуй інші тести для розширення кругозору'
        ],
        'matching_characters': [
            {'name': 'Гендальф', 'match_percentage': 85},
            {'name': 'Арагорн', 'match_percentage': 72}
        ]
    }
    
    return {
        'success': True,
        'analysis': analysis
    }


@router.post("/chat")
async def chat_with_character(
    character_id: int,
    message: str,
    session_id: str = None
):
    """Чат з AI-персонажем"""
    
    # Отримуємо персонажа
    characters = {
        1: {'name': 'Гендальф', 'style': 'мудрий, розважливий, говорить загадками'},
        2: {'name': 'Арагорн', 'style': 'сміливий, благородний, прямий'},
        3: {'name': 'Сем', 'style': 'добрий, вірний, простий'},
        4: {'name': 'Ерміона', 'style': 'розумна, чітка, фактологічна'}
    }
    
    character = characters.get(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Генерація відповіді (спрощена)
    responses = {
        'Гендальф': 'Мудрість приходить з часом, друже. Не поспішай.',
        'Арагорн': 'Честь і відвага ведуть нас вперед. Що ти обереш?',
        'Сем': 'Я завжди поруч з друзями. Розкажи, що сталося?',
        'Ерміона': 'Цікаве питання! Давай розберемося логічно.'
    }
    
    reply = responses.get(character['name'], 'Розкажи більше про це.')
    
    return {
        'success': True,
        'character': character['name'],
        'message': message,
        'reply': reply
    }
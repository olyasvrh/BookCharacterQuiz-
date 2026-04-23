"""
Контролер для соціальних функцій
Ендпоінти: /api/social
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Dict, Any

router = APIRouter(prefix="/api/social", tags=["Social"])

# Тимчасові сховища
posts_db = []
comments_db = []
likes_db = {}


@router.get("/posts")
async def get_posts(limit: int = 20, offset: int = 0):
    """Отримати стрічку постів"""
    
    posts = sorted(posts_db, key=lambda x: x['created_at'], reverse=True)
    paginated = posts[offset:offset + limit]
    
    return {
        'success': True,
        'posts': paginated,
        'total': len(posts),
        'limit': limit,
        'offset': offset
    }


@router.post("/posts")
async def create_post(user_id: int, content: str, quiz_result_id: int = None):
    """Створити пост про результат тесту"""
    
    post = {
        'id': len(posts_db) + 1,
        'user_id': user_id,
        'content': content,
        'quiz_result_id': quiz_result_id,
        'created_at': datetime.now().isoformat(),
        'likes': 0,
        'comments': []
    }
    
    posts_db.append(post)
    
    return {
        'success': True,
        'post': post
    }


@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    """Отримати пост за ID"""
    
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return {
        'success': True,
        'post': post
    }


@router.post("/posts/{post_id}/like")
async def like_post(post_id: int, user_id: int):
    """Лайкнути пост"""
    
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Перевірка чи вже лайкнув
    if likes_db.get(post_id, {}).get(user_id):
        raise HTTPException(status_code=400, detail="Already liked")
    
    if post_id not in likes_db:
        likes_db[post_id] = {}
    
    likes_db[post_id][user_id] = True
    post['likes'] = len(likes_db[post_id])
    
    return {
        'success': True,
        'likes': post['likes']
    }


@router.post("/posts/{post_id}/comment")
async def add_comment(post_id: int, user_id: int, text: str):
    """Додати коментар до посту"""
    
    post = next((p for p in posts_db if p['id'] == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = {
        'id': len(comments_db) + 1,
        'post_id': post_id,
        'user_id': user_id,
        'text': text,
        'created_at': datetime.now().isoformat()
    }
    
    comments_db.append(comment)
    
    if 'comments' not in post:
        post['comments'] = []
    post['comments'].append(comment)
    
    return {
        'success': True,
        'comment': comment
    }


@router.get("/posts/{post_id}/comments")
async def get_comments(post_id: int):
    """Отримати коментарі до посту"""
    
    post_comments = [c for c in comments_db if c['post_id'] == post_id]
    
    return {
        'success': True,
        'comments': post_comments,
        'count': len(post_comments)
    }


@router.post("/share-result")
async def share_quiz_result(user_id: int, session_id: str, visibility: str = "public"):
    """Поділитися результатом тесту"""
    
    # В реальному проекті тут буде отримання результату з БД
    share_link = f"/share/{session_id}"
    
    return {
        'success': True,
        'share_link': share_link,
        'visibility': visibility
    }
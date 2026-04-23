from pydantic import BaseModel
from typing import List, Optional, Dict

# --- Auth View Models ---
class UserRegisterVM(BaseModel):
    username: str
    email: str
    password: str

class UserLoginVM(BaseModel):
    email: str
    password: str

# --- Quiz View Models (Справжній тест) ---
class AnswerVM(BaseModel):
    question_id: int
    point: int  # Бали за відповідь (напр. 1, 2 або 5)

class QuizSubmitVM(BaseModel):
    user_id: int
    quiz_id: int
    answers: List[AnswerVM]

# --- AI & Analytics View Models ---
class AIAnalysisRequestVM(BaseModel):
    text_content: str  # Для аналізу психотипу або емоцій

class AIComparisonVM(BaseModel):
    first_char_id: int
    second_char_id: int

# --- Social & Favourites View Models ---
class CommentVM(BaseModel):
    user_id: int
    post_id: int
    text: str

class ShareRequestVM(BaseModel):
    result_id: int
    platform_name: str  # "instagram", "telegram" тощо
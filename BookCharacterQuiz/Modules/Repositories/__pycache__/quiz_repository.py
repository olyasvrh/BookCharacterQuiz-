import uuid
from typing import Dict, List, Optional
from Modules.database.db import execute_query, execute_update


class QuizRepository:
    
    @staticmethod
    def get_quiz_by_id(quiz_id: int) -> Optional[Dict]:
        result = execute_query("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_questions_by_quiz(quiz_id: int) -> List[Dict]:
        return execute_query("SELECT * FROM questions WHERE quiz_id = ? ORDER BY order_num", (quiz_id,))
    
    @staticmethod
    def get_question_with_answers(question_id: int) -> Optional[Dict]:
        question_result = execute_query("SELECT * FROM questions WHERE id = ?", (question_id,))
        if not question_result:
            return None
        question = dict(question_result[0])
        answers = execute_query("SELECT * FROM answers WHERE question_id = ?", (question_id,))
        question['answers'] = [dict(a) for a in answers]
        return question
    
    @staticmethod
    def get_answer_by_id(answer_id: int) -> Optional[Dict]:
        result = execute_query("SELECT * FROM answers WHERE id = ?", (answer_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_character_by_id(character_id: int) -> Optional[Dict]:
        result = execute_query("SELECT * FROM characters WHERE id = ?", (character_id,))
        return result[0] if result else None
    
    @staticmethod
    def create_session(user_id: int, quiz_id: int) -> str:
        session_id = f"session_{uuid.uuid4().hex[:8]}"
        execute_update(
            "INSERT INTO quiz_sessions (id, user_id, quiz_id) VALUES (?, ?, ?)",
            (session_id, user_id, quiz_id)
        )
        return session_id
    
    @staticmethod
    def get_session(session_id: str) -> Optional[Dict]:
        result = execute_query("SELECT * FROM quiz_sessions WHERE id = ?", (session_id,))
        return result[0] if result else None
    
    @staticmethod
    def complete_session(session_id: str) -> None:
        execute_update("UPDATE quiz_sessions SET status = 'completed' WHERE id = ?", (session_id,))
    
    @staticmethod
    def save_answer(session_id: str, question_id: int, answer_id: int, character_id: int, score: int) -> None:
        execute_update(
            "INSERT INTO user_answers (session_id, question_id, answer_id, character_id, score) VALUES (?, ?, ?, ?, ?)",
            (session_id, question_id, answer_id, character_id, score)
        )
    
    @staticmethod
    def get_user_answers(session_id: str) -> List[Dict]:
        return execute_query("SELECT * FROM user_answers WHERE session_id = ?", (session_id,))
    
    @staticmethod
    def get_answered_count(session_id: str) -> int:
        result = execute_query("SELECT COUNT(*) as count FROM user_answers WHERE session_id = ?", (session_id,))
        return result[0]['count'] if result else 0
    
    @staticmethod
    def get_answered_question_ids(session_id: str) -> List[int]:
        result = execute_query("SELECT question_id FROM user_answers WHERE session_id = ?", (session_id,))
        return [row['question_id'] for row in result]
    
    @staticmethod
    def save_result(session_id: str, user_id: int, character_id: int, total_score: int, percentage: float) -> None:
        execute_update(
            "INSERT INTO results (session_id, user_id, character_id, total_score, percentage) VALUES (?, ?, ?, ?, ?)",
            (session_id, user_id, character_id, total_score, percentage)
        )
    
    @staticmethod
    def get_result(session_id: str) -> Optional[Dict]:
        result = execute_query(
            "SELECT r.*, c.name as character_name, c.description, c.quote FROM results r JOIN characters c ON r.character_id = c.id WHERE r.session_id = ?",
            (session_id,)
        )
        return result[0] if result else None
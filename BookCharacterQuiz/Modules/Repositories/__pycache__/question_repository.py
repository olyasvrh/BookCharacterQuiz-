from typing import Dict, List, Optional
from Modules.database.db import execute_query, execute_update


class QuestionRepository:
    
    @staticmethod
    def get_question_by_id(question_id: int) -> Optional[Dict]:
        result = execute_query("SELECT * FROM questions WHERE id = ?", (question_id,))
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
    def create_question(quiz_id: int, text: str, order_num: int = 0) -> int:
        return execute_update(
            "INSERT INTO questions (quiz_id, text, order_num) VALUES (?, ?, ?)",
            (quiz_id, text, order_num)
        )
    
    @staticmethod
    def update_question(question_id: int, text: str = None, order_num: int = None) -> None:
        if text is not None:
            execute_update("UPDATE questions SET text = ? WHERE id = ?", (text, question_id))
        if order_num is not None:
            execute_update("UPDATE questions SET order_num = ? WHERE id = ?", (order_num, question_id))
    
    @staticmethod
    def delete_question(question_id: int) -> None:
        execute_update("DELETE FROM questions WHERE id = ?", (question_id,))
    
    @staticmethod
    def get_total_questions(quiz_id: int) -> int:
        result = execute_query("SELECT COUNT(*) as count FROM questions WHERE quiz_id = ?", (quiz_id,))
        return result[0]['count'] if result else 0


class AnswerRepository:
    
    @staticmethod
    def get_answer_by_id(answer_id: int) -> Optional[Dict]:
        result = execute_query("SELECT * FROM answers WHERE id = ?", (answer_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_answers_by_question(question_id: int) -> List[Dict]:
        return execute_query("SELECT * FROM answers WHERE question_id = ?", (question_id,))
    
    @staticmethod
    def create_answer(question_id: int, text: str, character_id: int = None, score: int = 0) -> int:
        return execute_update(
            "INSERT INTO answers (question_id, text, character_id, score) VALUES (?, ?, ?, ?)",
            (question_id, text, character_id, score)
        )
    
    @staticmethod
    def update_answer(answer_id: int, text: str = None, character_id: int = None, score: int = None) -> None:
        if text is not None:
            execute_update("UPDATE answers SET text = ? WHERE id = ?", (text, answer_id))
        if character_id is not None:
            execute_update("UPDATE answers SET character_id = ? WHERE id = ?", (character_id, answer_id))
        if score is not None:
            execute_update("UPDATE answers SET score = ? WHERE id = ?", (score, answer_id))
    
    @staticmethod
    def delete_answer(answer_id: int) -> None:
        execute_update("DELETE FROM answers WHERE id = ?", (answer_id,))
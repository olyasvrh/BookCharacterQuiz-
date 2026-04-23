from typing import Dict, List, Optional
from Modules.database.db import execute_query, execute_update


class ResultRepository:
    
    @staticmethod
    def save_result(session_id: str, user_id: int, character_id: int, total_score: int, percentage: float) -> None:
        execute_update(
            "INSERT INTO results (session_id, user_id, character_id, total_score, percentage) VALUES (?, ?, ?, ?, ?)",
            (session_id, user_id, character_id, total_score, percentage)
        )
    
    @staticmethod
    def get_result_by_session(session_id: str) -> Optional[Dict]:
        result = execute_query(
            "SELECT r.*, c.name as character_name, c.description, c.quote FROM results r JOIN characters c ON r.character_id = c.id WHERE r.session_id = ?",
            (session_id,)
        )
        return result[0] if result else None
    
    @staticmethod
    def get_results_by_user(user_id: int, limit: int = 10) -> List[Dict]:
        results = execute_query(
            "SELECT r.*, c.name as character_name FROM results r JOIN characters c ON r.character_id = c.id WHERE r.user_id = ? ORDER BY r.created_at DESC LIMIT ?",
            (user_id, limit)
        )
        return results
    
    @staticmethod
    def get_results_by_character(character_id: int, limit: int = 50) -> List[Dict]:
        results = execute_query(
            "SELECT * FROM results WHERE character_id = ? ORDER BY created_at DESC LIMIT ?",
            (character_id, limit)
        )
        return results
    
    @staticmethod
    def get_average_score_by_character(character_id: int) -> float:
        result = execute_query(
            "SELECT AVG(percentage) as avg_percentage FROM results WHERE character_id = ?",
            (character_id,)
        )
        return result[0]['avg_percentage'] if result and result[0]['avg_percentage'] else 0.0
    
    @staticmethod
    def get_total_quiz_count() -> int:
        result = execute_query("SELECT COUNT(*) as count FROM results")
        return result[0]['count'] if result else 0
    
    @staticmethod
    def delete_result(result_id: int) -> None:
        execute_update("DELETE FROM results WHERE id = ?", (result_id,))
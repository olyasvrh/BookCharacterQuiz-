from typing import Dict, List, Optional
from Modules.database.db import execute_query, execute_update


class CharacterRepository:
    
    @staticmethod
    def get_character_by_id(character_id: int) -> Optional[Dict]:
        result = execute_query("SELECT * FROM characters WHERE id = ?", (character_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_character_by_name(name: str) -> Optional[Dict]:
        result = execute_query("SELECT * FROM characters WHERE name = ?", (name,))
        return result[0] if result else None
    
    @staticmethod
    def get_all_characters() -> List[Dict]:
        return execute_query("SELECT * FROM characters")
    
    @staticmethod
    def get_characters_by_book(book_title: str) -> List[Dict]:
        return execute_query("SELECT * FROM characters WHERE book_title = ?", (book_title,))
    
    @staticmethod
    def create_character(name: str, book_title: str, description: str = None, quote: str = None) -> int:
        return execute_update(
            "INSERT INTO characters (name, book_title, description, quote) VALUES (?, ?, ?, ?)",
            (name, book_title, description, quote)
        )
    
    @staticmethod
    def update_character(character_id: int, name: str = None, book_title: str = None, description: str = None, quote: str = None) -> None:
        if name is not None:
            execute_update("UPDATE characters SET name = ? WHERE id = ?", (name, character_id))
        if book_title is not None:
            execute_update("UPDATE characters SET book_title = ? WHERE id = ?", (book_title, character_id))
        if description is not None:
            execute_update("UPDATE characters SET description = ? WHERE id = ?", (description, character_id))
        if quote is not None:
            execute_update("UPDATE characters SET quote = ? WHERE id = ?", (quote, character_id))
    
    @staticmethod
    def delete_character(character_id: int) -> None:
        execute_update("DELETE FROM characters WHERE id = ?", (character_id,))
    
    @staticmethod
    def search_characters(search_term: str) -> List[Dict]:
        return execute_query(
            "SELECT * FROM characters WHERE name LIKE ? OR book_title LIKE ?",
            (f"%{search_term}%", f"%{search_term}%")
        )
    
    @staticmethod
    def get_popular_characters(limit: int = 5) -> List[Dict]:
        results = execute_query(
            "SELECT c.id, c.name, c.book_title, COUNT(r.id) as result_count FROM characters c LEFT JOIN results r ON c.id = r.character_id GROUP BY c.id ORDER BY result_count DESC LIMIT ?",
            (limit,)
        )
        return results
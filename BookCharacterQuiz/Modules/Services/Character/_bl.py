from typing import Dict, List, Optional
from Modules.Repositories import CharacterRepository


class CharacterValidator:
    @staticmethod
    def validate_character_data(name: str, book_title: str) -> Optional[str]:
        if not name:
            return 'Character name is required'
        if not book_title:
            return 'Book title is required'
        return None

    @staticmethod
    def validate_character_id(character_id: int) -> Optional[str]:
        if not character_id:
            return 'Character ID is required'
        return None


class CharacterConverter:
    @staticmethod
    def to_dto(character: Dict) -> Dict:
        if not character:
            return None
        return {
            'id': character.get('id'),
            'name': character.get('name'),
            'book_title': character.get('book_title'),
            'description': character.get('description'),
            'quote': character.get('quote')
        }

    @staticmethod
    def to_list_response(characters: List[Dict]) -> List[Dict]:
        return [CharacterConverter.to_dto(c) for c in characters]

    @staticmethod
    def to_popular_response(character: Dict, result_count: int) -> Dict:
        return {
            'id': character.get('id'),
            'name': character.get('name'),
            'book_title': character.get('book_title'),
            'result_count': result_count
        }


class CharacterHelper:
    @staticmethod
    def get_character_description(character: Dict) -> str:
        if not character:
            return "Персонажа не знайдено"
        return f"{character.get('name')} - {character.get('description', 'Опис відсутній')}"

    @staticmethod
    def format_quote(character: Dict) -> str:
        if not character or not character.get('quote'):
            return "Немає цитати"
        return f"«{character.get('quote')}» — {character.get('name')}"


class CharacterNotifier:
    @staticmethod
    def notify_character_created(name: str):
        print(f"[NOTIFY] Створено нового персонажа: {name}")

    @staticmethod
    def notify_character_deleted(name: str):
        print(f"[NOTIFY] Видалено персонажа: {name}")

    @staticmethod
    def notify_characters_fetched(count: int):
        print(f"[NOTIFY] Отримано {count} персонажів з бази даних")


class CharacterService:
    @staticmethod
    def get_all_characters() -> Dict:
        characters = CharacterRepository.get_all_characters()
        CharacterNotifier.notify_characters_fetched(len(characters))

        return {
            'success': True,
            'characters': CharacterConverter.to_list_response(characters),
            'count': len(characters)
        }

    @staticmethod
    def get_character_by_id(character_id: int) -> Dict:
        error = CharacterValidator.validate_character_id(character_id)
        if error:
            return {'success': False, 'error': error}

        character = CharacterRepository.get_character_by_id(character_id)
        if not character:
            return {'success': False, 'error': 'Character not found'}

        return {
            'success': True,
            'character': CharacterConverter.to_dto(character)
        }

    @staticmethod
    def get_character_by_name(name: str) -> Dict:
        if not name:
            return {'success': False, 'error': 'Name is required'}

        character = CharacterRepository.get_character_by_name(name)
        if not character:
            return {'success': False, 'error': 'Character not found'}

        return {
            'success': True,
            'character': CharacterConverter.to_dto(character)
        }

    @staticmethod
    def get_characters_by_book(book_title: str) -> Dict:
        if not book_title:
            return {'success': False, 'error': 'Book title is required'}

        characters = CharacterRepository.get_characters_by_book(book_title)

        return {
            'success': True,
            'book_title': book_title,
            'characters': CharacterConverter.to_list_response(characters),
            'count': len(characters)
        }

    @staticmethod
    def create_character(name: str, book_title: str, description: str = None, quote: str = None) -> Dict:
        error = CharacterValidator.validate_character_data(name, book_title)
        if error:
            return {'success': False, 'error': error}

        character_id = CharacterRepository.create_character(name, book_title, description, quote)
        CharacterNotifier.notify_character_created(name)

        return {
            'success': True,
            'character_id': character_id,
            'message': f'Персонаж "{name}" створений'
        }

    @staticmethod
    def update_character(character_id: int, name: str = None, book_title: str = None,
                         description: str = None, quote: str = None) -> Dict:
        error = CharacterValidator.validate_character_id(character_id)
        if error:
            return {'success': False, 'error': error}

        existing = CharacterRepository.get_character_by_id(character_id)
        if not existing:
            return {'success': False, 'error': 'Character not found'}

        CharacterRepository.update_character(character_id, name, book_title, description, quote)

        return {
            'success': True,
            'message': 'Персонаж оновлений'
        }

    @staticmethod
    def delete_character(character_id: int) -> Dict:
        error = CharacterValidator.validate_character_id(character_id)
        if error:
            return {'success': False, 'error': error}

        character = CharacterRepository.get_character_by_id(character_id)
        if not character:
            return {'success': False, 'error': 'Character not found'}

        CharacterRepository.delete_character(character_id)
        CharacterNotifier.notify_character_deleted(character.get('name'))

        return {
            'success': True,
            'message': f'Персонаж "{character.get("name")}" видалений'
        }

    @staticmethod
    def search_characters(search_term: str) -> Dict:
        if not search_term:
            return {'success': False, 'error': 'Search term is required'}

        characters = CharacterRepository.search_characters(search_term)

        return {
            'success': True,
            'search_term': search_term,
            'characters': CharacterConverter.to_list_response(characters),
            'count': len(characters)
        }

    @staticmethod
    def get_popular_characters(limit: int = 5) -> Dict:
        popular = CharacterRepository.get_popular_characters(limit)

        return {
            'success': True,
            'popular_characters': popular,
            'limit': limit
        }

    @staticmethod
    def get_character_description_text(character_id: int) -> Dict:
        error = CharacterValidator.validate_character_id(character_id)
        if error:
            return {'success': False, 'error': error}

        character = CharacterRepository.get_character_by_id(character_id)
        if not character:
            return {'success': False, 'error': 'Character not found'}

        return {
            'success': True,
            'description': CharacterHelper.get_character_description(character),
            'quote': CharacterHelper.format_quote(character)
        }
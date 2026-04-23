from typing import Dict, List, Optional
from Modules.Repositories import ResultRepository
from Modules.Repositories import CharacterRepository


class ResultValidator:
    @staticmethod
    def validate_session_id(session_id: str) -> Optional[str]:
        if not session_id:
            return 'Session ID is required'
        return None

    @staticmethod
    def validate_result_data(session_id: str, user_id: int, character_id: int) -> Optional[str]:
        if not session_id:
            return 'Session ID is required'
        if not user_id:
            return 'User ID is required'
        if not character_id:
            return 'Character ID is required'
        return None


class ResultConverter:
    @staticmethod
    def to_dto(result: Dict) -> Dict:
        if not result:
            return None
        return {
            'id': result.get('id'),
            'session_id': result.get('session_id'),
            'user_id': result.get('user_id'),
            'character_id': result.get('character_id'),
            'character_name': result.get('character_name'),
            'total_score': result.get('total_score', 0),
            'percentage': result.get('percentage', 0.0),
            'created_at': result.get('created_at')
        }

    @staticmethod
    def to_full_result(result: Dict, character: Dict) -> Dict:
        return {
            'result': ResultConverter.to_dto(result),
            'character': {
                'id': character.get('id'),
                'name': character.get('name'),
                'description': character.get('description'),
                'quote': character.get('quote')
            }
        }

    @staticmethod
    def to_list_response(results: List[Dict]) -> List[Dict]:
        return [ResultConverter.to_dto(r) for r in results]


class ResultHelper:
    @staticmethod
    def calculate_level(percentage: float) -> str:
        if percentage >= 80:
            return "excellent"
        elif percentage >= 60:
            return "good"
        elif percentage >= 40:
            return "average"
        else:
            return "poor"

    @staticmethod
    def get_level_description(level: str) -> str:
        levels = {
            "excellent": "Вітаю! Ти справжній цей персонаж!",
            "good": "Ти дуже схожий на цього персонажа!",
            "average": "У тебе є риси цього персонажа!",
            "poor": "Ти трохи схожий на цього персонажа!"
        }
        return levels.get(level, "")

    @staticmethod
    def format_result_message(character_name: str, percentage: float) -> str:
        level = ResultHelper.calculate_level(percentage)
        description = ResultHelper.get_level_description(level)
        return f"{description} Твій персонаж: {character_name} ({percentage}%)"


class ResultNotifier:
    @staticmethod
    def notify_result_saved(session_id: str, character_name: str, percentage: float):
        print(f"[NOTIFY] Збережено результат: сесія={session_id}, персонаж={character_name}, {percentage}%")

    @staticmethod
    def notify_result_fetched(session_id: str):
        print(f"[NOTIFY] Отримано результат для сесії: {session_id}")


class ResultService:
    @staticmethod
    def save_result(session_id: str, user_id: int, character_id: int, total_score: int, percentage: float) -> Dict:
        error = ResultValidator.validate_result_data(session_id, user_id, character_id)
        if error:
            return {'success': False, 'error': error}

        ResultRepository.save_result(session_id, user_id, character_id, total_score, percentage)

        character = CharacterRepository.get_character_by_id(character_id)
        character_name = character.get('name') if character else "Невідомо"

        ResultNotifier.notify_result_saved(session_id, character_name, percentage)

        return {
            'success': True,
            'message': 'Result saved successfully',
            'session_id': session_id,
            'character_name': character_name,
            'percentage': percentage
        }

    @staticmethod
    def get_result_by_session(session_id: str) -> Dict:
        error = ResultValidator.validate_session_id(session_id)
        if error:
            return {'success': False, 'error': error}

        result = ResultRepository.get_result_by_session(session_id)
        if not result:
            return {'success': False, 'error': 'Result not found'}

        ResultNotifier.notify_result_fetched(session_id)

        character = CharacterRepository.get_character_by_id(result.get('character_id'))

        return {
            'success': True,
            'result': ResultConverter.to_full_result(result, character) if character else ResultConverter.to_dto(result),
            'message': ResultHelper.format_result_message(
                result.get('character_name', 'Невідомо'),
                result.get('percentage', 0)
            )
        }

    @staticmethod
    def get_user_results(user_id: int, limit: int = 10) -> Dict:
        if not user_id:
            return {'success': False, 'error': 'User ID is required'}

        results = ResultRepository.get_results_by_user(user_id, limit)

        return {
            'success': True,
            'user_id': user_id,
            'results': ResultConverter.to_list_response(results),
            'count': len(results),
            'limit': limit
        }

    @staticmethod
    def get_character_stats(character_id: int) -> Dict:
        if not character_id:
            return {'success': False, 'error': 'Character ID is required'}

        character = CharacterRepository.get_character_by_id(character_id)
        if not character:
            return {'success': False, 'error': 'Character not found'}

        avg_score = ResultRepository.get_average_score_by_character(character_id)

        return {
            'success': True,
            'character': {
                'id': character.get('id'),
                'name': character.get('name'),
                'book_title': character.get('book_title')
            },
            'statistics': {
                'average_percentage': round(avg_score, 2),
                'level': ResultHelper.calculate_level(avg_score)
            }
        }

    @staticmethod
    def delete_result(result_id: int) -> Dict:
        if not result_id:
            return {'success': False, 'error': 'Result ID is required'}

        ResultRepository.delete_result(result_id)

        return {
            'success': True,
            'message': 'Result deleted successfully'
        }

    @staticmethod
    def get_total_quiz_count() -> Dict:
        count = ResultRepository.get_total_quiz_count()
        return {
            'success': True,
            'total_quizzes_completed': count
        }
from typing import Dict, List, Optional
from Modules.Repositories import QuizRepository


class QuizValidator:
    @staticmethod
    def validate_start_data(user_id: int, quiz_id: int) -> Optional[str]:
        if not user_id:
            return 'User ID is required'
        if not quiz_id:
            return 'Quiz ID is required'
        return None

    @staticmethod
    def validate_answer(session_id: str, question_id: int, answer_id: int) -> Optional[str]:
        if not session_id:
            return 'Session ID is required'
        if not question_id:
            return 'Question ID is required'
        if not answer_id:
            return 'Answer ID is required'
        return None


class QuizConverter:
    @staticmethod
    def to_response(quiz: Dict, session_id: str, first_question: Dict) -> Dict:
        return {
            'session_id': session_id,
            'quiz_id': quiz.get('id'),
            'title': quiz.get('title'),
            'description': quiz.get('description'),
            'total_questions': quiz.get('total_questions', 5),
            'first_question': first_question
        }

    @staticmethod
    def to_answer_response(answered_count: int, total_questions: int, next_question: Dict, progress: float) -> Dict:
        return {
            'success': True,
            'completed': False,
            'answered_count': answered_count,
            'total_questions': total_questions,
            'progress': progress,
            'next_question': next_question
        }

    @staticmethod
    def to_result_response(character: Dict, total_score: int, max_score: int, percentage: float, level: str) -> Dict:
        return {
            'success': True,
            'completed': True,
            'character': {
                'id': character.get('id'),
                'name': character.get('name'),
                'book_title': character.get('book_title'),
                'description': character.get('description'),
                'quote': character.get('quote')
            } if character else None,
            'total_score': total_score,
            'max_score': max_score,
            'percentage': percentage,
            'level': level
        }


class QuizHelper:
    @staticmethod
    def calculate_progress(answered: int, total: int) -> float:
        if total == 0:
            return 0.0
        return round((answered / total) * 100, 2)

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
    def aggregate_scores(answers: List[Dict]) -> Dict[int, int]:
        scores = {}
        for answer in answers:
            char_id = answer.get('character_id')
            score = answer.get('score', 0)
            if char_id:
                scores[char_id] = scores.get(char_id, 0) + score
        return scores

    @staticmethod
    def determine_character(scores: Dict[int, int]) -> Optional[int]:
        if not scores:
            return None
        return max(scores, key=scores.get)

    @staticmethod
    def get_next_question(questions: List[Dict], answered_ids: List[int]) -> Optional[Dict]:
        for q in questions:
            if q['id'] not in answered_ids:
                return q
        return None


class QuizNotifier:
    @staticmethod
    def notify_quiz_started(user_id: int, session_id: str):
        print(f"[NOTIFY] Користувач {user_id} почав тест. Сесія: {session_id}")

    @staticmethod
    def notify_quiz_completed(session_id: str, character_name: str):
        print(f"[NOTIFY] Тест завершено. Сесія: {session_id}. Результат: {character_name}")

    @staticmethod
    def notify_answer_saved(session_id: str, question_id: int):
        print(f"[NOTIFY] Збережено відповідь. Сесія: {session_id}, Питання: {question_id}")


class QuizService:
    @staticmethod
    def start_quiz(user_id: int, quiz_id: int) -> Dict:
        error = QuizValidator.validate_start_data(user_id, quiz_id)
        if error:
            return {'success': False, 'error': error}

        quiz = QuizRepository.get_quiz_by_id(quiz_id)
        if not quiz:
            return {'success': False, 'error': 'Quiz not found'}

        questions = QuizRepository.get_questions_by_quiz(quiz_id)
        session_id = QuizRepository.create_session(user_id, quiz_id)

        first_question = None
        if questions:
            first_question = QuizRepository.get_question_with_answers(questions[0]['id'])
            if first_question:
                for a in first_question.get('answers', []):
                    a.pop('character_id', None)
                    a.pop('score', None)

        QuizNotifier.notify_quiz_started(user_id, session_id)

        return {'success': True, **QuizConverter.to_response(quiz, session_id, first_question)}

    @staticmethod
    def submit_answer(session_id: str, question_id: int, answer_id: int) -> Dict:
        error = QuizValidator.validate_answer(session_id, question_id, answer_id)
        if error:
            return {'success': False, 'error': error}

        session = QuizRepository.get_session(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}

        if session['status'] != 'in_progress':
            return {'success': False, 'error': 'Quiz already completed'}

        answer = QuizRepository.get_answer_by_id(answer_id)
        if not answer:
            return {'success': False, 'error': 'Answer not found'}

        QuizRepository.save_answer(
            session_id, question_id, answer_id,
            answer.get('character_id'), answer.get('score', 0)
        )

        QuizNotifier.notify_answer_saved(session_id, question_id)

        answered_count = QuizRepository.get_answered_count(session_id)
        questions = QuizRepository.get_questions_by_quiz(session['quiz_id'])

        if answered_count >= len(questions):
            return QuizService.complete_quiz(session_id)

        answered_ids = QuizRepository.get_answered_question_ids(session_id)
        next_question_raw = QuizHelper.get_next_question(questions, answered_ids)

        next_question = None
        if next_question_raw:
            next_question = QuizRepository.get_question_with_answers(next_question_raw['id'])
            if next_question:
                for a in next_question.get('answers', []):
                    a.pop('character_id', None)
                    a.pop('score', None)

        progress = QuizHelper.calculate_progress(answered_count, len(questions))

        return QuizConverter.to_answer_response(answered_count, len(questions), next_question, progress)

    @staticmethod
    def complete_quiz(session_id: str) -> Dict:
        session = QuizRepository.get_session(session_id)
        answers = QuizRepository.get_user_answers(session_id)
        questions = QuizRepository.get_questions_by_quiz(session['quiz_id'])

        scores = QuizHelper.aggregate_scores(answers)
        character_id = QuizHelper.determine_character(scores)

        total_score = sum(scores.values())
        max_score = len(questions) * 10
        percentage = round((total_score / max_score) * 100, 2) if max_score else 0
        level = QuizHelper.calculate_level(percentage)

        character = QuizRepository.get_character_by_id(character_id) if character_id else None

        QuizRepository.save_result(session_id, session['user_id'], character_id, total_score, percentage)
        QuizRepository.complete_session(session_id)

        QuizNotifier.notify_quiz_completed(session_id, character.get('name') if character else "Невідомо")

        return QuizConverter.to_result_response(character, total_score, max_score, percentage, level)

    @staticmethod
    def get_result(session_id: str) -> Dict:
        result = QuizRepository.get_result(session_id)
        if not result:
            return {'success': False, 'error': 'Result not found'}
        return {'success': True, 'result': result}
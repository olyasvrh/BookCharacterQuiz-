from typing import Dict, List, Optional
from Modules.Repositories import QuestionRepository, AnswerRepository


class QuestionValidator:
    @staticmethod
    def validate_question_data(text: str, quiz_id: int) -> Optional[str]:
        if not text:
            return 'Question text is required'
        if not quiz_id:
            return 'Quiz ID is required'
        return None

    @staticmethod
    def validate_question_id(question_id: int) -> Optional[str]:
        if not question_id:
            return 'Question ID is required'
        return None

    @staticmethod
    def validate_answer_data(text: str, question_id: int) -> Optional[str]:
        if not text:
            return 'Answer text is required'
        if not question_id:
            return 'Question ID is required'
        return None


class QuestionConverter:
    @staticmethod
    def to_dto(question: Dict) -> Dict:
        if not question:
            return None
        return {
            'id': question.get('id'),
            'quiz_id': question.get('quiz_id'),
            'text': question.get('text'),
            'order_num': question.get('order_num', 0)
        }

    @staticmethod
    def to_api_format(question: Dict, question_number: int = 0, total: int = 5) -> Dict:
        if not question:
            return None
        answers = question.get('answers', [])
        return {
            'question_number': question_number,
            'total_questions': total,
            'id': question.get('id'),
            'text': question.get('text'),
            'answers': [
                {'id': a.get('id'), 'text': a.get('text')}
                for a in answers
            ]
        }

    @staticmethod
    def answer_to_dto(answer: Dict) -> Dict:
        if not answer:
            return None
        return {
            'id': answer.get('id'),
            'question_id': answer.get('question_id'),
            'text': answer.get('text'),
            'character_id': answer.get('character_id'),
            'score': answer.get('score', 0)
        }

    @staticmethod
    def to_list_response(questions: List[Dict]) -> List[Dict]:
        return [QuestionConverter.to_dto(q) for q in questions]


class QuestionHelper:
    @staticmethod
    def shuffle_answers(answers: List[Dict]) -> List[Dict]:
        import random
        shuffled = answers.copy()
        random.shuffle(shuffled)
        return shuffled

    @staticmethod
    def get_next_order_num(questions: List[Dict]) -> int:
        if not questions:
            return 1
        max_order = max([q.get('order_num', 0) for q in questions])
        return max_order + 1


class QuestionNotifier:
    @staticmethod
    def notify_question_created(question_id: int, text: str):
        print(f"[NOTIFY] Створено питання ID={question_id}: {text[:50]}...")

    @staticmethod
    def notify_question_deleted(question_id: int):
        print(f"[NOTIFY] Видалено питання ID={question_id}")

    @staticmethod
    def notify_answer_created(answer_id: int, question_id: int):
        print(f"[NOTIFY] Створено відповідь ID={answer_id} для питання {question_id}")


class QuestionService:
    @staticmethod
    def get_questions_by_quiz(quiz_id: int) -> Dict:
        questions = QuestionRepository.get_questions_by_quiz(quiz_id)
        return {
            'success': True,
            'quiz_id': quiz_id,
            'questions': QuestionConverter.to_list_response(questions),
            'count': len(questions)
        }

    @staticmethod
    def get_question_with_answers(question_id: int, total_questions: int = 5, question_number: int = 0) -> Dict:
        error = QuestionValidator.validate_question_id(question_id)
        if error:
            return {'success': False, 'error': error}

        question = QuestionRepository.get_question_with_answers(question_id)
        if not question:
            return {'success': False, 'error': 'Question not found'}

        shuffled_answers = QuestionHelper.shuffle_answers(question.get('answers', []))
        question['answers'] = shuffled_answers

        return {
            'success': True,
            'question': QuestionConverter.to_api_format(question, question_number, total_questions)
        }

    @staticmethod
    def create_question(quiz_id: int, text: str) -> Dict:
        error = QuestionValidator.validate_question_data(text, quiz_id)
        if error:
            return {'success': False, 'error': error}

        existing_questions = QuestionRepository.get_questions_by_quiz(quiz_id)
        order_num = QuestionHelper.get_next_order_num(existing_questions)

        question_id = QuestionRepository.create_question(quiz_id, text, order_num)
        QuestionNotifier.notify_question_created(question_id, text)

        return {
            'success': True,
            'question_id': question_id,
            'message': 'Question created successfully'
        }

    @staticmethod
    def update_question(question_id: int, text: str = None, order_num: int = None) -> Dict:
        error = QuestionValidator.validate_question_id(question_id)
        if error:
            return {'success': False, 'error': error}

        existing = QuestionRepository.get_question_by_id(question_id)
        if not existing:
            return {'success': False, 'error': 'Question not found'}

        QuestionRepository.update_question(question_id, text, order_num)

        return {
            'success': True,
            'message': 'Question updated successfully'
        }

    @staticmethod
    def delete_question(question_id: int) -> Dict:
        error = QuestionValidator.validate_question_id(question_id)
        if error:
            return {'success': False, 'error': error}

        QuestionRepository.delete_question(question_id)
        QuestionNotifier.notify_question_deleted(question_id)

        return {
            'success': True,
            'message': 'Question deleted successfully'
        }

    @staticmethod
    def create_answer(question_id: int, text: str, character_id: int = None, score: int = 0) -> Dict:
        error = QuestionValidator.validate_answer_data(text, question_id)
        if error:
            return {'success': False, 'error': error}

        answer_id = AnswerRepository.create_answer(question_id, text, character_id, score)
        QuestionNotifier.notify_answer_created(answer_id, question_id)

        return {
            'success': True,
            'answer_id': answer_id,
            'message': 'Answer created successfully'
        }

    @staticmethod
    def get_answers_by_question(question_id: int) -> Dict:
        error = QuestionValidator.validate_question_id(question_id)
        if error:
            return {'success': False, 'error': error}

        answers = AnswerRepository.get_answers_by_question(question_id)

        return {
            'success': True,
            'question_id': question_id,
            'answers': [QuestionConverter.answer_to_dto(a) for a in answers],
            'count': len(answers)
        }
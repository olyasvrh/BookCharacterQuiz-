from typing import List

# Модель для однієї відповіді
class AnswerVM:
    def __init__(self, question_id: int, point: int):
        self.question_id = question_id
        self.point = point

# Головна модель для надсилання всього тесту на сервер
class QuizSubmitVM:
    def __init__(self, user_id: int, quiz_id: int, answers: List[AnswerVM]):
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.answers = answers

# Додаткова модель для запитів про персонажів (наприклад, для BookController)
class CharacterRequestVM:
    def __init__(self, character_id: int, search_query: str = ""):
        self.character_id = character_id
        self.search_query = search_query
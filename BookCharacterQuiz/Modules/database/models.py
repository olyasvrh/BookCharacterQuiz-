from Modules.database.db import execute_query, execute_update, get_connection

CREATE_TABLES_QUERIES = {
    "quizzes": """
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            total_questions INTEGER DEFAULT 5
        )
    """,
    "questions": """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            order_num INTEGER DEFAULT 0
        )
    """,
    "answers": """
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            character_id INTEGER,
            score INTEGER DEFAULT 0
        )
    """,
    "characters": """
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            book_title TEXT NOT NULL,
            description TEXT,
            quote TEXT
        )
    """,
    "quiz_sessions": """
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            status TEXT DEFAULT 'in_progress',
            started_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "user_answers": """
        CREATE TABLE IF NOT EXISTS user_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            character_id INTEGER,
            score INTEGER DEFAULT 0
        )
    """,
    "results": """
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            character_id INTEGER NOT NULL,
            total_score INTEGER DEFAULT 0,
            percentage REAL DEFAULT 0
        )
    """
}

def init_database():
    with get_connection() as conn:
        cursor = conn.cursor()
        for name, query in CREATE_TABLES_QUERIES.items():
            cursor.execute(query)
    
    insert_sample_data()

def insert_sample_data():
    chars = execute_query("SELECT COUNT(*) as count FROM characters")
    if chars[0]['count'] == 0:
        characters = [
            (1, 'Гендальф', 'Володар перснів', 'Мудрий чарівник', 'Навіть найменша людина може змінити хід майбутнього'),
            (2, 'Арагорн', 'Володар перснів', 'Сміливий воїн та лідер', 'Не завжди сила вирішує долю'),
            (3, 'Сем', 'Володар перснів', 'Вірний друг', 'Я можу нести тебе'),
            (4, 'Ерміона', 'Гаррі Поттер', 'Найрозумніша відьма', 'Книги! І розум!')
        ]
        for c in characters:
            execute_update("INSERT INTO characters (id, name, book_title, description, quote) VALUES (?, ?, ?, ?, ?)", c)
    
    quizzes = execute_query("SELECT COUNT(*) as count FROM quizzes")
    if quizzes[0]['count'] == 0:
        execute_update("INSERT INTO quizzes (id, title, description, total_questions) VALUES (1, 'Хто ти з книжкових персонажів?', 'Тест для визначення книжкового персонажа', 5)")
    
    questions = execute_query("SELECT COUNT(*) as count FROM questions")
    if questions[0]['count'] == 0:
        q_data = [
            (1, 1, 'Як ти проводиш вільний час?', 1),
            (2, 1, 'Яка твоя найсильніша риса?', 2),
            (3, 1, 'Що для тебе найважливіше?', 3),
            (4, 1, 'Як реагуєш на труднощі?', 4),
            (5, 1, 'Який жанр книг тобі ближчий?', 5)
        ]
        for q in q_data:
            execute_update("INSERT INTO questions (id, quiz_id, text, order_num) VALUES (?, ?, ?, ?)", q)
    
    answers = execute_query("SELECT COUNT(*) as count FROM answers")
    if answers[0]['count'] == 0:
        a_data = [
            (1, 1, 'Читаю книгу', 1, 10), (2, 1, 'Подорожую', 2, 10),
            (3, 1, 'Допомагаю іншим', 3, 10), (4, 1, 'Вчусь новому', 4, 10),
            (5, 2, 'Мудрість', 1, 10), (6, 2, 'Сміливість', 2, 10),
            (7, 2, 'Доброта', 3, 10), (8, 2, 'Розум', 4, 10),
            (9, 3, 'Знання', 1, 10), (10, 3, 'Свобода', 2, 10),
            (11, 3, 'Родина', 3, 10), (12, 3, 'Справедливість', 4, 10),
            (13, 4, 'Аналізую', 1, 10), (14, 4, 'Дію рішуче', 2, 10),
            (15, 4, 'Шукаю підтримки', 3, 10), (16, 4, 'Вивчаю проблему', 4, 10),
            (17, 5, 'Філософія', 1, 10), (18, 5, 'Пригоди', 2, 10),
            (19, 5, 'Сімейна сага', 3, 10), (20, 5, 'Детектив', 4, 10)
        ]
        for a in a_data:
            execute_update("INSERT INTO answers (id, question_id, text, character_id, score) VALUES (?, ?, ?, ?, ?)", a)
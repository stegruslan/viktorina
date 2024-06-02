import sqlite3


class Quiz:
    def __init__(self, questions, difficulty):
        # Инициализируем викторину с вопросами и уровнем сложности
        self.questions = questions
        self.difficulty = difficulty
        self.score = 0  # Счетчик правильных ответов

    def start(self):
        # Запускаем викторину
        for question in self.questions:
            # Для каждого вопроса в списке вопросов
            print(question.text)  # Печатаем текст вопроса
            for i, option in enumerate(question.options):
                # Печатаем варианты ответов
                print(f"{i + 1}. {option}")
            answer = int(input("Ваш ответ: "))  # Считываем ответ пользователя
            if question.check_answer(answer):
                # Проверяем, правильный ли ответ
                self.score += 1  # Увеличиваем счетчик правильных ответов
        print(f"Ваш результат: {self.score} правильных ответов")  # Печатаем результат викторины


class Question:
    def __init__(self, text, options, correct_option):
        # Инициализируем вопрос с текстом, вариантами ответов и правильным вариантом
        self.text = text
        self.options = options
        self.correct_option = correct_option

    def check_answer(self, answer):
        # Проверяем, правильный ли ответ
        return answer == self.correct_option


class User:
    def __init__(self, name, score, difficulty):
        # Инициализируем пользователя с именем, очками и уровнем сложности
        self.name = name
        self.score = score
        self.difficulty = difficulty


class Leaderboard:
    def __init__(self, db):
        # Инициализируем таблицу лидеров с базой данных
        self.db = db

    def save_result(self, user):
        # Сохраняем результат пользователя в базу данных
        self.db.insert_result(user.name, user.score, user.difficulty)

    def show_leaderboard(self, difficulty):
        # Отображаем таблицу лидеров для заданного уровня сложности
        results = self.db.get_results(difficulty)
        for result in results:
            # Печатаем имя и очки каждого пользователя в таблице лидеров
            print(f"Имя: {result[0]}, Очки: {result[1]}")


class Database:
    def __init__(self, db_name="quiz.db"):
        # Инициализируем базу данных с именем файла базы данных
        self.conn = sqlite3.connect(db_name)
        self.create_table()  # Создаем таблицу, если её нет

    def create_table(self):
        # Создаем таблицу для хранения результатов, если её нет
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS leaderboard (name TEXT, score INTEGER, difficulty TEXT)"
            )

    def insert_result(self, name, score, difficulty):
        # Вставляем результат пользователя в таблицу
        with self.conn:
            self.conn.execute(
                "INSERT INTO leaderboard (name, score, difficulty) VALUES (?, ?, ?)",
                (name, score, difficulty),
            )

    def get_results(self, difficulty):
        # Получаем результаты для заданного уровня сложности, отсортированные по очкам
        cursor = self.conn.execute(
            "SELECT name, score FROM leaderboard WHERE difficulty=? ORDER BY score DESC",
            (difficulty,),
        )
        return cursor.fetchall()  # Возвращаем все результаты


# Легкие вопросы
easy_questions = [
    Question("Какого цвета небо?", ["Синий", "Зеленый", "Красный", "Желтый"], 1),
    Question("Сколько дней в неделе?", ["5", "6", "7", "8"], 3),
    Question("Сколько пальцев на руке у человека?", ["4", "5", "6", "7"], 2),
    Question("Какой газ необходим для дыхания?", ["Гелий", "Кислород", "Водород", "Азот"], 2),
    Question("Как называется столица Франции?", ["Берлин", "Мадрид", "Париж", "Лондон"], 3)
]

# Средние вопросы
medium_questions = [
    Question("Кто написал 'Война и мир'?", ["Толстой", "Достоевский", "Пушкин", "Гоголь"], 1),
    Question("Сколько планет в Солнечной системе?", ["7", "8", "9", "10"], 2),
    Question("Какой элемент обозначается символом 'O'?", ["Золото", "Кислород", "Серебро", "Железо"], 2),
    Question("Кто является основателем компании Microsoft?",
             ["Стив Джобс", "Билл Гейтс", "Марк Цукерберг", "Илон Маск"], 2),
    Question("В каком году человек впервые ступил на Луну?", ["1965", "1969", "1972", "1980"], 2)
]

# Сложные вопросы
hard_questions = [
    Question("Что такое квантовая механика?", ["Раздел физики", "Теория музыки", "Стиль искусства", "Вид спорта"], 1),
    Question("Кто разработал теорию относительности?", ["Ньютон", "Эйнштейн", "Галилей", "Бор"], 2),
    Question("Кто написал оперу 'Волшебная флейта'?", ["Бетховен", "Моцарт", "Шуберт", "Вивальди"], 2),
    Question("Кто является автором картины 'Мона Лиза'?",
             ["Ван Гог", "Пабло Пикассо", "Леонардо да Винчи", "Рембрандт"], 3),
    Question("Как называется самая большая планета в Солнечной системе?", ["Земля", "Марс", "Юпитер", "Сатурн"], 3)
]


def main():
    db = Database()  # Создаем экземпляр базы данных
    leaderboard = Leaderboard(db)  # Создаем экземпляр таблицы лидеров

    name = input("Введите ваше имя: ")  # Запрашиваем имя пользователя
    difficulty = input(
        "Выберите уровень сложности (легкий, средний, сложный): ").lower()  # Запрашиваем уровень сложности

    # В зависимости от выбранного уровня сложности выбираем соответствующий список вопросов
    if difficulty == "легкий":
        questions = easy_questions
    elif difficulty == "средний":
        questions = medium_questions
    elif difficulty == "сложный":
        questions = hard_questions
    else:
        print("Некорректный уровень сложности. Попробуйте снова.")
        return

    quiz = Quiz(questions, difficulty)  # Создаем экземпляр викторины с вопросами и уровнем сложности
    quiz.start()  # Запускаем викторину

    user = User(name, quiz.score, difficulty)  # Создаем экземпляр пользователя с его результатами
    leaderboard.save_result(user)  # Сохраняем результат пользователя в таблицу лидеров

    print("\nТаблица лидеров в этой категории сложности:")  # Печатаем таблицу лидеров
    leaderboard.show_leaderboard(difficulty)  # Отображаем таблицу лидеров для выбранного уровня сложности


if __name__ == "__main__":
    main()  # Запускаем функцию main, если скрипт запускается напрямую

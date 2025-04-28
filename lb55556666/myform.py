# Импорт необходимых модулей
from bottle import post, request  # Импорт декоратора @post и объекта request из фреймворка Bottle
from datetime import datetime  # Импорт datetime для работы с датами
import re  # Импорт модуля для работы с регулярными выражениями
import json  # Импорт модуля для работы с JSON
import os  # Импорт модуля для работы с операционной системой
import pdb  # Импорт модуля для отладки (Python Debugger)

# Имя файла для хранения данных в формате JSON
FILE = 'questions.json'




def validate_email(email):
    """Проверяет валидность email"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.fullmatch(pattern, email))

# Функция для загрузки данных из JSON-файла
def load_data():
    # Проверяем, существует ли файл
    if os.path.exists(FILE):
        # Если файл существует, открываем его для чтения
        with open(FILE, 'r', encoding='utf-8') as file:
            # Загружаем и возвращаем данные из файла в формате JSON
            return json.load(file)
    # Если файл не существует, возвращаем пустой словарь
    return {}

# Функция для сохранения данных в JSON-файл
def save_data(data):
    # Открываем файл для записи (если файла нет, он будет создан)
    with open(JSON_FILE, 'w', encoding='utf-8') as file:
        # Записываем данные в файл с отступами (для читаемости) 
        # и поддержкой кириллицы (ensure_ascii=False)
        json.dump(data, file, indent=4, ensure_ascii=False)

# Обработчик POST-запроса по адресу '/home'
@post('/home', method='post')
def my_form():
    # Получаем данные из формы:
    mail = request.forms.get('ADRESS')  # Email пользователя
    username = request.forms.get('USERNAME')  # Имя пользователя
    question = request.forms.get('QUEST')  # Вопрос пользователя

    # --- Проверки ---

    # Проверка на заполнение всех полей
    if not mail and not username and not question:
        return "Error: All fields must be filled!"
    if not username:
        return "Error: You didn't enter your name!"
    if not mail:
        return "Error: You didn't enter your email!"
    if not question:
        return "Error: You didn't enter your question!"

    # Проверка имени пользователя:
    # Должно быть от 2 до 50 латинских букв
    if not re.fullmatch(r'[A-Za-z]{2,50}', username):
        return "Error: Name must be at least 2 letters and contain only Latin letters!"

    # Проверка вопроса:
    # Должен быть не короче 4 символов (после удаления пробелов)
    if len(question.strip()) < 4:
        return "Error: Question must be at least 4 characters long!"
    # Не может состоять только из цифр
    if question.strip().isdigit():
        return "Error: Question can't contain only digits!"

    # Сложный паттерн для проверки email:
    email_pattern = (
        r'^[a-zA-Z0-9](?!.*?[._-]{2})[a-zA-Z0-9._%+-]{2,63}'  # Локальная часть до @
        r'@[a-zA-Z0-9-]{1,63}(\.[a-zA-Z]{2,10}){1,3}$'  # Доменная часть после @
    )
    if not re.match(email_pattern, mail):
        return "Error: Invalid email address format!"

    # Дополнительная проверка: локальная часть email не может состоять только из цифр
    local_part = mail.split('@')[0]
    if local_part.isdigit():
        return "Error: Email address can't contain only digits before @"

    # --- Работа с данными ---

    # Загружаем текущие данные из файла
    data = load_data()

    # Если email нет в данных, добавляем нового пользователя
    if mail not in data:
        data[mail] = {"username": username, "questions": []}

    # Проверяем, не задавал ли пользователь этот вопрос ранее
    if question not in data[mail]["questions"]:
        # Если вопрос новый, добавляем его в список
        data[mail]["questions"].append(question)
    else:
        return "Error: This question has already been asked!"

    # Сохраняем обновленные данные в файл
    save_data(data)

    # Точка останова для отладки (можно удалить в продакшн-коде)
    pdb.set_trace()

    # Формируем дату в формате ГГГГ-ММ-ДД
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Возвращаем сообщение об успешной обработке формы
    return f"Thanks, {username}! The answer will be sent to the mail {mail}. Access Date: {current_date}"
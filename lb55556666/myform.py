from bottle import post, request, route, static_file
import re
from datetime import datetime
import json
import os
import pdb  # Импортируем pdb для отладочной печати

# Путь к JSON-файлу
DATA_FILE = "user_data.json"

# Загрузка данных из JSON-файла
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# Сохранение данных в JSON-файл
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

@post('/home', method='post')
def my_form():
    # Загружаем текущие данные из файла
    user_data = load_data()

    # Получаем данные из формы
    mail = request.forms.get('ADRESS')
    username = request.forms.get('USERNAME')
    question = request.forms.get('QUEST')

    # Проверка заполненности полей
    if not mail or not username or not question:
        return "Error: All fields must be filled!"

    # Строгий паттерн для проверки формата электронной почты
    email_pattern = r"^(?:[a-zA-Z0-9_'^&/+-])+(?:\.(?:[a-zA-Z0-9_'^&/+-]+))*@(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})$"

    # Проверка формата электронной почты
    if not re.match(email_pattern, mail):
        return "Error: Invalid email format!"

    # Проверка общей длины адреса
    if len(mail) > 254:
        return "Error: Email address is too long!"

    # Проверка длины вопроса (более 3 символов)
    if len(question) <= 3:
        return "Error: The question must be longer than 3 characters!"

    # Проверка, что вопрос не состоит только из цифр
    if question.isdigit():
        return "Error: The question cannot consist only of digits!"

    # Если пользователь уже есть в словаре, добавляем вопрос в список
    if mail in user_data:
        # Проверяем, чтобы вопрос не был дубликатом
        if question not in user_data[mail]["questions"]:
            user_data[mail]["questions"].append(question)
        else:
            return f"Error: The question '{question}' already exists for this user!"
    else:
        # Создаем новую запись для пользователя
        user_data[mail] = {
            "username": username,
            "questions": [question]
        }

    # Сохраняем обновленные данные в файл
    save_data(user_data)

    # Отладочная печать с использованием pdb
    pdb.set_trace()  # Останавливаем выполнение программы для просмотра данных

    # Получение текущей даты в формате YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Формирование результирующего сообщения
    result_message = f"Thanks, {username}! The answer will be sent to the mail {mail}. Access Date: {current_date}"

    return result_message

# Роут для статических файлов
@route('/static/<filepath:path>')
def server_static(filepath):
    """Handler for static files, used with the development server."""
    return static_file(filepath, root='./static')

if __name__ == '__main__':
    from bottle import run
    run(host='localhost', port=8080, debug=True)
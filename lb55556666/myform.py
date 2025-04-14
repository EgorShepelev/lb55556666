from bottle import post, request, route, static_file
import re
from datetime import datetime
import pdb  # Импортируем pdb для отладочной печати

# Глобальный словарь для хранения данных (email -> [USERNAME, QUESTION])
user_data = {}

@post('/home', method='post')
def my_form():
    global user_data  # Объявляем использование глобального словаря

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

    # Проверка длины вопроса
    if len(question) > 1000:
        return "Error: The question is too long! Maximum 1000 characters allowed."

    # Добавляем данные в словарь (email -> [USERNAME, QUESTION])
    user_data[mail] = [username, question]

    # Отладочная печать с использованием pdb
    pdb.set_trace()  # Останавливаем выполнение программы для просмотра словаря

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
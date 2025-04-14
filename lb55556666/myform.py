from bottle import post, request
import re
from datetime import datetime

@post('/home', method='post')
def my_form():
    # Получаем данные из формы
    mail = request.forms.get('ADRESS')
    username = request.forms.get('USERNAME')

    # Проверка заполненности полей
    if not mail or not username:
        return "Error: All fields must be filled!"

    # Упрощённый паттерн для проверки формата электронной почты
    email_pattern = r"^(?=.{1,64}@)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Проверка формата электронной почты
    if not re.match(email_pattern, mail):
        return "Error: Invalid email format!"

    # Проверка общей длины адреса
    if len(mail) > 254:
        return "Error: Email address is too long!"

    # Получение текущей даты в формате YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Формирование результирующего сообщения
    result_message = f"Thanks, {username}! The answer will be sent to the mail {mail}. Access Date: {current_date}"

    return result_message
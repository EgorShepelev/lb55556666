from bottle import post, request, template
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

    # Проверка формата электронной почты с помощью регулярного выражения
    email_pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
    if not re.match(email_pattern, mail):
        return "Error: Invalid email format!"

    # Получение текущей даты в формате YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Формирование результирующего сообщения
    result_message = f"Thanks, {username}! The answer will be sent to the mail {mail}. Access Date: {current_date}"

    return result_message
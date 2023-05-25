from django.core.exceptions import ValidationError
import datetime
import re


def validate_year(year_real):
    if year_real > datetime.datetime.now().year:
        raise ValidationError('Check your year')


def validate_username(username):
    # https://docs.python.org/3/library/re.html#re.compile
    # Взял отсюда, но в redoc был указан такой шаблон - ^[\w.@+-]+\z,
    # Я понимаю, что "z" означает однозначный конец строки,
    # но с ним код не работает.
    # По-этому пришлось вставлять "$", который более гибкий или flexible
    template_of_string = r'^[\w.@+-]+$'
    # 'me' взят из эндпоинта redoc /users/me
    if username == 'me':
        raise ValidationError('Thats imposible')
    # Ищем совпаления между шаблоном и никнеймом юезра,
    # Чтобы все были одного порядка
    if not (re.match(template_of_string, username)):
        raise ValidationError('Check yuor albhabet')
    return username

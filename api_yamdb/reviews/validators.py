import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if len(value) > 150:
        raise ValidationError('Длина поля username не должна превышать 150 символов')
    pattern = r'^[\w.@+-]+$'
    if not re.search(pattern, value):
        raise ValidationError('Недопустимые символы', params={'value': value})
    if value.lower() == 'me':
        raise ValidationError("Имя не может быть 'me'")

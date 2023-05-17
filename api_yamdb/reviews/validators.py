import re

from django.core.exceptions import ValidationError


def validate_name(value):
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>')
        )
    if re.search(r'^[\w.@+-]+\z', value) is None:
        raise ValidationError(
            (f'Недопустимые символы'),
            params={'value': value},
        )
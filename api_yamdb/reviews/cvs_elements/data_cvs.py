import csv
from django.core.management.base import BaseCommand, CommandError
from reviews.models import (Title, Category,
                            Genre, User,
                            Review, Comment,
                            GenreTitle)
from collections import OrderedDict
from django.db import transaction

# https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/
# взято отсюда
default_data = OrderedDict({
    'category.csv': Category,
    'comments.csv': Comment,
    'genre_title.csv': GenreTitle,
    'genre.csv': Genre,
    'review.csv': Review,
    'titles.csv': Title,
    'users.csv': User
})
data_path = 'static/data/'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Beginning of import")
        with transaction.atomic():
            for filename, model in default_data.items():
                try:
                    with open(data_path + filename,
                              newline='', encoding='utf-8') as data_csv:
                        reader = csv.DictReader(data_csv)
                        model_objects = [model(**data) for data in reader]
                        model.objects.bulk_create(model_objects)
                except model.DoesNotExist:
                    raise CommandError('File does not exist: %s' % filename)
        self.stdout.write(
            self.style.SUCCESS('All csv_data have been imported'))

# Здесь для каждого файла CSV мы сначала формируем список объектов модели (model_objects), 
# а затем используем метод bulk_create, чтобы создать все объекты одним запросом. Весь 
# процесс выполняется внутри менеджера контекста transaction.atomic().

# Такой подход позволяет гарантировать атомарность операции создания объектов при 
# работе с базой данных, а также обеспечивает более высокую производительность при работе 
# с большим количеством данных.

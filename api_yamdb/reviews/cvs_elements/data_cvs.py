import csv
from django.core.management.base import BaseCommand, CommandError
from reviews.models import (Title, Category,
                            Genre, User,
                            Review, Comment,
                            GenreTitle)
from collections import OrderedDict
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
        for filename, model in default_data.items():
            with open(data_path + filename,
                      'rt', encoding='utf-8') as data_csv:
                try:
                    reader = csv.DictReader(data_csv)
                    # * для распаковки словарей в список reader
                    res = model.objects.create(model(**data)
                                               for data in reader)
                except model.DoesNotExist:
                    raise CommandError('File dosent exist' % filename)
                res.opened = False
                res.save
        self.stdout.write(
            self.style.SUCCESS('All csv_data have been done' % filename)
        )

# Если честно, то я не понимаю, что тут нужно такого писать,
# обошёл много сайтов
# Но толкового обьяснения не нашёл. Можете скинуть пж нужный сайт с инфой.
# Заранее спасибо!

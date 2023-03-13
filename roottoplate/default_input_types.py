import os
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'roottoplate.settings')
import django  # noqa: E402
django.setup()
from composter.models import InputType  # noqa:E402


def populate_input_types(file_path):
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        input_list = list(reader)

    for item in input_list:
        create_input_type(item)


def create_input_type(item):
    new_type = InputType.objects.get_or_create(name=item[0], nitrogenPercent=item[1],
                                               CNRatio=item[2], moisturePercent=item[3])
    return new_type

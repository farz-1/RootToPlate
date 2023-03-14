import os
import csv
from default_input_types import populate_input_types
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'roottoplate.settings')
import django  # noqa: E402
django.setup()
from django.contrib.auth.models import User  # noqa: E402
from composter.models import InputType, Input, InputEntry, TemperatureEntry, \
    RestaurantRequest, EnergyUsage  # noqa:E402
from datetime import datetime  # noqa:E402
from django.utils import timezone  # noqa:E402

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
INPUT_TYPES_FILEPATH = 'inputtypes.csv'
TEMPERATURES_FILEPATH = 'temperatures.csv'
INPUTS_FILEPATH = 'inputs.csv'

print(os.path.abspath('inputtypes.csv'))
print(os.getcwd())
print(os.path.getsize('inputtypes.csv'))

ABSOLUTE_PATH = '/path/to/your/file/static/db-data/inputtypes.csv'


def populate():
    populate_input_types()

    with open(TEMPERATURES_FILEPATH) as csvfile:
        reader = csv.reader(csvfile)
        temperature_entries = list(reader)

    with open(INPUTS_FILEPATH) as csvfile:
        reader = csv.reader(csvfile)
        input_entries = list(reader)

    users = [
        # users, stored as list of dictionaries
        {'username': 'kw01',
         'password': 'grass99',
         'firstName': 'Katie',
         'lastName': 'White',
         'isAdmin': True},
        {'username': 'ag23',
         'password': 'compost1',
         'firstName': 'Agatha',
         'lastName': 'Green',
         'isAdmin': False},
        {'username': 'lb212',
         'password': 'soil110',
         'firstName': 'Lucas',
         'lastName': 'Brown',
         'isAdmin': False},
        {'username': 'ab88',
         'password': '45dirt',
         'firstName': 'Amelia',
         'lastName': 'Black',
         'isAdmin': False},
    ]

    restaurant_requests = [
        # restaurant requests, stored as list of dictionaries
        {'id': '20002',
         'name': 'TEST_RESTAURANT',
         'address': '26 Vinicombe Street',
         'dateRequested': '2023-01-02 22:01:40',
         'deadline': '2023-01-30 23:00:00',
         'email': 'test@kapao.com',
         'phone': 44800829839,
         'notes': 'quick',
         'bags': 2,
         'collected': False},
    ]

    energies = [
        #  energy entries, stored as a list of dictionaries
        {'date': '2023-01-02',
         'gas': 1800,
         'electricity': 1800},
        {'date': '2023-02-02',
         'gas': 3200,
         'electricity': 2400}
    ]

    for u in users:
        new_user = create_user(u)
        print("Created profile: " + str(new_user))

    create_temperature_entries(temperature_entries)
    create_input_entries(input_entries)

    for r in restaurant_requests:
        create_restaurant_request(r)

    for e in energies:
        create_energy(e)


def create_user(data):
    # creates user
    print("creating " + data['username'] + "...")
    user = User.objects.create_user(username=data['username'],
                                    password=data['password'])
    user.first_name = data['firstName']
    user.last_name = data['lastName']
    user.is_staff = data['isAdmin']
    if data['isAdmin']:
        user.is_superuser = True
    user.save()
    return user


def create_input_entries(data):
    # creates input entry
    user = User.objects.get(username='kw01')
    count = 0
    for item in data:
        print(f'creating input entry {str(count)}...')
        input_entry = InputEntry.objects.get_or_create(entryID=count, entryTime=date(item[0] + ' 00:00:00'),
                                                       notes='initial data from Lucia', user=user)

        if item[1]:
            input_type = 'Coffee grounds'
            amount = item[1]
            create_input(count, input_type, amount)

        if item[2]:
            input_type = 'Food waste'
            amount = item[2]
            create_input(count, input_type, amount)

        if item[3]:
            input_type = 'Grass clippings'
            amount = item[3]
            create_input(count, input_type, amount)

        if item[4]:
            input_type = 'Leaves'
            amount = item[4]
            create_input(count, input_type, amount)

        if item[5]:
            input_type = 'Shrub trimmings'
            amount = item[5]
            create_input(count, input_type, amount)

        if item[6]:
            input_type = 'Wood'
            amount = item[6]
            create_input(count, input_type, amount)

        if item[7]:
            input_type = 'Hay'
            amount = item[7]
            create_input(count, input_type, amount)

        count += 1

    return input_entry


def create_input(count, input_type, amount):
    # creates input
    entry = InputEntry.objects.get(entryID=count)
    input_type = InputType.objects.get(name=input_type)
    new_input = Input.objects.get_or_create(inputEntry=entry,
                                            inputType=input_type,
                                            inputAmount=amount)
    return new_input


def create_temperature_entries(data):
    # creates temperature entry
    user = User.objects.get(username='kw01')
    count = 0
    for item in data:
        print(f'creating temp entry {str(count)}...')
        entry = TemperatureEntry.objects.get_or_create(entryID=count,
                                                       entryTime=date(item[0] + ' 00:00:00'),
                                                       probe1=item[1],
                                                       probe2=item[2],
                                                       probe3=item[3],
                                                       probe4=item[4],
                                                       notes='Initial data from Lucia',
                                                       user=user)[0]
        count += 1
    return entry


def create_restaurant_request(data):
    # creates restaurant request
    print(f'creating restaurant request {str(data["id"])}...')
    request = RestaurantRequest.objects.\
        get_or_create(requestID=data['id'],
                      name=data['name'],
                      address=data['address'],
                      dateRequested=date(data['dateRequested']),
                      deadlineDate=date(data['deadline']),
                      email=data['email'],
                      phoneNumber=data['phone'],
                      notes=data['notes'],
                      numberOfBags=data['bags'],
                      collected=data['collected'])
    return request


def create_energy(data):
    #  creates energy entry
    print('creating energy entry')
    entry = EnergyUsage.objects.get_or_create(date=data['date'],
                                              gas=data['gas'],
                                              electricity=data['electricity'])
    return entry


def date(date):
    return timezone.make_aware(datetime.strptime(date, DATE_FORMAT))


# Execution starts here
if __name__ == '__main__':
    print('Starting the composter population script...')
    populate()

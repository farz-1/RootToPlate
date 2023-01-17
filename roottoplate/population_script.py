import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'roottoplate.settings')
import django  # noqa: E402
django.setup()
from django.contrib.auth.models import User  # noqa: E402
from composter.models import InputType, Input, InputEntry, TemperatureEntry, \
    RestaurantRequest, Output  # noqa:E402


def populate():
    # input types, stored as a list of dictionaries
    input_types = [
        {'name': 'Food scraps',
         'woodChipRatio': 5,  # 5:1
         'CNRatio': 2},  # placeholder
        {'name': 'Vegetable clipping',
         'woodChipRatio': 3,  # 3:1
         'CNRatio': 2},
        {'name': 'Fresh/wet grass',
         'woodChipRatio': 6,  # 6:1
         'CNRatio': 2},
        {'name': 'Brown/dry grass',
         'woodChipRatio': 10,  # 10:1
         'CNRatio': 2},
        {'name': 'Weeds',
         'woodChipRatio': 3,  # 3:1
         'CNRatio': 2},
        {'name': 'Plank stalks',
         'woodChipRatio': 5,  # 5:1
         'CNRatio': 2},
    ]

    input_entries = [
        # input entries, stored as list of dictionaries
        {'id': 10001,
         'entryTime': '2022-12-25 23:24:54',
         'notes': 'all good',
         'user': 'ag23'},
        {'id': 10002,
         'entryTime': '2022-12-26 19:24:42',
         'notes': 'late sorry',
         'user': 'kw01'},
        {'id': 10003,
         'entryTime': '2023-01-05 05:21:19',
         'notes': 'ok composter',
         'user': 'ag23'},
    ]

    inputs = [
        # inputs, stored as list of dictionaries
        {'inputEntry': 10002,
         'inputType': 'Food scraps',
         'amount': 2},
        {'inputEntry': 10003,
         'inputType': 'Food scraps',
         'amount': 4},
        {'inputEntry': 10003,
         'inputType': 'Weeds',
         'amount': 2},
        {'inputEntry': 10001,
         'inputType': 'Brown/dry grass',
         'amount': 1},
    ]

    temperature_entries = [
        # temperature entries, stored as list of dictionaries
        {'id': 10001,
         'entryTime': '2022-12-25 21:24:54',
         'probe1': 44.6,
         'probe2': 44.7,
         'probe3': 45.7,
         'probe4': 44.9,
         'notes': 'no issues',
         'user': 'ag23'},
        {'id': 34264,
         'entryTime': '2022-12-13 06:11:44',
         'probe1': 44.2,
         'probe2': 44.4,
         'probe3': 41.7,
         'probe4': 40.9,
         'notes': 'no issues',
         'user': 'kw01'},
        {'id': 10002,
         'entryTime': '2022-12-20 20:20:20',
         'probe1': 39.6,
         'probe2': 40.9,
         'probe3': 42.5,
         'probe4': 44.0,
         'notes': 'probe 1 cold',
         'user': 'ag23'},
        {'id': 10003,
         'entryTime': '2022-11-13 13:59:18',
         'probe1': 45.0,
         'probe2': 44.6,
         'probe3': 43.9,
         'probe4': 44.1,
         'notes': 'good compost temp',
         'user': 'ab88'},
    ]

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

    outputs = [
        # outputs, stored as list of dictionaries
        {'id': '1001',
         'amount': 22.2,
         'time': '2023-01-22 21:01:00',
         'notes': 'looks good',
         'user': 'ag23'},
        {'id': '1002',
         'amount': 22.5,
         'time': '2022-11-30 04:52:43',
         'notes': 'looks good',
         'user': 'lb212'},
        {'id': '6584',
         'amount': 21.2,
         'time': '2022-12-31 23:54:54',
         'notes': 'brilliant',
         'user': 'ag23'},
        {'id': '1006',
         'amount': 23.4,
         'time': '2023-01-01 16:33:30',
         'notes': 'looks good',
         'user': 'ab88'},
        {'id': '1009',
         'amount': 27.7,
         'time': '2022-12-29 22:01:02',
         'notes': 'looks good',
         'user': 'ag23'},
    ]

    restaurant_requests = [
        # restaurant requests, stored as list of dictionaries
        {'id': '20002',
         'name': 'Ka Pao',
         'address': '26 Vinicombe Street',  # temp, using google data later?
         'dateRequested': '2023-01-02 22:01:40',
         'deadline': '2023-01-30 23:00:00',
         'email': 'kapao@kapao.com',
         'phone': 44800829839,
         'notes': 'quick',
         'bags': 2,
         'collected': False},
    ]

    for u in users:
        new_user = create_user(u)
        print("Created profile: " + str(new_user))

    for o in outputs:
        create_output(o)

    for it in input_types:
        create_input_types(it)

    for ti in temperature_entries:
        create_temperature_entry(ti)

    for ie in input_entries:
        create_input_entry(ie)

    for i in inputs:
        create_input(i)

    for r in restaurant_requests:
        create_restaurant_request(r)


def create_user(data):
    # creates user
    print("creating " + data['username'] + "...")
    user = User.objects.create_user(username=data['username'],
                                    password=data['password'])
    user.first_name = data['firstName']
    user.last_name = data['lastName']
    user.is_staff = data['isAdmin']
    user.save()
    return user


def create_input_types(data):
    # creates input type
    print("creating " + data['name'] + " input type...")
    input_type = InputType.objects.\
        get_or_create(name=data['name'],
                      woodChipRatio=data['woodChipRatio'],
                      CNRatio=data['CNRatio'])[0]
    return input_type


def create_input_entry(data):
    # creates input entry
    print("creating input entry " + str(data['id']) + "...")
    user = User.objects.get(username=data['user'])
    input_entry = InputEntry.objects.get_or_create(entryID=data['id'],
                                                   entryTime=data['entryTime'],
                                                   notes=data['notes'],
                                                   user=user)
    return input_entry


def create_input(data):
    # creates input
    entry = InputEntry.objects.get(entryID=data['inputEntry'])
    input_type = InputType.objects.get(name=data['inputType'])
    new_input = Input.objects.get_or_create(inputEntry=entry,
                                            inputType=input_type,
                                            inputAmount=data['amount'])
    return new_input


def create_temperature_entry(data):
    # creates temperature entry
    print("creating temperature entry " + str(data['id']) + "...")
    user = User.objects.get(username=data['user'])
    entry = TemperatureEntry.objects.get_or_create(entryID=data['id'],
                                                   entryTime=data['entryTime'],
                                                   probe1=data['probe1'],
                                                   probe2=data['probe2'],
                                                   probe3=data['probe3'],
                                                   probe4=data['probe4'],
                                                   notes=data['notes'],
                                                   user=user)[0]
    return entry


def create_output(data):
    # creates output
    print("creating output " + str(data['id']) + "...")
    user = User.objects.get(username=data['user'])
    output = Output.objects.get_or_create(outputID=data['id'],
                                          amount=data['amount'],
                                          time=data['time'],
                                          notes=data['notes'],
                                          user=user)[0]
    return output


def create_restaurant_request(data):
    # creates restaurant request
    print(f'creating restaurant request {str(data["id"])}...')
    request = RestaurantRequest.objects.\
        get_or_create(requestID=data['id'],
                      name=data['name'],
                      address=data['address'],
                      dateRequested=data['dateRequested'],
                      deadlineDate=data['deadline'],
                      email=data['email'],
                      phoneNumber=data['phone'],
                      notes=data['notes'],
                      numberOfBags=data['bags'],
                      collected=data['collected'])
    return request


# Execution starts here
if __name__ == '__main__':
    print('Starting the composter population script...')
    populate()

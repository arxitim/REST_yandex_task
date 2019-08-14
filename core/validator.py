from datetime import date


def name_valid(name):
    if len(name) < 2:
        raise ValueError("Неверный формат записи имени")
    for word in name:
        if not word.isalpha():
            raise ValueError("Имя не может содержать цифры")


def gender_valid(gender):
    if gender not in ['male', 'female']:
        raise ValueError("Пол может быть только male или female")


def birth_date_valid(birth_date):
    if len(birth_date) != 3:
        raise ValueError("Неверный формат записи даты")
    try:
        date(int(birth_date[2]), int(birth_date[1]), int(birth_date[0]))
    except ValueError:
        raise ValueError("Такой даты не существует")


def town_valid(town):
    if not (town.isalpha() or town.isdigit()):
        raise ValueError("Город должна состоять миниму из одной цифры или буквы")


def street_valid(street):
    if not (street.isalpha() or street.isdigit()):
        raise ValueError("Улица должна состоять миниму из одной цифры или буквы")


def building_valid(building):
    if not (building.isalpha() or building.isdigit()):
        raise ValueError("Адрес должна состоять миниму из одной цифры или буквы")


def apartment_valid(apartment):
    if (int(apartment) != float(apartment)) or (int(apartment) <= 0):
        raise ValueError("Номер квартиры должен быть целым числом")


def duplicates_valid(data, name):
    if len(data) != len(set(data)):
        raise ValueError(f"{name} не уникален в рамках одной выгрузки")


def ids_valid(data):
    if not all(isinstance(_id, int) for _id in data) or [True for _id in data if _id <= 0]:
        raise ValueError("Все элементы поля relative (все идентификаторы жителей) должны быть int > 0")


def post_validate(data):
    """
    Универсальный валидатор для полей одного жителя

    На вход подается python-object
    """

    if (len(data) != 1) or ('citizens' not in data):
        raise ValueError("Неверный формат данных")

    all_citizens = [citizen['citizen_id'] for citizen in data['citizens']]

    duplicates_valid(all_citizens, 'citizen_id')
    ids_valid(all_citizens)

    for citizen in data['citizens']:

        if citizen['relatives'] is not None:
            duplicates_valid(citizen['relatives'], 'relative')
            for relative in citizen['relatives']:
                try:
                    person = next(x for x in data['citizens'] if x['citizen_id'] == relative)
                except StopIteration:
                    raise ValueError('Человек не может состоять в отношениях с человеком не из этой выгрузки')

                if citizen['citizen_id'] not in person['relatives']:
                    raise ValueError("Отношения у жителей в одной выгрузке должны быть двусторонними")

                if relative == citizen['citizen_id']:
                    raise ValueError('У человека не может быть взаимоотношений между самим собой')
        else:
            raise ValueError('Поле relatives не должно быть null')

        name_valid(citizen['name'].split())

        gender_valid(citizen['gender'])

        birth_date_valid(citizen['birth_date'].split('.'))

        town_valid(citizen['town'][0])

        street_valid(citizen['street'][0])

        building_valid(citizen['building'][0])

        apartment_valid(citizen['apartment'])

    return data


def patch_validate(data, citizen_id):
    """
    Валидатор для PATCH.

    Принимает на вход python-object

    """
    fields = {'name', 'gender', 'birth_date', 'relatives', 'town', 'street', 'building', 'apartment'}

    if (len(data) > len(set(data)))\
            or not set(data).issubset(fields) \
            or not data:
        raise ValueError('В запросе есть некорректные поля (или запрос оказался пустым)')

    if 'relatives' in data:
        if data['relatives'] is None:
            raise ValueError('Поле relatives не должно быть null')

        if citizen_id in data['relatives']:
            raise ValueError('У жителя не может быть отношений с самим собой')

        ids_valid(data['relatives'])

        duplicates_valid(data['relatives'], 'relative')

    name_valid(data.get('name', "Иван Иванов").split())

    gender_valid(data.get('gender', 'male'))

    birth_date_valid(data.get('birth_date', '23.11.1986').split('.'))

    town_valid(data.get('town', 'Москва')[0])

    street_valid(data.get('street', 'Иосифа Бродского')[0])

    building_valid(data.get('building', '1')[0])

    apartment_valid(data.get('apartment', 1))

    # не валидируем поле relatives, сделаем это во View

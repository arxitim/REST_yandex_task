from datetime import date
from string import punctuation


FIELDS = {'name', 'gender', 'birth_date', 'relatives', 'town', 'street', 'building', 'apartment'}


def name_valid(name):
    name = name.split()
    if len(name) < 2 or len(name) > 3:
        raise ValueError("Неверный формат записи имени")
    for word in name:
        if not word.isalpha():
            raise ValueError("Имя не может содержать цифры")


def gender_valid(gender):
    if gender not in ['male', 'female']:
        raise ValueError("Пол может быть только male или female")


def birth_date_valid(birth_date):
    birth_date = birth_date.split('.')
    if len(birth_date) != 3:
        raise ValueError("Неверный формат записи даты")
    try:
        date(int(birth_date[2]), int(birth_date[1]), int(birth_date[0]))
    except ValueError:
        raise ValueError("Такой даты не существует")


def town_valid(town):
    if not isinstance(town, str):
        raise ValueError('Название города должно быть строкой')
    if not (town[0].isalpha() or town[0].isdigit()):
        raise ValueError("Город должна состоять миниму из одной цифры или буквы")
    for char in town:
        if (char in punctuation) and char != '-':
            raise ValueError("Название города не может содержать знаки пунктуации")


def street_valid(street):
    if not isinstance(street, str):
        raise ValueError('Название улицы должно быть строкой')
    if not (street[0].isalpha() or street[0].isdigit()):
        raise ValueError("Улица должна состоять миниму из одной цифры или буквы")
    for char in street:
        if (char in punctuation) and char not in ['-', '/']:
            raise ValueError("Название улицы не может содержать знаки пунктуации")


def building_valid(building):
    if not isinstance(building, str):
        raise ValueError('Название улицы должно быть строкой')
    if not (building[0].isalpha() or building[0].isdigit()):
        raise ValueError("Адрес должна состоять миниму из одной цифры или буквы")
    for char in building:
        if (char in punctuation) and char not in ['-', '/', '.', ',']:
            raise ValueError("Название улицы не может содержать знаки пунктуации")


def apartment_valid(apartment):
    if (int(apartment) != float(apartment)) or (int(apartment) <= 0):
        raise ValueError("Номер квартиры должен быть целым числом > 0")


def other_fields_valid(data):
    """
    All fields are validated here except 'citizen_id', 'relatives'

    :type data: dict
    :rtype: None
    """
    for field in data:
        if field in ['relatives', 'citizen_id']:
            continue

        # earlier we have checked that the value which gets in "eval" is a subset of "safe" words
        validator = eval(field + '_valid')
        validator(data[field])


def duplicates_valid(data, name):
    if len(data) != len(set(data)):
        raise ValueError(f"{name} не уникален в рамках одной выгрузки")


def ids_valid(data):
    if not all(isinstance(_id, int) for _id in data) or [True for _id in data if _id <= 0]:
        raise ValueError("Все элементы поля relative (все идентификаторы жителей) должны быть int > 0")


def post_validate(data):
    """
    Validator for POST request.

    :type data: dict
    :rtype: None
    """

    if (len(data) != 1) or ('citizens' not in data):
        raise ValueError("Неверный формат данных")

    all_citizens = [citizen['citizen_id'] for citizen in data['citizens']]

    duplicates_valid(all_citizens, 'citizen_id')
    ids_valid(all_citizens)

    for citizen in data['citizens']:
        if 'appartement' in citizen:
            citizen['apartment'] = citizen['appartement']
            del citizen['appartement']

        if (FIELDS | {'citizen_id'}) != set(citizen.keys()):
            raise ValueError('В запросе есть некорректные поля (или запрос оказался пустым)')

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

        other_fields_valid(citizen)


def patch_validate(data, citizen_id):
    """
    Validator for PATCH request.

    :type data: dict
    :type citizen_id: int
    :rtype: None
    """
    if 'appartement' in data:
        data['apartment'] = data['appartement']
        del data['appartement']

    if not set(data).issubset(FIELDS) or not data:
        raise ValueError('В запросе есть некорректные поля (или запрос оказался пустым)')

    if 'relatives' in data:
        if data['relatives'] is None:
            raise ValueError('Поле relatives не должно быть null')

        if citizen_id in data['relatives']:
            raise ValueError('У жителя не может быть отношений с самим собой')

        ids_valid(data['relatives'])
        duplicates_valid(data['relatives'], 'relative')

    other_fields_valid(data)

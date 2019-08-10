from datetime import date


def post_validate(data):
    """
    Универсальный валидатор для полей одного жителя

    На вход подается python-object
    """

    if (len(data) != 1) or ('citizens' not in data):
        raise ValueError("Неверный формат данных")

    for citizen in data['citizens']:
        if sorted(citizen.keys()) != ['apartment', 'birth_date', 'building', 'citizen_id',
                                      'gender', 'name', 'relatives', 'street', 'town']:
            raise ValueError("В полученных данных у одного или нескольких жителей нет всех необходимых полей")

        if (int(citizen['apartment']) != float(citizen['apartment'])) or (int(citizen['apartment']) <= 0):
            raise ValueError("Номер квартиры должен быть целым числом")

        birthdate = citizen['birth_date'].split('.')
        if len(birthdate) != 3:
            raise ValueError("Неверный формат записи даты")
        try:
            date(int(birthdate[2]), int(birthdate[1]), int(birthdate[0]))
        except ValueError:
            raise ValueError("Такой даты не существует")

        if (int(citizen['citizen_id']) != float(citizen['citizen_id'])) or (int(citizen['citizen_id']) <= 0):
            raise ValueError("citizen_id должен быть целым числом и больше чем ноль")
        else:
            if len([True for person in data['citizens'] if person['citizen_id'] == citizen['citizen_id']]) != 1:
                raise ValueError("citizen_id не уникален в рамках одной выгрузки")

        if citizen['gender'] not in ['male', 'female']:
            raise ValueError("Пол может быть только male или female")

        name_of_citizen = citizen['name'].split()
        if len(name_of_citizen) < 2:
            raise ValueError("Неверный формат записи имени")
        for word in name_of_citizen:
            if not word.isalpha():
                raise ValueError("Имя не может содержать цифры")

        if not (citizen['street'][0].isalpha() or citizen['street'][0].isdigit()):
            raise ValueError("Улица должна состоять миниму из одной цифры или буквы")

        if not (citizen['town'][0].isalpha() or citizen['town'][0].isdigit()):
            raise ValueError("Город должна состоять миниму из одной цифры или буквы")

        if not (citizen['building'][0].isalpha() or citizen['building'][0].isdigit()):
            raise ValueError("Адрес должна состоять миниму из одной цифры или буквы")

        if citizen['relatives']:
            for relative in citizen['relatives']:
                try:
                    person = next(x for x in data['citizens'] if x['citizen_id'] == relative)
                except StopIteration:
                    raise ValueError('Человек не может состоять в отношениях с человеком не из этой выгрузки')

                if citizen['citizen_id'] not in person['relatives']:
                    raise ValueError("Отношений у жителей в одной выгрузке должны быть двусторонними")

                if relative == citizen['citizen_id']:
                    raise ValueError('У человека не может быть взаимоотношений между самим собой')

    return data


def patch_validate(data):

    if (len(data) == len(set(data))) and set(data).issubset({
                                                            'name', 'gender', 'birth_date',
                                                            'relatives', 'town',
                                                            'street', 'building',
                                                            'apartment'}):
        raise ValueError

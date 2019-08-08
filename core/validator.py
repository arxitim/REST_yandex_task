from datetime import date


def post_validate(data):
    """
    Универсальный валидатор для полей одного жителя

    На вход подается python-object
    """

    if (len(data) != 1) or ('citizens' not in data):
        raise ValueError
    print('SUCCES')

    for citizen in data['citizens']:
        if sorted(citizen.keys()) != ['apartment', 'birth_date', 'building', 'citizen_id',
                                      'gender', 'name', 'relatives', 'street', 'town']:
            raise ValueError

        if (int(citizen['apartment']) != float(citizen['apartment'])) or (int(citizen['apartment']) <= 0):
            raise ValueError
        else:
            # на всякий случай переводим в int
            citizen['apartment'] = int(citizen['apartment'])
            print('SUCCES')

        birthdate = citizen['birth_date'].split('.')
        if len(birthdate) != 3:
            raise ValueError
        try:
            birthdate = date(int(birthdate[2]), int(birthdate[1]), int(birthdate[0]))
            print('SUCCES')
        except ValueError:
            raise ValueError

        if (int(citizen['citizen_id']) != float(citizen['citizen_id'])) or (int(citizen['citizen_id']) <= 0):
            raise ValueError
        else:
            if len([True for person in data['citizens'] if person['citizen_id'] == citizen['citizen_id']]) != 1:
                # Id не уникален
                raise ValueError

            # на всякий случай переводим в int
            citizen['citizen_id'] = int(citizen['citizen_id'])
        print('SUCCES')

        if citizen['gender'] not in ['male', 'female']:
            raise ValueError
        print('SUCCES')

        name_of_citizen = citizen['name'].split()
        if len(name_of_citizen) < 2:
            raise ValueError
        for word in name_of_citizen:
            # имя не может состоять из цифр
            if not word.isalpha():
                raise ValueError
        print('SUCCES')

        if not (citizen['street'][0].isalpha() or citizen['street'][0].isdigit()):
            raise ValueError
        print('SUCCES')

        if not(citizen['town'][0].isalpha() or citizen['town'][0].isdigit()):
            raise ValueError
        print('SUCCES')

        if not (citizen['building'][0].isalpha() or citizen['building'][0].isdigit()):
            raise ValueError
        print('SUCCES')

        if citizen['relatives']:
            for relative in citizen['relatives']:
                person = next(x for x in data['citizens'] if x['citizen_id'] == relative)
                if citizen['citizen_id'] not in person['relatives']:
                    raise ValueError
                    # отношения должны быть двусторонними
        print('SUCCES')

    return data

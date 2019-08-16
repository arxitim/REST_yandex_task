from django.http import HttpResponse
from django.views import View
from .models import Import
from .validator import post_validate, patch_validate
from datetime import date
from numpy import percentile

import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# 1
@method_decorator(csrf_exempt, name='dispatch')
class SaveImport(View):
    """
    Accepts a set of citizens' data (json)
    and saves it with a unique import_id identifier.

    """
    def post(self, request):
        try:
            document = json.loads(request.body)
            post_validate(document)
        except (TypeError, ValueError, KeyError, json.JSONDecodeError, IndexError, AttributeError) as exc:
            return HttpResponse(exc.args[0], status=400)

        # по-моему это бессмысленный кусок кода, но ТЗ есть ТЗ
        document['data'] = document.pop('citizens')
        # -----------------------------------------------------

        data = json.dumps(document, indent=2, ensure_ascii=False)

        payload = Import.objects.create(value=data)
        return HttpResponse(json.dumps({"data": {"import_id": payload.pk}}, indent=2),
                            content_type='application/json', status=201)


# 2
@method_decorator(csrf_exempt, name='dispatch')
class ChangeData(View):
    """
    Changes the citizen information in the specified data set.

    """
    def patch(self, request, import_id, citizen_id):

        try:
            # берем нужный импорт
            my_import = Import.objects.get(pk=import_id)
        except Import.DoesNotExist:
            return HttpResponse('Такого импорта не существует')

        # из него берем нужных людей
        all_citizens = json.loads(my_import.value)['data']
        #  и их ids соответсвенно
        citizens_ids = [_id['citizen_id'] for _id in all_citizens]

        # находим интересуещего нас жителя
        try:
            citizen = next(x for x in all_citizens if x['citizen_id'] == citizen_id)
        except StopIteration:
            return HttpResponse(status=400)

        # собираемся его пропатчить
        patch_citizen = all_citizens.pop(all_citizens.index(citizen))

        try:
            patch_data = json.loads(request.body)
            patch_validate(patch_data, citizen_id)
        except (json.JSONDecodeError, ValueError, TypeError, IndexError, AttributeError, KeyError) as exc:
            return HttpResponse(exc.args[0], status=400)

        # приступаем к патчингу
        for key in patch_data:
            if key == 'relatives':
                for relative in patch_data['relatives']:
                    if relative not in citizens_ids:
                        return HttpResponse('Отношений с данным id быть не может, так как его нет в данной выгрузке')

                # удалить все существующие:
                for relative in patch_citizen['relatives']:
                    new_relative = next(x for x in all_citizens if x['citizen_id'] == relative)
                    all_citizens[all_citizens.index(new_relative)]['relatives'].remove(citizen_id)

                # если апдэйтнулись родственные связи
                if patch_data['relatives']:
                    for relative in patch_data['relatives']:
                        new_relative = next(x for x in all_citizens if x['citizen_id'] == relative)
                        all_citizens[all_citizens.index(new_relative)]['relatives'].append(citizen_id)

            patch_citizen[key] = patch_data[key]

        # добавляем обратно в список жителей
        all_citizens.append(patch_citizen)

        # сохраняем обратно в базу
        my_import.value = json.dumps({"data": all_citizens}, ensure_ascii=False, indent=2)
        my_import.save()

        return HttpResponse(json.dumps({"data": patch_citizen}, ensure_ascii=False, indent=2),
                            content_type='application/json', status=200)


# 3
class GetData(View):
    """
    Returns the list of citizens for the specified data set.

    """
    def get(self, request, import_id):
        try:
            data = Import.objects.get(pk=import_id).value
        except Import.DoesNotExist:
            return HttpResponse('Импорта с таким номером не существует', status=400)

        return HttpResponse(data, content_type='application/json', status=200)


class GetPresents(View):
    """
    Returns citizens and the number of gifts they will buy to their closest relatives.
    The answer is grouped by months from the specified data set.

    """

    # test
    def get(self, request, import_id):
        try:
            data = Import.objects.get(pk=import_id).value
            all_citizens = json.loads(data)['data']
        except Import.DoesNotExist:
            return HttpResponse('Импорта с таким номером не существует', status=400)

        answer = {
            "1": [], "2": [], "3": [], "4": [], "5": [], "6": [],
            "7": [], "8": [], "9": [], "10": [], "11": [], "12": []
        }


        for citizen in all_citizens:
            # вспомогательная структура
            tmp_birthdays = dict()

            for relative in citizen['relatives']:
                target = next(x for x in all_citizens if x['citizen_id'] == relative)
                birthday = target['birth_date'].split('.')[1]
                if birthday[0] == '0':
                    birthday = birthday[1]

                if birthday not in tmp_birthdays:
                    tmp_birthdays[birthday] = {'citizen_id': citizen['citizen_id'], 'presents': 1}
                else:
                    tmp_birthdays[birthday]['presents'] += 1

            for month in tmp_birthdays:
                answer[month].append(tmp_birthdays[month])

        # EZ PZ LEMON SQUIZY
        return HttpResponse(json.dumps(answer, ensure_ascii=False, indent=2),
                                    content_type='application/json', status=200)


class GetStats(View):
    """
    Returns the statistics by city for the data set by age of citizens.

    """

    # test
    def get(self, request, import_id):

        def calculate_age(born):
            today = date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        try:
            data = Import.objects.get(pk=import_id).value
            all_citizens = json.loads(data)['data']
        except Import.DoesNotExist:
            return HttpResponse('Импорта с таким номером не существует', status=400)

        ages = dict()

        for citizen in all_citizens:

            birth_date = date(*[int(value) for value in citizen['birth_date'].split('.')[::-1]])

            if citizen['town'] not in ages:
                ages[citizen['town']] = [calculate_age(birth_date)]
            else:
                ages[citizen['town']].append(calculate_age(birth_date))

        answer = []
        for town in ages:
            stats = percentile(ages[town], q=[50, 75, 99], interpolation='linear')
            answer.append({'town': town, 'p50': stats[0], 'p75': stats[1], 'p99': stats[2]})


        return HttpResponse(json.dumps({"data": answer}, ensure_ascii=False, indent=2),
                            content_type='application/json', status=200)









class TestClass(View):
    def get(self, request, item_id):

        try:
            data = Import.objects.get(pk=item_id).value

        except Import.DoesNotExist:
            return HttpResponse(status=400, content='Импорта с таким номером не существует')

        return HttpResponse(data, content_type='application/json')
from django.http import HttpResponse
from django.views import View
from .models import Import
from .validator import post_validate, patch_validate

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

        # находим интересуещего нас жителя
        citizen = next(x for x in all_citizens if x['citizen_id'] == citizen_id)

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
                citizens_ids = [_id['citizen_id'] for _id in all_citizens]
                for relative in patch_data['relatives']:
                    if relative not in citizens_ids:
                        return HttpResponse('Отношений с данным id быть не может, так как его нет в данной выгрузке')

                # удалить все существующие:
                for relative in patch_citizen['relatives']:
                    new_relative = next(x for x in all_citizens if x['citizen_id'] == relative)
                    all_citizens[all_citizens.index(new_relative)][key].remove(citizen_id)

                # если апдэйтнулись родственные связи
                if patch_data[key]:
                    for relative in patch_data[key]:
                        new_relative = next(x for x in all_citizens if x['citizen_id'] == relative)
                        all_citizens[all_citizens.index(new_relative)][key].append(citizen_id)

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
            return HttpResponse(status=400, content='Импорта с таким номером не существует')

        return HttpResponse(data, content_type='application/json', status=200)


class GetPresents(View):
    """
    Returns citizens and the number of gifts they will buy to their closest relatives.
    The answer is grouped by months from the specified data set.

    """

    # test
    def get(self, request, import_id):
        return HttpResponse(f'Get presents data for {import_id}')


class GetStats(View):
    """
    Returns the statistics by city for the data set by age of citizens.

    """

    # test
    def get(self, request, import_id):
        return HttpResponse(f'Get stats data for {import_id}')


class TestClass(View):
    def get(self, request, item_id):

        try:
            data = Import.objects.get(pk=item_id).value

        except Import.DoesNotExist:
            return HttpResponse(status=400, content='Импорта с таким номером не существует')

        return HttpResponse(data, content_type='application/json')
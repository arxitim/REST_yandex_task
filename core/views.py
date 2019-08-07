from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Import

from pprint import pprint
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# patch можно определить как метод класса все норм


# 1
@method_decorator(csrf_exempt, name='dispatch')
class SaveImport(View):
    """
    Принимает на вход набор с данными о жителях (json)
    и сохраняет его с уникальным идентификатором import_id.

    """
    def post(self, request):

        document = json.loads(request.body)

        # по-моему это бессмысленный кусок кода, но ТЗ есть ТЗ
        document['data'] = document.pop('citizens')
        # -----------------------------------------------------

        data = json.dumps(document, indent=4, ensure_ascii=False)

        payload = Import.objects.create(value=data)
        return HttpResponse(payload.pk, status=200)


# 2
@method_decorator(csrf_exempt, name='dispatch')
class ChangeData(View):
    """
    Изменяет инормацию о жителе в указанном наборе данных.

    """
    def patch(self, request, import_id, citizen_id):
        all_citizens = json.loads(Import.objects.get(pk=import_id).value)['data']

        # находим интересуещего нас жителя
        citizen = next(x for x in all_citizens if x['citizen_id'] == citizen_id)

        print(all_citizens.index(citizen))

        patch_data = json.loads(request.body)

        return HttpResponse('ok', status=200)

    # test
    def get(self, request, import_id, citizen_id):
        return HttpResponse(f'Change data for {import_id}  {citizen_id}')


# 3
class GetData(View):
    """
    Возвращает список жителей для указанного набора данных.

    """
    def get(self, request, import_id):
        try:
            data = Import.objects.get(pk=import_id).value
        except Import.DoesNotExist:
            return HttpResponse(status=404, content='Импорта с таким номером не существует')

        return HttpResponse(data, content_type='application/json', status=200)


class GetPresents(View):
    """
    Возвращает жителей и кол-во подарков, которые они будут покупать
    своим ближайшим родственникам.
    Ответ сгруппирован по месяцам из указанного набора данных

    """

    # test
    def get(self, request, import_id):
        return HttpResponse(f'Get presents data for {import_id}')


class GetStats(View):
    """
    Возвращает статистику по городам для набора данных
    в разрезе возраста жителей.

    """

    # test
    def get(self, request, import_id):
        return HttpResponse(f'Get stats data for {import_id}')


class TestClass(View):
    def get(self, request, item_id):

        try:
            data = Import.objects.get(pk=item_id).value

        except Import.DoesNotExist:
            return HttpResponse(status=404, content='Импорта с таким номером не существует')

        return HttpResponse(data, content_type='application/json')
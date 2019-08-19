import json
from random import choice
from time import time

from django.test import TestCase


class OverheadTest(TestCase):
    def setUp(self) -> None:
        a = {
            "citizen_id": None,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5", "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "26.12.1986",
            "gender": "male",
            "relatives": []
        }

        b = {
            "citizen_id": None,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Сергей Иванович",
            "birth_date": "17.04.1997",
            "gender": "male",
            "relatives": []
        }
        c = {
            "citizen_id": None,
            "town": "Керчь",
            "street": "Иосифа Бродского",
            "building": "2",
            "apartment": 11,
            "name": "Романова Мария Леонидовна",
            "birth_date": "22.11.1986",
            "gender": "female",
            "relatives": []
        }

        data = {'citizens': []}

        for i in range(1, 10002):
            citizen = choice([a.copy(), b.copy(), c.copy()])
            citizen['citizen_id'] = i
            data['citizens'].append(citizen)

        self.data = data

    def test_timeout(self):
        start = time()
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')

        finish = int(time() - start)
        self.assertEqual(finish < 10, True)

    def test_status_check(self):
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 201)

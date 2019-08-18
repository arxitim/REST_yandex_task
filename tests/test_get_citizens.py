import json

from django.test import TestCase
from core.models import Import


class GetTest(TestCase):
    def setUp(self) -> None:
        data = [
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5", "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [2]
            },
            {
                "citizen_id": 2,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Сергей Иванович",
                "birth_date": "17.04.1997",
                "gender": "male",
                "relatives": [1]
            },
            {
                "citizen_id": 3,
                "town": "Керчь",
                "street": "Иосифа Бродского",
                "building": "2",
                "apartment": 11,
                "name": "Романова Мария Леонидовна",
                "birth_date": "22.11.1986",
                "gender": "female",
                "relatives": []
            }
        ]

        Import.objects.create(value=json.dumps(data, ensure_ascii=False, indent=2))

    def test_get_citizens(self):
        answer = self.client.get('/imports/1/citizens')
        self.assertEqual(answer.status_code, 200)

    def test_get_doesnt_exist_import(self):
        answer = self.client.get('/imports/99/citizens')
        self.assertEqual(answer.status_code, 400)


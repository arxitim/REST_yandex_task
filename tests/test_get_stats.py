import json

from django.test import TestCase
from core.models import Import


class GetStats(TestCase):
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
                "relatives": [2, 3]
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
                "relatives": [1]
            },
            {
                "citizen_id": 4,
                "town": "Таганрог",
                "street": "Ленина",
                "building": "1",
                "apartment": 7,
                "name": "Петрова Мария Ивановна",
                "birth_date": "12.05.1974",
                "gender": "female",
                "relatives": []

            }
        ]
        a = Import.objects.create(value=json.dumps(data, ensure_ascii=False, indent=2))

    def test_get_stats(self):
        expectations = {
                        "data": [
                            {
                              "town": "Москва",
                              "p50": 27.0,
                              "p75": 29.5,
                              "p99": 31.9
                            },
                            {
                              "town": "Керчь",
                              "p50": 32.0,
                              "p75": 32.0,
                              "p99": 32.0
                            },
                            {
                              "town": "Таганрог",
                              "p50": 45.0,
                              "p75": 45.0,
                              "p99": 45.0
                            }
                          ]
                        }

        expectations = json.dumps(expectations, ensure_ascii=False, indent=2)

        answer = self.client.get('/imports/1/towns/stat/percentile/age')
        self.assertEqual(answer._container[0].decode(), expectations)

    def test_get_doesnt_exist_stats(self):
        answer = self.client.get('/imports/99/citizens/birthdays')
        self.assertEqual(answer.status_code, 400)


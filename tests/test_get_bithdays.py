import json

from django.test import TestCase
from core.models import Import


class GetBirthdays(TestCase):
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
            }
        ]
        a = Import.objects.create(value=json.dumps(data, ensure_ascii=False, indent=2))

    def test_get_birthdays(self):
        expectations = {"data": {
                          "1": [],
                          "2": [],
                          "3": [],
                          "4": [
                            {
                              "citizen_id": 1,
                              "presents": 1
                            }
                          ],
                          "5": [],
                          "6": [],
                          "7": [],
                          "8": [],
                          "9": [],
                          "10": [],
                          "11": [
                            {
                              "citizen_id": 1,
                              "presents": 1
                            }
                          ],
                          "12": [
                            {
                              "citizen_id": 2,
                              "presents": 1
                            },
                            {
                              "citizen_id": 3,
                              "presents": 1
                            }
                          ]
                        }
        }
        expectations = json.dumps(expectations, indent=2)

        answer = self.client.get('/imports/1/citizens/birthdays')
        self.assertEqual(answer._container[0].decode(), expectations)

    def test_get_doesnt_exist_birthdays(self):
        answer = self.client.get('/imports/99/citizens/birthdays')
        self.assertEqual(answer.status_code, 400)


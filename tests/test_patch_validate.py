import json

from django.test import TestCase
from core.models import Import


class PatchTest(TestCase):
    def setUp(self) -> None:
        citizens = [
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
                "name": "Романова Мария",
                "birth_date": "22.11.1986",
                "gender": "female",
                "relatives": []
            }
        ]

        citizens = json.dumps(citizens, ensure_ascii=False, indent=2)

        Import.objects.create(value=citizens)
        
        self.data = {
                "town": "Керчь",
                "street": "Иосифа Бродского",
                "building": "2",
                "apartment": 11,
                "name": "Романова Мария",
                "birth_date": "22.11.1986",
                "gender": "female",
                "relatives": []
            }

    def test_its_ok_1(self):
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 200)

    def test_wrong_format_1(self):
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps({"citizens": None}, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_format_2(self):
        self.data['wrong'] = "wrong_field"
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_format_3(self):
        a = self.client.patch(path='/imports/1/citizens/3', data='Wrong information',  content_type='string')
        self.assertEqual(a.status_code, 400)

    def test_wrong_town_1(self):
        self.data['town'] = ""
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_town_2(self):
        self.data['town'] = "!."
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_town_3(self):
        self.data['town'] = None
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_town_4(self):
        self.data['town'] = ['Wrong']
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_street_1(self):
        self.data['street'] = ""
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_street_2(self):
        self.data['street'] = "!."
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_street_3(self):
        self.data['street'] = None
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_street_4(self):
        self.data['street'] = ['Wrong']
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_building_1(self):
        self.data['building'] = ""
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_building_2(self):
        self.data['building'] = "!."
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_building_3(self):
        self.data['building'] = None
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_building_4(self):
        self.data['building'] = ['Wrong']
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_1(self):
        self.data['apartment'] = 0
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_2(self):
        self.data['apartment'] = -1
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_3(self):
        self.data['apartment'] = 1.5
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_4(self):
        self.data['apartment'] = 'apartment'
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_5(self):
        self.data['apartment'] = None
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_6(self):
        self.data['apartment'] = ""
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_1(self):
        self.data['name'] = ""
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_2(self):
        self.data['name'] = "!."
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_3(self):
        self.data['name'] = None
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_4(self):
        self.data['name'] = ['Wrong']
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_5(self):
        self.data['name'] = "Великий Могучий Русский Язык"
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_1(self):
        self.data['birth_date'] = ""
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_2(self):
        self.data['birth_date'] = "!."
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_3(self):
        self.data['birth_date'] = None
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_4(self):
        self.data['birth_date'] = ['Wrong']
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_5(self):
        self.data['name'] = "Великий Могучий Русский Язык"
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_6(self):
        self.data['name'] = 15
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_7(self):
        self.data['name'] = '32.02.1999'
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_1(self):
        self.data['gender'] = ""
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_2(self):
        self.data['gender'] = "!."
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_3(self):
        self.data['gender'] = None
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_4(self):
        self.data['gender'] = ['Wrong']
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_5(self):
        self.data['gender'] = ['male']
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_1(self):
        self.data['relatives'] = None
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_2(self):
        self.data['relatives'] = [None, None]
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_3(self):
        self.data['relatives'] = 1
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_4(self):
        self.data['relatives'] = ['a', 'b']
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_5(self):
        self.data['relatives'] = [4]
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_6(self):
        self.data['relatives'] = [3]
        a = self.client.patch(path='/imports/1/citizens/3', data=json.dumps(self.data, ensure_ascii=False),
                              content_type='application/json')
        self.assertEqual(a.status_code, 400)


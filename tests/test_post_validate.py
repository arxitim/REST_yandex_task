import json

from django.test import TestCase


class PostTest(TestCase):
    def setUp(self) -> None:
        self.data = {"citizens": [
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
                "name": "Романова Мария",
                "birth_date": "22.11.1986",
                "gender": "female",
                "relatives": [1]
            }
        ]
        }

    def test_its_ok(self):
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 201)

    def test_wrong_format_1(self):
        a = self.client.post(path='/imports', data=json.dumps({"citizens": None}, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_format_2(self):
        self.data['citizens'][2].pop('relatives')
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_format_3(self):
        a = self.client.post(path='/imports', data='Wrong information', content_type='string')
        self.assertEqual(a.status_code, 400)

    def test_wrong_id_1(self):
        self.data['citizens'][2]['citizen_id'] = 0
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_id_2(self):
        self.data['citizens'][2]['citizen_id'] = -1
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_id_3(self):
        self.data['citizens'][2]['citizen_id'] = 1.5
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_id_4(self):
        self.data['citizens'][2]['citizen_id'] = 'id'
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_id_5(self):
        self.data['citizens'][2]['citizen_id'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_id_6(self):
        self.data['citizens'][2]['citizen_id'] = ""
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_town_1(self):
        self.data['citizens'][2]['town'] = ""
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_town_2(self):
        self.data['citizens'][2]['town'] = "!."
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_town_3(self):
        self.data['citizens'][2]['town'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_town_4(self):
        self.data['citizens'][2]['town'] = ['Wrong']
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_street_1(self):
        self.data['citizens'][2]['street'] = ""
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_street_2(self):
        self.data['citizens'][2]['street'] = "!."
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_street_3(self):
        self.data['citizens'][2]['street'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_street_4(self):
        self.data['citizens'][2]['street'] = ['Wrong']
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_building_1(self):
        self.data['citizens'][2]['building'] = ""
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_building_2(self):
        self.data['citizens'][2]['building'] = "!."
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_building_3(self):
        self.data['citizens'][2]['building'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_building_4(self):
        self.data['citizens'][2]['building'] = ['Wrong']
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_1(self):
        self.data['citizens'][2]['apartment'] = 0
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_2(self):
        self.data['citizens'][2]['apartment'] = -1
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_3(self):
        self.data['citizens'][2]['apartment'] = 1.5
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_4(self):
        self.data['citizens'][2]['apartment'] = 'apartment'
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_5(self):
        self.data['citizens'][2]['apartment'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_apartment_6(self):
        self.data['citizens'][2]['apartment'] = ""
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_1(self):
        self.data['citizens'][2]['name'] = ""
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_2(self):
        self.data['citizens'][2]['name'] = "!."
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_3(self):
        self.data['citizens'][2]['name'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_4(self):
        self.data['citizens'][2]['name'] = ['Wrong']
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_name_5(self):
        self.data['citizens'][2]['name'] = "Великий Могучий Русский Язык"
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_1(self):
        self.data['citizens'][2]['birth_date'] = ""
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_2(self):
        self.data['citizens'][2]['birth_date'] = "!."
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_3(self):
        self.data['citizens'][2]['birth_date'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_4(self):
        self.data['citizens'][2]['birth_date'] = ['Wrong']
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_5(self):
        self.data['citizens'][2]['name'] = "Великий Могучий Русский Язык"
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_6(self):
        self.data['citizens'][2]['name'] = 15
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_birth_date_7(self):
        self.data['citizens'][2]['name'] = '32.02.1999'
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_1(self):
        self.data['citizens'][2]['gender'] = ""
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_2(self):
        self.data['citizens'][2]['gender'] = "!."
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_3(self):
        self.data['citizens'][2]['gender'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_4(self):
        self.data['citizens'][2]['gender'] = ['Wrong']
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_gender_5(self):
        self.data['citizens'][2]['gender'] = ['male']
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_1(self):
        self.data['citizens'][2]['relatives'] = None
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_2(self):
        self.data['citizens'][2]['relatives'] = [None, None]
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_3(self):
        self.data['citizens'][2]['relatives'] = 1
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_4(self):
        self.data['citizens'][2]['relatives'] = ['a', 'b']
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_5(self):
        self.data['citizens'][2]['relatives'] = [4]
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_6(self):
        self.data['citizens'][2]['relatives'] = [3]
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

    def test_wrong_relatives_7(self):
        self.data['citizens'][2]['relatives'] = [2]
        a = self.client.post(path='/imports', data=json.dumps(self.data, ensure_ascii=False),
                             content_type='application/json')
        self.assertEqual(a.status_code, 400)

from random import choice
import sys
import json
import requests

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

for i in range(1, 10001):
    citizen = choice([a.copy(), b.copy(), c.copy()])
    citizen['citizen_id'] = i
    data['citizens'].append(citizen)
    print(citizen['citizen_id'])

print("СФОРМИРОВАЛОСЬ")
print("СФОРМИРОВАЛОСЬ")
print("СФОРМИРОВАЛОСЬ")


headers = {'Content-Type': 'application/json'}
a = requests.post('http://127.0.0.1:8000/imports/', data=json.dumps(data, indent=4).encode('utf-8'), headers=headers)

print(a.status_code)
print(a.text)


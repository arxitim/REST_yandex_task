import json
import requests

data = {
    "name": "Иванова Мария Леонидовна",
    "town": "Москва",
    "street": "Льва Толстого",
    "building": "16к7стр5",
    "apartment": 7,
    "relatives": []
}

headers = {'Content-Type': 'application/json'}
a = requests.patch('http://127.0.0.1:8000/imports/3/citizens/3', data=json.dumps(data, indent=4), headers=headers)

print(a.status_code)
print(a.text)
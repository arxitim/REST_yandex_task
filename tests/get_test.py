import requests


a = requests.get(f'http://127.0.0.1:8000/imports/{input()}/citizens')

print(a.status_code)
print(a.text)

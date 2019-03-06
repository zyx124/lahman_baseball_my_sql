import requests
import json

def test_api_1():

    r = requests.get('http://127.0.0.1:5000')
    result = r.text

    print("First REST APT returned", r.text)


def test_json():
    params = {'nameLast': 'Williams', 'fields': 'playerID, nameLast, nameFirst'}
    url = 'http://127.0.0.1:5000/api/lahman2017/people'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.get(url, headers = headers, params=params)
    print('result = ')
    print(json.dumps(r.json(), indent=2, default=str))

def test_json2():
    url = 'http://127.0.0.1:5000/explain/body'
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {'p': 'cool'}
    r = requests.post(url, headers=headers, json=data)
    print('result = ')
    print(json.dumps(r.json(),indent=2, default=str))

#test_api_1()
#test_json()
test_json2()
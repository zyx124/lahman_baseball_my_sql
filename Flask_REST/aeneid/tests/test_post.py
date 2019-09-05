import requests
import json

def display_response(rsp):

    try:
        print("Printing a response.")
        print("HTTP status code: ", rsp.status_code)
        h = dict(rsp.headers)
        print("Response headers: \n", json.dumps(h, indent=2, default=str))

        try:
            body = rsp.json()
            print("JSON body: \n", json.dumps(body, indent=2, default=str))
        except Exception as e:
            body = rsp.text
            print("Text body: \n", body)

    except Exception as e:
        print("display_response got exception e = ", e)


def test_create_player():


    try:
        body = {
            "playerID": "ok1",
            "nameLast": "Obiwan",
            "nameFirst": "Kenobi",

        }
        print("\ntest_create_manager: test 1, player = \,", json.dumps(body, indent=2, default=str))
        url = "http://127.0.0.1:5000/api/lahman2017/people"
        headers = {"content-type": "application/json"}
        result = requests.post(url, headers=headers, json=body)
        display_response(result)

        print("\ntest_create_manager: test 2 retrieving created player.")
        link = result.headers.get('Location', None)
        if link is None:
            print("No link header returned.")
        else:
            url = link
            headers = None
            result = requests.get(url)
            print("\ntest_create_player: Get returned: ")
            display_response(result)

        print("\ntest_create_manager: test 1, creating duplicate = \,", json.dumps(body, indent=2, default=str))
        url = "http://127.0.0.1:5000/api/lahman2017/people"
        headers = {"content-type": "application/json"}
        result = requests.post(url, headers=headers, json=body)
        display_response(result)

    except Exception as e:
        print("POST got exception = ", e)


test_create_player()
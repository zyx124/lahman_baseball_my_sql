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


def test_get_by_path():


    try:

        print("\ntest_get_manager: test 1, player = willite01,")
        url = "http://127.0.0.1:5000/api/lahman2017/people/willite01/batting?fields=playerID&order_by=G"
        result = requests.get(url)
        display_response(result)



    except Exception as e:
        print("POST got exception = ", e)


test_get_by_path()
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


def test_update_by_path():


    try:
        new = { "H":"100", "HR":"50", "yearID":"1963", "teamID":"BOS", "stint":"1" }
        print("\ntest_update_by_path:", new)
        url = "http://127.0.0.1:5000/api/lahman2017/people/willite01/batting"
        headers = {"content-type": "application/json"}
        result = requests.post(url, headers=headers, json=new)
        display_response(result)

        #test if new record has been added
        url2 = "http://127.0.0.1:5000/api/lahman2017/batting/willite01_BOS_1963_1"
        result2 = requests.get(url2)
        display_response(result2)


    except Exception as e:
        print("POST got exception = ", e)


test_update_by_path()
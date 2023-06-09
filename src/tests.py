import time
import httpx

# from fastapi.testclient import TestClient
# from .application import app
from pprint import pprint

client = httpx.Client()


def test_full():
    print("\n")
    base_url = "http://127.0.0.1:8000/"

    # get types
    response0 = client.get(base_url + "converter/conversion-types")
    res0_json = response0.json()
    assert response0.status_code == 200
    print("1 >>>", res0_json, "\n")

    # send convert
    files = [
        ("file", ("Keycode.pdf", open("/home/jahongir/Documents/Keycode.pdf", "rb"))),
    ]
    response1 = client.post(
        base_url + "converter/upload",
        params={"convert_to": "new.docx"},
        files=files,
    )
    assert response1.status_code == 201
    print("2 >>>", response1.json(), "\n")

    # get convertions
    message_id = response1.json().get("message_id")
    time.sleep(1)
    n = 0
    while n < 1:
        response2 = client.get(
            base_url + "converter/check", params={"message_id": message_id}
        )
        # if response2.json().get("status") != "result missing":
        #     break
        n += 1
        time.sleep(4)
    else:
        assert response2.status_code == 200
        print("3 >>>", response2.json(), "\n")

    # get file
    response3 = client.get(
        base_url + "converter/download", params={"message_id": message_id}
    )
    print("4 >>>", response3.headers)

import httpx
import time

client = httpx.Client()


def test_full():
    print("\n")
    base_url = "http://0.0.0.0:8000/"

    # get types
    response0 = client.get(base_url + "converter/conversion-types")
    res0_json = response0.json()
    assert response0.status_code == 200
    print("1 >>>", res0_json, "\n")

    # send convert
    files = [
        (
            "file",
            ("Keycode.pdf", open("/home/jahongir/Documents/Keycode.pdf", "rb")),
        ),
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
    success = ""
    while success != "success":
        response2 = client.get(
            base_url + "converter/check", params={"message_id": message_id}
        )
        time.sleep(2)
        print("3 >>>", response2.json(), "\n")
        success = response2.json().get("status")
        assert response2.status_code == 200

    # get file
    response3 = client.get(
        base_url + "converter/download", params={"message_id": message_id}
    )
    print("4 >>>", response3.headers)

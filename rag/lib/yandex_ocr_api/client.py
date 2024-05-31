import requests
import time

TIME_SLEEP = 60

class OCRClient:

    def __init__(self, TOKEN) -> None:
        self.post_api_handles = {"pdf_async": "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeTextAsync"}
        self.get_api_handles = {"get_pdf_async": "https://ocr.api.cloud.yandex.net/ocr/v1/getRecognition?operationId={id}"}
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {TOKEN}",
        }

    def post_process_request(self, json_body, handle):
        response = requests.post(self.post_api_handles[handle], headers=self.headers, json=json_body)

        if response.status_code != 200:
            raise Exception("Request has {0} code with {1} handle".format(response.status_code, handle))

        return response.json()
    
    def get_process_request(self, handle, id):
        response = requests.get(self.get_api_handles[handle].format(id=id), headers=self.headers)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            time.sleep(TIME_SLEEP)  
            return {}
        else:
            raise Exception("Request has {0} code with {1} handle where response conent: {2}".format(response.status_code, handle, response.content))

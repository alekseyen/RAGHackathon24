import requests

class YandexGPT:

    def __init__(self, CATALOG_ID, TOKEN):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {TOKEN}",
        }
        self.post_api_handles = {"sync_text_generation": "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"}
        self.models = {"yandex_2": f"gpt://{CATALOG_ID}/yandexgpt-lite/latest"}
        self.user_requests = []

    def process_request(self, user_prompt, system_prompt, handle_api, model, save_user_request=False, **kwargs):

        json = {
            "modelUri": self.models[model],
            "completionOptions": {
                "stream": kwargs.get("stream", False),
                "temperature": kwargs.get("temperature", 0),
                "maxTokens": kwargs.get("maxTokens", 1000),
            },
            "messages": []
        }

        system = {"role": "system",
                  "text": system_prompt
        }
        user = {"role": "user",
                "text": user_prompt
        }

        json["messages"].append(system)

        if save_user_request:
            json["messages"] += self.user_requests
            self.user_requests.append(user)
        else:
            self.user_requests = []

        json["messages"].append(user)

        url = self.post_api_handles[handle_api]

        response = requests.post(url, json=json, headers=self.headers)

        if response.status_code != 200:
            raise Exception("Request has {0} code with {1} handle".format(response.status_code, handle_api))

        return response.json()

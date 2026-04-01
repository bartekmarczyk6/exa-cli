import httpx
import time
from .errors import handle_api_error

BASE_URL = "https://api.exa.ai"

class ExaClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

    def _request(self, method, endpoint, **kwargs):
        url = f"{BASE_URL}{endpoint}"
        retries = 3
        backoff = 1

        with httpx.Client() as client:
            for attempt in range(retries):
                response = client.request(method, url, headers=self.headers, **kwargs)
                if response.status_code in (429, 500, 502, 503, 504):
                    if attempt < retries - 1:
                        time.sleep(backoff)
                        backoff *= 2
                        continue
                if response.status_code >= 400:
                    handle_api_error(response)
                if response.status_code == 204 or not response.content:
                    return {}
                return response.json()

    def post(self, endpoint, json=None):
        return self._request("POST", endpoint, json=json)

    def get(self, endpoint, params=None):
        return self._request("GET", endpoint, params=params)

    def stream_post(self, endpoint, json=None):
        import httpx_sse
        url = f"{BASE_URL}{endpoint}"
        with httpx.Client() as client:
            with httpx_sse.connect_sse(client, "POST", url, headers=self.headers, json=json) as event_source:
                for event in event_source.iter_sse():
                    yield event.data

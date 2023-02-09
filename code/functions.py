import requests
from requests.adapters import HTTPAdapter, Retry


class Request:
    def __init__(self, n_retry: int = 10, timeout: int = 5):
        self.retries = Retry(total=n_retry, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.adapter = HTTPAdapter(max_retries=self.retries)
        self.http = requests.Session()
        self.http.mount("https://", self.adapter)

        self.timeout = timeout

    def get(self, url: str, params: dict = None) -> str:
        if params is None:
            params = {}

        resp = self.http.get(url, params=params, timeout=self.timeout, headers={'accept-language':'pt-BR,pt;q=0.5'})
        resp.raise_for_status()

        return resp
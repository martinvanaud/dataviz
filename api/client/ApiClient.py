import requests


class APIClient:
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def request(self, method: str, endpoint: str, params: dict = None, headers: dict = None, json: dict = None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)

        response = self.session.request(method, url, params=params, headers=request_headers, json=json)
        return self._handle_response(response)

    def get(self, endpoint: str, params: dict = None, headers: dict = None, path_params: dict = None):
        if path_params:
            endpoint = endpoint.format(**path_params)
        return self.request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint: str, json: dict = None, headers: dict = None):
        return self.request("POST", endpoint, json=json, headers=headers)

    def _handle_response(self, response):
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": str(e), "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

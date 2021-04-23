import requests


class TAAPI:
    def __init__(self, config):
        self.config = config
        self.headers = {
            "Accept": "application/json",
        }

    def get_indicator_data(self):
        response = requests.get(
            url=self._get_url_from_config(),
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()

    def _get_url_from_config(self):
        taapi = self.config.get("taapi.io")
        return f'{taapi.get("base_url")}' \
               f'{taapi.get("indicator")}' \
               f'?secret={taapi.get("api_key")}' \
               f'&symbol={taapi.get("symbol")}' \
               f'&exchange={taapi.get("exchange")}' \
               f'&interval={taapi.get("interval")}'

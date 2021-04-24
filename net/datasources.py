import requests


class TAAPI:
    TAAPI = 'TAAPI'
    BASE_URL = 'base_url'
    INDICATOR = 'indicator'
    API_KEY = 'api_key'
    SYMBOL = 'symbol'
    EXCHANGE = 'exchange'
    INTERVAL = 'interval'

    def __init__(self, config):
        self.config = config
        self.headers = {
            "Accept": "application/json",
        }

    def get_indicator_data(self):
        response = requests.get(
            url=self._get_url_from_config(),
            headers=self.headers,
            timeout=3,
        )
        response.raise_for_status()
        return response.json()

    def _get_url_from_config(self):
        taapi = self.config.get(self.TAAPI)
        return f'{taapi.get(self.BASE_URL)}' \
               f'{taapi.get(self.INDICATOR)}' \
               f'?secret={taapi.get(self.API_KEY)}' \
               f'&symbol={taapi.get(self.SYMBOL)}' \
               f'&exchange={taapi.get(self.EXCHANGE)}' \
               f'&interval={taapi.get(self.INTERVAL)}'


class CMC:
    CMC = 'CMC'
    BASE_URL = 'base_url'
    ENDPOINT = 'endpoint'
    X_CMC_PRO_API_KEY = 'x-cmc-pro-api-key'
    SYMBOL = 'symbol'

    def __init__(self, config):
        self.config = config.get(self.CMC)
        self.headers = {
            "Accept": "application/json",
            "X-CMC_PRO_API_KEY": self.config.get(self.X_CMC_PRO_API_KEY)
        }

    def get_price_and_volume(self):
        response = requests.get(
            url=f'{self.config.get(self.BASE_URL)}{self.config.get(self.ENDPOINT)}',
            params={'symbol': self.config.get(self.SYMBOL)},
            headers=self.headers,
            timeout=3,
        )
        response.raise_for_status()
        data = response.json()
        return {
            'price': data['data']['BTC']['quote']['USD']['price'],
            'volume': data['data']['BTC']['quote']['USD']['volume_24h'],
        }

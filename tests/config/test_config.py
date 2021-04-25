from unittest import TestCase, mock

from config.config import ConfigParser, ValidationError


class ConfigTest(TestCase):

    config_file = {
        'BTC': {
            'TAAPI': {
                'base_url': 'https://api.taapi.io/',
                'exchange': 'binance',
                'indicator': 'macd',
                'symbol': 'BTC/USDT',
                'interval': '1h',
            },
            'CMC': {
                'base_url': 'https://pro-api.coinmarketcap.com',
                'endpoint': '/v1/cryptocurrency/quotes/latest',
                'symbol': 'BTC',
            }
        }
    }

    secrets_file = {
        'BTC': {
            'TAAPI': {
                'api_key': 'taapi-secret',
            },
            'CMC': {
                'x-cmc-pro-api-key': 'cmc-secret',
            }
        }
    }

    merged_config = {
        'BTC': {
            'TAAPI': {
                'base_url': 'https://api.taapi.io/',
                'exchange': 'binance',
                'indicator': 'macd',
                'symbol': 'BTC/USDT',
                'interval': '1h',
                'api_key': 'taapi-secret',
            },
            'CMC': {
                'base_url': 'https://pro-api.coinmarketcap.com',
                'endpoint': '/v1/cryptocurrency/quotes/latest',
                'symbol': 'BTC',
                'x-cmc-pro-api-key': 'cmc-secret',
            }
        }
    }

    @mock.patch('config.config.ConfigParser.read_config')
    def test_read_config_not_called_when_empty_list_passed_to_constructor(self, read_config):
        # given
        cp = ConfigParser([])

        # when
        cp.read_configs()

        # then
        read_config.assert_not_called()

    @mock.patch('config.config.ConfigParser.read_config')
    def test_read_configs_return_combined_values_from_yaml_files(self, read_config):
        # given
        read_config.side_effect = [self.config_file, self.secrets_file]
        expected = self.merged_config
        cp = ConfigParser(['config.yaml', 'secret.yaml'])

        # when
        configs = cp.read_configs()

        # then
        self.assertEqual(expected, configs)

    @mock.patch('config.config.ConfigParser.read_config')
    def test_read_configs_override_values_from_first_file_with_keys_from_second_file(self, read_config):
        # given
        read_config.side_effect = [self.config_file, self.secrets_file]
        expected = self.merged_config
        cp = ConfigParser(['config.yaml', 'secret.yaml'])

        # when
        configs = cp.read_configs()

        # then
        self.assertEqual(expected, configs)

    @mock.patch('config.config.ConfigParser.read_config')
    def test_read_configs_add_nested_values_instead_of_override_it(self, read_config):
        # given
        read_config.side_effect = [self.config_file, self.secrets_file]
        expected = self.merged_config
        cp = ConfigParser(['config.yaml', 'secret.yaml'])

        # when
        configs = cp.read_configs()

        # then
        self.assertEqual(expected, configs)

    @mock.patch('config.config.ConfigParser.read_config')
    def test_read_configs_raise_validation_error_if_lack_of_mandatory_keys(self, read_config):
        # given
        read_config.return_value = self.config_file
        cp = ConfigParser(['fake.yaml'])

        # then
        with self.assertRaises(ValidationError):
            # when
            cp.read_configs()

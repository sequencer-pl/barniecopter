from unittest import TestCase, mock

from config.config import ConfigParser


class ConfigTest(TestCase):

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
        config_content = {'public': 'value'}
        secret_content = {'secret': 'password'}
        read_config.side_effect = [config_content, secret_content]
        expected = {**config_content, **secret_content}
        cp = ConfigParser(['config.yaml', 'secret.yaml'])

        # when
        configs = cp.read_configs()

        # then
        self.assertEqual(expected, configs)

    @mock.patch('config.config.ConfigParser.read_config')
    def test_read_configs_override_values_from_first_file_with_keys_from_second_file(self, read_config):
        # given
        config_content = {'public': 'value', 'secret': ''}
        secret_content = {'secret': 'password'}
        read_config.side_effect = [config_content, secret_content]
        expected = {**config_content, **secret_content}
        cp = ConfigParser(['config.yaml', 'secret.yaml'])

        # when
        configs = cp.read_configs()

        # then
        self.assertEqual(expected, configs)

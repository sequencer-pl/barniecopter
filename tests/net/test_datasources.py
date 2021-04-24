from unittest import TestCase, mock

import responses
from requests import HTTPError

from net.datasources import TAAPI, CMC


class TAAPITest(TestCase):

    @responses.activate
    def test_get_indicator_data_raise_exception_when_requests_return_bad_status_code(self):
        # given
        config = {
            'TAAPI': {
                'base_url': 'http://nonexisting.datasource/',
                'indicator': 'fake-indicator'
            }
        }
        responses.add(responses.GET, 'http://nonexisting.datasource/fake-indicator',
                      status=404)

        # then
        with self.assertRaises(HTTPError):
            # when
            TAAPI(config).get_indicator_data()

    @responses.activate
    def test_get_indicator_data_return_dict(self):
        # given
        config = {
            'TAAPI': {
                'base_url': 'http://proper.datasource/',
                'indicator': 'indicator'
            }
        }
        expected = {
            'indicator': 'value'
        }
        responses.add(responses.GET, 'http://proper.datasource/indicator',
                      status=200, json=expected)

        # when
        data = TAAPI(config).get_indicator_data()

        # then
        self.assertEqual(data, expected)


class CMCTest(TestCase):

    config = {
        'CMC': {
            'base_url': 'http://sample.datasource',
            'endpoint': '/test_endpoint',
            'symbol': 'BTC',
            'x-cmc-pro-api-key': 'cmc-secret',
        }
    }

    @responses.activate
    def test_get_price_and_volume_raise_excpetion_when_request_ends_with_bad_status_code(self):
        # given
        responses.add(responses.GET, 'http://sample.datasource/test_endpoint?symbol=BTC',
                      status=404)

        # then
        with self.assertRaises(HTTPError):
            # when
            CMC(self.config).get_price_and_volume()

    @responses.activate
    def test_get_price_and_volume_call_request_with_x_cmc_pro_api_key_in_header(self):
        # given
        responses.add(responses.GET, 'http://sample.datasource/test_endpoint?symbol=BTC',
                      status=200,
                      json={
                          'data': {
                              'BTC': {
                                  'quote': {
                                      'USD': {
                                          'price': 10,
                                          'volume_24h': 24,
                                      }
                                  }
                              }
                          }
                      })

        # when
        CMC(self.config).get_price_and_volume()

        # then
        self.assertEqual(responses.calls[0].request.headers['X-CMC_PRO_API_KEY'], 'cmc-secret')

    @responses.activate
    def test_get_price_and_volume_return_dict_with_price_and_volume(self):
        # given
        responses.add(responses.GET, 'http://sample.datasource/test_endpoint?symbol=BTC',
                      status=200,
                      json={
                          'data': {
                              'BTC': {
                                  'quote': {
                                      'USD': {
                                          'price': 10,
                                          'volume_24h': 24,
                                      }
                                  }
                              }
                          }
                      })
        expected = {
            'price': 10, 'volume': 24
        }

        # when
        response = CMC(self.config).get_price_and_volume()

        # then
        self.assertEqual(response, expected)

    @responses.activate
    def test_get_price_and_volume_do_request_on_correct_endpoint_with_params(self):
        # given
        responses.add(responses.GET, 'http://sample.datasource/test_endpoint?symbol=BTC',
                      status=200,
                      json={
                          'data': {
                              'BTC': {
                                  'quote': {
                                      'USD': {
                                          'price': 10,
                                          'volume_24h': 24,
                                      }
                                  }
                              }
                          }
                      })
        expected_url = f"{self.config['CMC']['base_url']}{self.config['CMC']['endpoint']}"
        expected_params = {'symbol': self.config['CMC']['base_url']}

        # when
        CMC(self.config).get_price_and_volume()

        # then
        responses.calls[0].request.url = expected_url
        responses.calls[0].request.params = expected_params

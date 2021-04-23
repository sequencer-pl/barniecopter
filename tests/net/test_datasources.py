from unittest import TestCase

import responses
from requests import HTTPError

from net.datasources import TAAPI


class TAAPITest(TestCase):

    @responses.activate
    def test_get_indicator_data_raise_exception_when_requests_return_bad_status_code(self):
        # given
        config = {
            'base_url': 'http://nonexisting.datasource/',
            'indicator': 'fake-indicator'
        }
        responses.add(
            responses.GET,
            'http://nonexisting.datasource/fake-indicator',
            status=404
        )

        # then
        with self.assertRaises(HTTPError):
            # when
            TAAPI(config).get_indicator_data()

    @responses.activate
    def test_get_indicator_data_return_dict(self):
        # given
        config = {
            'base_url': 'http://proper.datasource/',
            'indicator': 'indicator'
        }
        responses.add(responses.GET, 'http://proper.datasource/indicator',
                      status=200,
                      json={
                          'indicator': 'value'
                      })

        # when
        data = TAAPI(config).get_indicator_data()

        # then
        self.assertIsInstance(data, dict)

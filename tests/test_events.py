# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"


class TestEventEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_event(self):
        with open('./tests/test_files/get_event.json', 'r') as event_file:
            event_json = json.load(event_file)
        responses.add(responses.GET, '{}/sample/v1/events/1337'.format(BASE_HOST), json=event_json, status=200)
        self.api.get_event(1337)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), event_json)

    @responses.activate
    def test_get_events(self):
        with open('./tests/test_files/get_events.json', 'r') as event_file:
            event_json = json.load(event_file)
        responses.add(responses.GET, '{}/sample/v1/events'.format(BASE_HOST), json=event_json, status=200)
        self.api.get_events()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), event_json)

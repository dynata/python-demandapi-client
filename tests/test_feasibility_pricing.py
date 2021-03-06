# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"


class TestFeasibilityEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_feasibility(self):
        with open('./tests/test_files/get_feasibility.json', 'r') as project_file:
            project_json = json.load(project_file)
        responses.add(responses.GET, '{}/sample/v1/projects/1/feasibility'.format(BASE_HOST), json=project_json, status=200)
        self.api.get_feasibility(1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), project_json)

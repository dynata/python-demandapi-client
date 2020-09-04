# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"


class TestUsersEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_teams(self):
        # Tests getting all teams.
        with open('./tests/test_files/get_teams.json', 'r') as teams:
            teams_json = json.load(teams)
        # Success response
        responses.add(responses.GET,'{}/sample/v1/teams'.format(BASE_HOST), json=teams_json, status=200)
        self.api.get_company_teams()
        self.assertEqual(len(responses.calls), 1)
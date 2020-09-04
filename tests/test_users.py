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
    def test_get_user_info(self):
        # Tests getting currently logged in user info.
        with open('./tests/test_files/get_user_info.json', 'r') as user_info:
            user_info_json = json.load(user_info)
        # Success response
        responses.add(responses.GET,'{}/sample/v1/users/info'.format(BASE_HOST), json=user_info_json, status=200)
        self.api.get_user_info()
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_company_users(self):
        # Tests getting all company users.
        with open('./tests/test_files/get_company_users.json', 'r') as company_users:
            company_users_json = json.load(company_users)
        # Success response
        responses.add(responses.GET,'{}/sample/v1/users'.format(BASE_HOST), json=company_users_json, status=200)
        self.api.get_company_users()
        self.assertEqual(len(responses.calls), 1)
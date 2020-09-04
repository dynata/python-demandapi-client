# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

from dynatademand.api import DemandAPIClient
from dynatademand.errors import DemandAPIError

BASE_HOST = "http://test-url.example"


class TestUsersEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_project_permissions(self):
        with open('./tests/test_files/get_project_permissions.json', 'r') as get_permissions_file:
            permissions_json = json.load(get_permissions_file)
        responses.add(responses.GET, '{}/sample/v1/projects/1/permissions'.format(BASE_HOST), json=permissions_json, status=200)
        self.api.get_project_permissions(1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), permissions_json)

    @responses.activate
    def test_upsert_project_permissions(self):
        # Tests updating a project.
        with open('./tests/test_files/upsert_project_permissions.json', 'r') as upsert_project_file:
            upsert_project_data = json.load(upsert_project_file)

        # Success response
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/1/permissions'.format(BASE_HOST),
            json={'status': {'message': 'success'}},
            status=200)
        # Error message included
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/1/permissions'.format(BASE_HOST),
            json={'status': {'message': 'error'}},
            status=200)

        # Test successful response.
        self.api.upsert_project_permissions(1, upsert_project_data)
        self.assertEqual(len(responses.calls), 1)

        # Test response with error included.
        with self.assertRaises(DemandAPIError):
            self.api.upsert_project_permissions(1, upsert_project_data)
        self.assertEqual(len(responses.calls), 2)
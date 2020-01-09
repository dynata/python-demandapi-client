# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import responses
import unittest
from jsonschema.exceptions import ValidationError

from dynatademand.api import DemandAPIClient
from dynatademand.validator import DemandAPIValidator

BASE_HOST = "http://test-url.example"


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = DemandAPIValidator()
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    def test_query_params(self):
        self.validator.validate_request(
            'get_projects',
            query_params={'limit': 100}
        )

        with self.assertRaises(ValidationError):
            self.validator.validate_request(
                'get_projects',
                query_params={'limit': 'five hundred'}
            )

    @responses.activate
    def test_query_params_with_api_client(self):
        responses.add(responses.GET, '{}/sample/v1/projects'.format(BASE_HOST), json={}, status=200)

        # Valid keyword arguments
        self.api.get_projects(
            limit=100,
            offset=0,
            created_at="today",
            sort=["ordering"]
        )

        with self.assertRaises(ValidationError):
            # Limit greater than allowed
            self.api.get_projects(limit=500)

        with self.assertRaises(ValidationError):
            # Limit not a number
            self.api.get_projects(limit="five")

    @responses.activate
    def test_path_validation(self):
        responses.add(
            responses.GET,
            '{}/sample/v1/projects/my%20project/lineItems/my%20line%20item'.format(BASE_HOST),
            json={},
            status=200
        )

        # All path components are strings and don't have any validation besides that.
        # This is technically valid even if it looks weird.
        self.api.get_line_item("my project", "my line item")

    @responses.activate
    def test_body_validation(self):
        # Tests implementation of validation through the API.
        with open('./tests/test_files/update_project.json', 'r') as update_project_file:
            update_project_data = json.load(update_project_file)
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/1'.format(BASE_HOST),
            json={'status': {'message': 'success'}},
            status=200
        )

        self.api.update_project(1, update_project_data)

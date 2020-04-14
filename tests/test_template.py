# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"


class TestTemplateEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_templates(self):
        # Tests getting all templates.
        with open('./tests/test_files/get_templates.json', 'r') as options:
            options_json = json.load(options)
        # Success response
        responses.add(
            responses.GET,
            '{}/sample/v1/templates/quotaplan/{}/{}'.format(BASE_HOST,'US','en'),
            json=options_json,
            status=200)
        self.api.get_templates('US', 'en')
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_create_template(self):
        # Tests creating a template.
        with open('./tests/test_files/create_template.json', 'r') as new_template_file:
            new_template_data = json.load(new_template_file)
        # Success response
        responses.add(
            responses.POST,
            '{}/sample/v1/templates/quotaplan'.format(BASE_HOST),
            json={'status': {'message': 'success'}},
            status=200)
        # Response with error status
        responses.add(
            responses.POST,
            '{}/sample/v1/templates/quotaplan'.format(BASE_HOST),
            json={'status': {'message': 'error'}},
            status=200)
        # Test success response
        self.api.create_template(new_template_data)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update_template(self):
        # Tests creating a template.
        with open('./tests/test_files/update_template.json', 'r') as new_template_file:
            new_template_data = json.load(new_template_file)
        # Success response
        responses.add(
            responses.POST,
            '{}/sample/v1/templates/quotaplan/{}'.format(BASE_HOST, 1),
            json={'status': {'message': 'success'}},
            status=200)
        # Response with error status
        responses.add(
            responses.POST,
            '{}/sample/v1/templates/quotaplan/{}'.format(BASE_HOST, 1),
            json={'status': {'message': 'error'}},
            status=200)
        # Test success response
        self.api.update_template(1, new_template_data)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete_template(self):
        # Tests deleteing templates
        responses.add(
            responses.DELETE,
            '{}/sample/v1/templates/quotaplan/1'.format(BASE_HOST),
            json={'status': {'message': 'success'}},
            status=200)
        # Response with error status
        responses.add(
            responses.DELETE,
            '{}/sample/v1/templates/quotaplan/1'.format(BASE_HOST),
            json={'status': {'message': 'error'}},
            status=200)
        # Test successful response
        self.api.delete_template(1)
        self.assertEqual(len(responses.calls), 1)

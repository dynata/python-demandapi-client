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


class TestProjectEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_project(self):
        with open('./tests/test_files/get_project.json', 'r') as project_file:
            project_json = json.load(project_file)
        responses.add(responses.GET, '{}/sample/v1/projects/1'.format(BASE_HOST), json=project_json, status=200)
        self.api.get_project(1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), project_json)

    @responses.activate
    def test_get_projects(self):
        with open('./tests/test_files/get_projects.json', 'r') as project_file:
            project_json = json.load(project_file)
        responses.add(responses.GET, '{}/sample/v1/projects'.format(BASE_HOST), json=project_json, status=200)
        self.api.get_projects()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), project_json)

    @responses.activate
    def test_get_project_detailed_report(self):
        with open('./tests/test_files/get_project_detailed_report.json', 'r') as project_detailed_report_file:
            project_detailed_report_json = json.load(project_detailed_report_file)
        responses.add(responses.GET, '{}/sample/v1/projects/1/detailedReport'.format(BASE_HOST), json=project_detailed_report_json, status=200)
        self.api.get_project_detailed_report(1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), project_detailed_report_json)

    @responses.activate
    def test_create_project(self):
        # Tests creating a project. This also tests validating the project data as part of `api.create_project`.
        with open('./tests/test_files/create_project.json', 'r') as new_project_file:
            new_project_data = json.load(new_project_file)
        responses.add(responses.POST, '{}/sample/v1/projects'.format(BASE_HOST), json={'status': {'message': 'success'}}, status=200)
        self.api.create_project(new_project_data)
        self.assertEqual(len(responses.calls), 1)

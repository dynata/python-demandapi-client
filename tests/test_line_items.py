# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

from dynatademand.api import DemandAPIClient
from dynatademand.errors import DemandAPIError

BASE_HOST = "http://test-url.example"


class TestLineItemEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_line_item(self):
        with open('./tests/test_files/get_line_item.json', 'r') as line_item_file:
            line_item_json = json.load(line_item_file)
        responses.add(
            responses.GET,
            '{}/sample/v1/projects/1/lineItems/100'.format(BASE_HOST),
            json=line_item_json,
            status=200)
        self.api.get_line_item(1, 100)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), line_item_json)

    @responses.activate
    def test_get_line_items(self):
        with open('./tests/test_files/get_line_items.json', 'r') as line_item_file:
            line_item_json = json.load(line_item_file)
        responses.add(responses.GET, '{}/sample/v1/projects/1/lineItems'.format(BASE_HOST), json=line_item_json, status=200)
        self.api.get_line_items(1)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), line_item_json)

    @responses.activate
    def test_get_line_item_detailed_report(self):
        with open('./tests/test_files/get_line_item_detailed_report.json', 'r') as line_item_detailed_report_file:
            line_item_detailed_report_json = json.load(line_item_detailed_report_file)
        responses.add(
            responses.GET,
            '{}/sample/v1/projects/1/lineItems/100/detailedReport'.format(BASE_HOST),
            json=line_item_detailed_report_json,
            status=200)
        self.api.get_line_item_detailed_report(1, 100)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), line_item_detailed_report_json)

    @responses.activate
    def test_launch_line_item(self):
        # Tests closing a project.
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/24/lineItems/180/launch'.format(BASE_HOST),
            json={'status': {'message': 'success'}},
            status=200
        )

        # Response with error status
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/24/lineItems/180/launch'.format(BASE_HOST),
            json={'status': {'message': 'error'}},
            status=200
        )

        # Test successful response
        self.api.launch_line_item(24, 180)
        self.assertEqual(len(responses.calls), 1)

        # Test error response
        with self.assertRaises(DemandAPIError):
            self.api.launch_line_item(24, 180)
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_pause_line_item(self):
        # Tests pausing a line item.
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/24/lineItems/180/pause'.format(BASE_HOST),
            json={'status': {'message': 'success'}},
            status=200
        )
        # Response with error
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/24/lineItems/180/pause'.format(BASE_HOST),
            json={'status': {'message': 'error'}},
            status=200
        )

        # Test successful response
        self.api.pause_line_item(24, 180)
        self.assertEqual(len(responses.calls), 1)

        # Test error response
        with self.assertRaises(DemandAPIError):
            self.api.pause_line_item(24, 180)
        self.assertEqual(len(responses.calls), 2)

    @responses.activate
    def test_update_line_item(self):
        with open('./tests/test_files/update_line_item.json', 'r') as new_lineitem_file:
            update_lineitem_data = json.load(new_lineitem_file)

        # Success response
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/1/lineItems/1'.format(BASE_HOST),
            json={'status': {'message': 'success'}},
            status=200
        )
        # Response with error status
        responses.add(
            responses.POST,
            '{}/sample/v1/projects/1/lineItems/1'.format(BASE_HOST),
            json={'status': {'message': 'error'}},
            status=200
        )

        # Test success response
        self.api.update_line_item(1, 1, update_lineitem_data)
        self.assertEqual(len(responses.calls), 1)

        # Test error response
        with self.assertRaises(DemandAPIError):
            self.api.update_line_item(1, 1, update_lineitem_data)
            self.assertEqual(len(responses.calls), 2)

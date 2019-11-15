# encoding: utf-8
from __future__ import unicode_literals, print_function

import unittest
import responses

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from dynatademand.api import DemandAPIClient
from dynatademand.errors import DemandAPIError

BASE_URL = "http://test-url.example"


class AuthenticationTestMissingCredentials(unittest.TestCase):
    @patch('os.getenv')
    def test_missing_client_id(self, mock_getenv):
        mock_getenv.side_effect = [
            None,
            "test_username",
            "test_password",
            BASE_URL
        ]
        with self.assertRaises(DemandAPIError):
            DemandAPIClient()

    @patch('os.getenv')
    def test_missing_username(self, mock_getenv):
        mock_getenv.side_effect = [
            "test_client_id",
            None,
            "test_password",
            BASE_URL
        ]
        with self.assertRaises(DemandAPIError):
            DemandAPIClient()

    @patch('os.getenv')
    def test_missing_password(self, mock_getenv):
        mock_getenv.side_effect = [
            "test_client_id",
            "test_username",
            None,
            BASE_URL
        ]
        with self.assertRaises(DemandAPIError):
            DemandAPIClient()


def api_test_url(endpoint):
    return "{}{}".format(BASE_URL, endpoint)


class AuthenticationTests(unittest.TestCase):
    @patch('os.getenv')
    def setUp(self, mock_getenv):
        mock_getenv.side_effect = [
            "test_client_id",
            "test_username",
            "test_password",
            BASE_URL
        ]
        self.client = DemandAPIClient()
        self.assertEqual(self.client.client_id, "test_client_id")

    @responses.activate
    def test_authenticate(self):
        responses.add(
            responses.POST,
            "{}{}".format(self.client.auth_base_url, "/token/password"),
            json={
                "accessToken": "access_token",
                "refreshToken": "refresh_token"
            }
        )
        self.client.authenticate()
        self.assertEqual(self.client._access_token, "access_token")
        self.assertEqual(self.client._refresh_token, "refresh_token")
        self.assertIsNone(self.client._check_authentication())

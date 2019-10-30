import os
import requests
from .errors import DemandAPIError


class DemandAPIClient(object):
    def __init__(self):
        self.client_id = os.getenv('DYNATA_DEMAND_CLIENT_ID', None)
        self.username = os.getenv('DYNATA_DEMAND_USERNAME', None)
        self.password = os.getenv('DYNATA_DEMAND_PASSWORD', None)
        if None in [self.client_id, self.username, self.password]:
            raise DemandAPIError("All authentication data is required.")
        self._access_token = None
        self._refresh_token = None
        self.base_host = os.getenv('DYNATA_DEMAND_BASE_URL', 'https://api.researchnow.com')
        self.auth_base_url = '{}/auth/v1'.format(self.base_host)
        self.base_url = '{}/sample/v1'.format(self.base_host)

    def _check_authentication(self):
        if self._access_token is None:
            raise DemandAPIError('The API instance must be authenticated before calling this method.')

    def _api_post(self, uri, payload):
        # Send an authenticated POST request to an API endpoint.
        self._check_authentication()
        url = '{}{}'.format(self.base_url, uri)
        request_headers = {
            'oauth_access_token': self._access_token,
            'Content-Type': "application/json",
        }
        response = requests.post(url=url, json=payload, headers=request_headers)
        if response.status_code > 399:
            raise DemandAPIError('Demand API request to {} failed with status {}. Response: {}'.format(
                url, response.status_code, response.content
            ))
        return response.json()

    def authenticate(self):
        url = '{}/token/password'.format(self.auth_base_url)
        auth_response = requests.post(url, json={
            'clientId': self.client_id,
            'password': self.password,
            'username': self.username,
        })
        if auth_response.status_code > 399:
            raise DemandAPIError('Authentication failed with status {} and error: {}'.format(
                auth_response.status_code,
                auth_response.json())
            )
        response_data = auth_response.json()
        self._access_token = response_data.get('accessToken')
        self._refresh_token = response_data.get('refreshToken')
        return response_data

    def refresh_access_token(self):
        url = '{}/token/refresh'.format(self.auth_base_url)
        refresh_response = requests.post(url, json={
            'clientId': self.client_id,
            'refreshToken': self._refresh_token
        })
        if refresh_response.status_code != 200:
            raise DemandAPIError("Refreshing Access Token failed with status {} and error: {}".format(
                refresh_response.status_code, refresh_response.content
            ))
        response_data = refresh_response.json()
        self._access_token = response_data.get('accessToken')
        self._refresh_token = response_data.get('refreshToken')
        return response_data

    def logout(self):
        url = '{}/logout'.format(self.auth_base_url)
        logout_response = requests.post(url, json={
            'clientId': self.client_id,
            'refreshToken': self._refresh_token,
            'accessToken': self._access_token
        })
        if logout_response.status_code != 204:
            raise DemandAPIError("Log out failed with status {} and error: {}".format(
                logout_response.status_code, logout_response.content
            ))
        return logout_response.json()

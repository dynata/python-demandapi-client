import os
import requests

from .errors import DemandAPIError
from .validator import DemandAPIValidator


class DemandAPIClient(object):
    def __init__(self, client_id=None, username=None, password=None, base_host=None):
        if client_id is not None:
            self.client_id = client_id
        else:
            self.client_id = os.getenv('DYNATA_DEMAND_CLIENT_ID', None)
        if username is not None:
            self.username = username
        else:
            self.username = os.getenv('DYNATA_DEMAND_USERNAME', None)
        if password is not None:
            self.password = password
        else:
            self.password = os.getenv('DYNATA_DEMAND_PASSWORD', None)
        if base_host is not None:
            self.base_host = base_host
        else:
            self.base_host = os.getenv('DYNATA_DEMAND_BASE_URL', default='https://api.researchnow.com')

        if None in [self.client_id, self.username, self.password]:
            raise DemandAPIError('All authentication data is required.')

        self._access_token = None
        self._refresh_token = None
        self.auth_base_url = '{}/auth/v1'.format(self.base_host)
        self.base_url = '{}/sample/v1'.format(self.base_host)

        self.validator = DemandAPIValidator()

    def _check_authentication(self):
        # This doesn't check if the access token is valid, just that it exists.
        # The access_token is generated by calling the `authenticate` method.
        if self._access_token is None:
            raise DemandAPIError('The API instance must be authenticated before calling this method.')

    def _api_post(self, uri, payload):
        # Send an authenticated POST request to an API endpoint.
        self._check_authentication()
        url = '{}{}'.format(self.base_url, uri)
        request_headers = {
            'Authorization': 'Bearer {}'.format(self._access_token),
            'Content-Type': "application/json",
        }
        response = requests.post(url=url, json=payload, headers=request_headers)
        if response.status_code > 399:
            raise DemandAPIError('Demand API request to {} failed with status {}. Response: {}'.format(
                url, response.status_code, response.content
            ))
        return response.json()

    def _api_get(self, uri, query_params=None):
        # Send an authenticated POST request to an API endpoint.
        self._check_authentication()
        url = '{}{}'.format(self.base_url, uri)
        request_headers = {
            'Authorization': 'Bearer {}'.format(self._access_token),
            'Content-Type': "application/json",
        }
        response = requests.get(url=url, params=query_params, headers=request_headers)
        if response.status_code > 399:
            raise DemandAPIError('Demand API request to {} failed with status {}. Response: {}'.format(
                url, response.status_code, response.content
            ))
        if response.headers['content-type'] == 'application/pdf':
            return response.content
        return response.json()

    def _api_delete(self, uri):
        # Send an authenticated DELETE request to an API endpoint.
        self._check_authentication()
        url = '{}{}'.format(self.base_url, uri)
        request_headers = {
            'Authorization': 'Bearer {}'.format(self._access_token),
            'Content-Type': "application/json",
        }
        response = requests.delete(url=url, headers=request_headers)
        if response.status_code > 399:
            raise DemandAPIError('Demand API request to {} failed with status {}. Response: {}'.format(
                url, response.status_code, response.content
            ))
        if response.headers['content-type'] == 'application/pdf':
            return response.content
        return response.json()

    def authenticate(self):
        # Sends the authentication data to the access token endpoint.
        url = '{}/token/password'.format(self.auth_base_url)
        payload = {
            'clientId': self.client_id,
            'password': self.password,
            'username': self.username,
        }

        '''
            #TODO: Waiting for a valid schema.
            self.validator.validate_request(
                'obtain_access_token',
                request_body=payload
            )
        '''

        auth_response = requests.post(url, json=payload)
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
        payload = {
            'clientId': self.client_id,
            'refreshToken': self._refresh_token
        }
        # Validate the rqeuest before sending.
        self.validator.validate_request(
            'refresh_access_token',
            request_body=payload
        )
        refresh_response = requests.post(url, json=payload)
        if refresh_response.status_code != 200:
            raise DemandAPIError('Refreshing Access Token failed with status {} and error: {}'.format(
                refresh_response.status_code, refresh_response.content
            ))
        response_data = refresh_response.json()
        self._access_token = response_data.get('accessToken')
        self._refresh_token = response_data.get('refreshToken')
        return response_data

    def logout(self):
        url = '{}/logout'.format(self.auth_base_url)
        payload = {
            'clientId': self.client_id,
            'refreshToken': self._refresh_token,
            'accessToken': self._access_token
        }
        self.validator.validate_request(
            'logout',
            request_body=payload
        )

        logout_response = requests.post(url, json=payload)
        if logout_response.status_code != 204:
            raise DemandAPIError('Log out failed with status {} and error: {}'.format(
                logout_response.status_code, logout_response.content
            ))
        return logout_response.json()

    def get_attributes(self, country_code, language_code, **kwargs):
        self.validator.validate_request(
            'get_attributes',
            path_data={
                'countryCode': '{}'.format(country_code),
                'languageCode': '{}'.format(language_code)
            },
            query_params=kwargs,
        )
        return self._api_get('/attributes/{}/{}'.format(country_code, language_code), kwargs)

    def get_countries(self, **kwargs):
        self.validator.validate_request(
            'get_countries',
            query_params=kwargs,
        )
        return self._api_get('/countries', kwargs)

    def get_study_metadata(self):
        return self._api_get('/studyMetadata')

    def get_event(self, event_id):
        self.validator.validate_request(
            'get_event',
            path_data={'eventId': '{}'.format(event_id)},
        )
        return self._api_get('/events/{}'.format(event_id))

    def get_events(self, **kwargs):
        self.validator.validate_request(
            'get_events',
            query_params=kwargs,
        )
        return self._api_get('/events', kwargs)

    def create_project(self, project_data):
        '''
            #TODO: Waiting on a valid request body schema.
            self.validator.validate_request(
                'create_project',
                request_body=project_data,
            )
        '''
        response_data = self._api_post('/projects', project_data)
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                'Could not create project. Demand API responded with: {}'.format(
                    response_data
                )
            )
        return response_data

    def get_invoice(self, project_id):
        self.validator.validate_request(
            'get_event',
            path_data={'extProjectId': '{}'.format(project_id)},
        )
        return self._api_get('/projects/{}/invoices'.format(project_id))

    def buy_project(self, project_id, buy_data):
        '''
            Buy the line items for a project, agreeing to the price. A Line Item
            can only be bought if the feasibility for the line item is in status=READY
            and totalCount > 0.
        '''
        self.validator.validate_request(
            'buy_project',
            path_data={'extProjectId': '{}'.format(project_id)},
            request_body=buy_data,
        )
        response_data = self._api_post('/projects/{}/buy'.format(project_id), buy_data)
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not buy project. Demand API responded with: {}".format(
                    response_data
                )
            )
        return response_data

    def close_project(self, project_id):
        # Closes the requested project. Once a project is closed, all traffic
        # is stopped, and the project is automatically sent for invoicing.
        self.validator.validate_request(
            'close_project',
            path_data={'extProjectId': '{}'.format(project_id)},
        )
        response_data = self._api_post('/projects/{}/close'.format(project_id), {})
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not close project. Demand API responded with: {}".format(
                    response_data
                )
            )
        return response_data

    def get_project(self, project_id):
        self.validator.validate_request(
            'get_project',
            path_data={'extProjectId': '{}'.format(project_id)},
        )
        return self._api_get('/projects/{}'.format(project_id))

    def get_projects(self, **kwargs):
        self.validator.validate_request(
            'get_projects',
            query_params=kwargs,
        )
        return self._api_get('/projects', kwargs)

    def update_project(self, project_id, update_data):
        '''
            #TODO: Waiting on a valid request body schema and path schema.
            self.validator.validate_request(
                'update_project',
                path_data={'extProjectId': '{}'.format(project_id)},
                request_body=update_data,
            )
        '''
        response_data = self._api_post('/projects/{}'.format(project_id), update_data)
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not update project. Demand API responded with: {}".format(
                    response_data
                )
            )
        return response_data

    def get_project_detailed_report(self, project_id):
        self.validator.validate_request(
            'get_project_detailed_report',
            path_data={'extProjectId': '{}'.format(project_id)},
        )
        return self._api_get('/projects/{}/detailedReport'.format(project_id))

    def add_line_item(self, project_id, lineitem_data):
        '''
            A line item is a project entity that exist for a specific market and
            language that your survey is aimed at. It defines the target panelists
            for the market that the survey is looking for, and the number of
            completes required. A line item is our unit of work and is what
            gets billed to you.
        '''
        '''
            #TODO: Waiting on a valid request body and path schema.
            self.validator.validate_request(
                'create_line_item',
                path_data={
                    'extProjectId': '{}'.format(project_id)
                },
                request_body=lineitem_data
            )
        '''
        response_data = self._api_post('/projects/{}/lineItems'.format(project_id), lineitem_data)
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not add line item. Demand API responded with: {}".format(
                    response_data
                )
            )
        return response_data

    def close_line_item(self, project_id, line_item_id):
        # Starts traffic to a line item.
        self.validator.validate_request(
            'close_line_item',
            path_data={
                'extProjectId': '{}'.format(project_id),
                'extLineItemId': '{}'.format(line_item_id),
            },
        )
        response_data = self._api_post('/projects/{}/lineItems/{}/close'.format(project_id, line_item_id), {})
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not close line item. Demand API responded with: {}".format(
                    response_data
                )
            )
        return response_data

    def launch_line_item(self, project_id, line_item_id):
        # Starts traffic to a line item.
        self.validator.validate_request(
            'launch_line_item',
            path_data={
                'extProjectId': '{}'.format(project_id),
                'extLineItemId': '{}'.format(line_item_id),
            },
        )
        response_data = self._api_post('/projects/{}/lineItems/{}/launch'.format(project_id, line_item_id), {})
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not launch line item. Demand API responded with: {}".format(
                    response_data
                )
            )
        return response_data

    def pause_line_item(self, project_id, line_item_id):
        # Stops traffic to a line item.
        self.validator.validate_request(
            'pause_line_item',
            path_data={
                'extProjectId': '{}'.format(project_id),
                'extLineItemId': '{}'.format(line_item_id),
            },
        )
        response_data = self._api_post('/projects/{}/lineItems/{}/pause'.format(project_id, line_item_id), {})
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not pause line item. Demand API responded with: {}".format(
                    response_data
                )
            )
        return response_data

    def set_quotacell_status(self, project_id, line_item_id, quota_cell_id, action):
        # Stops traffic to a line item.
        self.validator.validate_request(
            'set_quotacell_status',
            path_data={
                'extProjectId': '{}'.format(project_id),
                'extLineItemId': '{}'.format(line_item_id),
                'quotaCellId': '{}'.format(quota_cell_id),
                'action': '{}'.format(action),
            },
        )
        response_data = self._api_post('/projects/{}/lineItems/{}/quotaCells/{}/{}'.format(
            project_id, line_item_id, quota_cell_id, action), {})
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not {} quotacell. Demand API responded with: {}".format(
                    action, response_data
                )
            )
        return response_data

    def get_line_item(self, project_id, line_item_id):
        self.validator.validate_request(
            'get_line_item',
            path_data={
                'extProjectId': '{}'.format(project_id),
                'extLineItemId': '{}'.format(line_item_id)
            },
        )
        return self._api_get('/projects/{}/lineItems/{}'.format(project_id, line_item_id))

    def update_line_item(self, project_id, line_item_id, line_item_data):
        '''
            Updates the specified line item by setting the values of the parameters passed.
            Any parameters not provided will be left unchanged.
        '''
        '''
            #TODO: Waiting on a valid path and request body schema.
            self.validator.validate_request(
                'update_line_item',
                path_data={
                    'extProjectId': '{}'.format(project_id),
                    'extLineItemId': '{}'.format(line_item_id),
                },
                request_body=line_item_data,
            )
        '''
        response_data = self._api_post('/projects/{}/lineItems/{}'.format(project_id, line_item_id), line_item_data)
        if response_data.get('status').get('message') != 'success':
            raise DemandAPIError(
                "Could not update line item. Demand API responded with: {}".format(
                    response_data
                )
            )
        return response_data

    def get_line_items(self, project_id, **kwargs):
        self.validator.validate_request(
            'get_line_items',
            path_data={'extProjectId': '{}'.format(project_id)},
            query_params=kwargs,
        )
        return self._api_get('/projects/{}/lineItems'.format(project_id), kwargs)

    def get_line_item_detailed_report(self, project_id, line_item_id):
        self.validator.validate_request(
            'get_line_item_detailed_report',
            path_data={
                'extProjectId': '{}'.format(project_id),
                'extLineItemId': '{}'.format(line_item_id),
            },
        )
        return self._api_get('/projects/{}/lineItems/{}/detailedReport'.format(project_id, line_item_id))

    def get_feasibility(self, project_id):
        self.validator.validate_request(
            'get_feasibility',
            path_data={'extProjectId': '{}'.format(project_id)},
        )
        return self._api_get('/projects/{}/feasibility'.format(project_id))

    def get_survey_topics(self, **kwargs):
        self.validator.validate_request(
            'get_survey_topics',
            query_params=kwargs,
        )
        return self._api_get('/categories/surveyTopics', kwargs)

    def get_sources(self):
        self.validator.validate_request(
            'get_sources',
        )
        return self._api_get('/sources')

    def get_invoices_summary(self, **kwargs):
        self.validator.validate_request(
            'get_invoices_summary',
            query_params=kwargs
        )
        return self._api_get('/projects/invoices/summary', kwargs)

    def reconcile_project(self, project_id, file, message):
        '''
            Sends a reconciliation request
        '''
        """
            # Awaiting valid body & path schemas
            self.validator.validate_request(
                'update_line_item',
                path_data={
                    'extProjectId': '{}'.format(project_id),
                },
                request_body={
                    'file': file,
                    'message': message,
                },
            )
        """
        self._check_authentication()
        url = '{}{}'.format(self.base_url, '/projects/{}/reconcile'.format(project_id))
        request_headers = {
            'Authorization': 'Bearer {}'.format(self._access_token),
            'Content-Type': "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
        response = requests.post(url=url, data=file, headers=request_headers)
        if response.status_code > 399:
            raise DemandAPIError('Demand API request to {} failed with status {}. Response: {}'.format(
                url, response.status_code, response.content
            ))
        return response.json()

    def create_template(self, template):
        # TODO: Waiting on a valid path and request body schema.
        # self.validator.validate_request(
        #     'create_template',
        #     request_body=template,
        # )
        return self._api_post('/templates/quotaplan', template)

    def update_template(self, id, template):
        # TODO: Waiting on a valid path and request body schema.
        # self.validator.validate_request(
        #     'update_template',
        #     path_data={'id': '{}'.format(id)},
        #     request_body=template,
        # )
        return self._api_post('/templates/quotaplan/{}'.format(id), template)

    def delete_template(self, id):
        self.validator.validate_request(
            'delete_template',
            path_data={'id': '{}'.format(id)},
         )
        return self._api_delete('/templates/quotaplan/{}'.format(id))

    def get_templates(self, country, lang, **kwargs):
        self.validator.validate_request(
            'get_templates',
            path_data={
                'countryCode': '{}'.format(country),
                'languageCode': '{}'.format(lang)
            },
            query_params=kwargs,
        )
        return self._api_get('/templates/quotaplan/{}/{}'.format(country, lang), kwargs)

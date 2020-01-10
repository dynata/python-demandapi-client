import json
import jsonschema

ENDPOINTS = {
    # Authorization
    'obtain_access_token': ['body', ],
    'refresh_access_token': ['body', ],
    'logout': ['body', ],

    # Projects
    'create_project': ['body', ],
    'get_projects': ['query', ],
    'get_project': ['path', ],
    'close_project': ['path', ],
    'update_project': ['path', 'body', ],
    'get_project_detailed_report': ['path', ],

    # Line items
    'get_line_item': ['path', ],
    'get_line_items': ['path', 'query'],
    'get_line_item_detailed_report': ['path', ],
    'update_line_item': ['path', 'body'],

    # Events
    'get_events': ['query', ],
    'get_event': ['path', ],

    # Attributes
    'get_attributes': ['path', 'query', ],

    # Categories
    'get_survey_topics': ['query', ],

    # Countries & Languages
    'get_countries': ['query', ],

    # Pricing & Feasibility
    'get_feasibility': ['path', ],

    # Supplier Sources
    'get_sources': [],
}


class DemandAPIValidator(object):
    def __init__(self, ):
        self.schemas = {
            'path': {},
            'query': {},
            'body': {},
        }
        for endpoint_name, schemas in ENDPOINTS.items():
            for schema in schemas:
                with open('dynatademand/schemas/request/{}/{}.json'.format(schema, endpoint_name), 'r') as schema_file:
                    self.schemas[schema][endpoint_name] = json.load(schema_file)

    def _validate_object(self, schema_type, endpoint_name, data):
        jsonschema.validate(schema=self.schemas[schema_type][endpoint_name], instance=data)

    def validate_request(self, endpoint_name, path_data={}, query_params={}, request_body={}):
        '''
            # TODO: None of the path schemas from the documentation are currently valid.
            if 'path' in ENDPOINTS[endpoint_name]:
                self._validate_object('path', endpoint_name, path_data)
        '''
        if 'query' in ENDPOINTS[endpoint_name]:
            self._validate_object('query', endpoint_name, query_params)
        if 'body' in ENDPOINTS[endpoint_name]:
            self._validate_object('body', endpoint_name, request_body)

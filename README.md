# python-demandapi-client

[![PyPI version](https://badge.fury.io/py/dynatademand.svg)](https://pypi.org/project/dynatademand/)

<a href="https://github.com/dynata/python-demandapi-client/actions?query=branch%3Adev"><img alt="GitHub Actions status" src="https://github.com/dynata/python-demandapi-client/workflows/python-tests/badge.svg"></a>

A Python client library for the [Dynata Demand API](https://developers.dynata.com/). There are also [go](https://github.com/researchnow/go-samplifyapi-client) and [.NET](https://github.com/researchnow/dotnet-samplifyapi-client) clients available.

## Setup

You can install the Demand API client with:

    pip install dynatademand

You can provide your Demand API credentials in a couple of ways. They can be set in the environment (a sample config is provided in `.env-example`) or you can provide them while creating the client object.

## Example Usage

```python
# You can optionally provide your credentials here instead of environment variables.
demandapi = DemandAPIClient("client_id", "username", "password")
demandapi.authenticate()

# Any function requiring one or more IDs should be provided as positional arguments.
demandapi.get_project(7)

# Provide query parameters as keyword-arguments.
demandapi.get_projects(state="LAUNCHED")

# Functions that send data in a request body accept a python dictionary.
# Your data will be validated against the schemas provided in the Demand API documentation.
project_data = {
  'title': 'My New Survey',
  ...
}
demandapi.create_project(project_data)
```

## Supported API Functions

Links to the Demand API documentation are included for each function.

### Authentication Functions

[Obtain Access Token](https://developers.dynata.com/demand-api-reference/authentication/authentication/post-token): authenticate()  
[Refresh Access Token](https://developers.dynata.com/demand-api-reference/authentication/authentication/post-token-refresh): refresh_access_token()  
[Logout](https://developers.dynata.com/demand-api-reference/authentication/authentication/post-logout): logout()  

### Event Functions

[Get Event](https://developers.dynata.com/demand-api-reference/notifications/events/get-event): get_event(event_id)  
[Get Events](https://developers.dynata.com/demand-api-reference/notifications/events/get-events): get_events(\*\*kwargs)  

### Project Functions

[Buy Project](https://developers.dynata.com/demand-api-reference/core-resources/projects/post-project-buy): buy_project(project_id, buy_data)  
[Close Project](https://developers.dynata.com/demand-api-reference/core-resources/projects/post-close-project): close_project(project_id)  
[Create Project](https://developers.dynata.com/demand-api-reference/core-resources/projects/post-projects): create_project(project_data)  
[Get Project](https://developers.dynata.com/demand-api-reference/core-resources/projects/get-project): get_project(project_id)  
[Get Projects](https://developers.dynata.com/demand-api-reference/core-resources/projects/get-projects): get_projects(\*\*kwargs)  
[Update Project](https://developers.dynata.com/demand-api-reference/core-resources/projects/post-project): update_project(project_id, update_data)  
[Get Project Detailed Report](https://developers.dynata.com/demand-api-reference/core-resources/projects/get-project-detailed-report): get_project_detailed_report(project_id)  
[Get Pricing & Feasibility](https://developers.dynata.com/demand-api-reference/core-resources/pricing-feasibility/get-pricing-feasibility): get_feasibility(project_id)  
[Get Invoice PDF](https://developers.dynata.com/demand-api-reference/billing_invoicing/invoicing/get-invoices): get_invoice(project_id)  
[Get Invoices Summary PDF](https://developers.dynata.com): get_invoices_summary(\*\*kwargs)

### Line Item Functions

[Add Line Item](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/post-lineitems): add_line_item(project_id, lineitem_data)  
[Close Line Item](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/post-lineitem-close): close_line_item(project_id, line_item_id)  
[Get Line Item](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/get-lineitem): get_line_item(project_id, line_item_id)  
[Get Line Items](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/get-lineitems): get_line_items(project_id, \*\*kwargs)  
[Launch Line Item](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/post-lineitem-launch): launch_line_item(project_id, line_item_id)  
[Pause Line Item](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/post-lineitem-pause): pause_line_item(project_id, line_item_id)  
[Update Line Item](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/post-lineitem): update_line_item(project_id, line_item_id, line_item_data)  
[Get Line Item Detailed Report](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/get-detailed-line-item): get_line_item_detailed_report(project_id, line_item_id) 
[Launch Quota cell](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/post-quota-cell-launch): set_quotacell_status(project_id, line_item_id, quota_cell_id, launch)  
[Pause Quota cell](https://developers.dynata.com/demand-api-reference/core-resources/lineitems/post-quota-cell-pause): set_quotacell_status(project_id, line_item_id, quota_cell_id, pause)  

### Misc Functions

[Get Attributes](https://developers.dynata.com/demand-api-reference/data_endpoints/attributes/get-attributes): get_attributes(country_code, language_code, \*\*kwargs)  
[Get Countries](https://developers.dynata.com/demand-api-reference/data_endpoints/countries-languages/get-countries): get_countries(\*\*kwargs)  
[Get Sources](https://developers.dynata.com/demand-api-reference/data_endpoints/supplier-sources/get-sources): get_sources()  
[Get Survey Topics](https://developers.dynata.com/demand-api-reference/data_endpoints/categories/get-survey-topic): get_survey_topics(\*\*kwargs)  

## Contributing

Information on [contributing](CONTRIBUTING.md).

## Testing

To run the tests, you will need to install the development requirements to your environment. It's recommended to create a virtual environment for your installation to avoid any package conflicts.

You can check out the code by running:

    git clone https://github.com/dynata/python-demandapi-client.git
    cd python-demandapi-client

And you can create an environment by running:

    # If you're using Python 2.7
    virtualenv venv

    # Or if you're using Python 3:
    python3 -m venv venv

    source venv/bin/activate
    pip install -r requirements.txt

While your virtual environment is activated, you can run `pytest tests` to run the tests.

# python-demandapi-client

<a href="https://github.com/dynata/python-demandapi-client/actions?query=branch%3Adev"><img alt="GitHub Actions status" src="https://github.com/dynata/python-demandapi-client/workflows/python-tests/badge.svg"></a>

A Python client library for the [Dynata Demand API](https://developers.dynata.com/). There are also [go](https://github.com/researchnow/go-samplifyapi-client) and [.NET](https://github.com/researchnow/dotnet-samplifyapi-client) clients available.

## Setup

The client requires environment variables to be set for the Dynata Demand API credentials. These can be found in `.env-example`.

## Example Usage

    demandapi = DemandAPIClient()
    demandapi.authenticate()
    demandapi.logout()

## Supported API Functions

### Authentication Functions

authenticate()  
refresh_access_token()  
logout()  

### Event Functions

get_event(event_id)  
get_events(\*\*kwargs)  

### Project Functions

buy_project(project_id, buy_data)  
close_project(project_id)  
create_project(project_data)  
get_project(project_id)  
get_projects(\*\*kwargs)  
reconcile_project(project_id, reconcile_data)  
update_project(project_id, update_data)  
get_project_detailed_report(project_id)  
get_feasibility(project_id)  
get_invoice(project_id)  

### Line Item Functions

add_line_item(project_id, lineitem_data)  
close_line_item(project_id, line_item_id)  
get_line_item(project_id, line_item_id)  
get_line_items(project_id, \*\*kwargs)  
launch_line_item(project_id, line_item_id)  
pause_line_item(project_id, line_item_id)  
update_line_item(project_id, line_item_id, line_item_data)  
get_line_item_detailed_report(project_id, line_item_id)  

### Misc Functions

get_attributes(country_code, language_code, \*\*kwargs)  
get_countries(\*\*kwargs)  
get_sources()  
get_survey_topics(\*\*kwargs)  

## Contributing

Information on [contributing](CONTRIBUTING.md).

## Testing

To run the tests,

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    pytest tests
    deactivate

to run the tests for this project.

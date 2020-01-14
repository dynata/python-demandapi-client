# python-demandapi-client

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

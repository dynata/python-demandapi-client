# python-demandapi-client
A Python client library for the Dynata Demand API

## Setup

The client requires environment variables to be set for the Dynata Demand API credentials. These can be found in `.env-example`.

## Example Usage

    demandapi = DemandAPIClient()
    demandapi.authenticate()
    demandapi.logout()

## Contributing

Information on [contributing](CONTRIBUTING.md).

## Testing

Use the command `pytest tests` to run the tests for this project.

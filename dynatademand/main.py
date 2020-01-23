from dynatademand.api import DemandAPIClient

api = DemandAPIClient(client_id='api', username='test', password='test', base_host='https://api.dev.pe.dynata.com')
api.authenticate()

result = api.get_invoices_summary(startDate='2019-06-12', endDate='2019-06-19', extProjectId='010528ef-8984-48c1-a06d-4dae730da027')

print(result)
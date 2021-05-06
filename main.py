from datetime import datetime
from search_console_api_client import SearchConsoleApiClient


date_from = '2020-11-01'
date_to = '2021-04-30'
client = SearchConsoleApiClient('{URL}')
data = client.query_search_analytics(datetime.strptime(date_from, '%Y-%m-%d'), datetime.strptime(date_to, '%Y-%m-%d'), ['query', 'page'])
data.to_csv('{}.csv'.format(date_from), index=False)

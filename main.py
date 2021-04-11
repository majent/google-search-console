from datetime import datetime
from search_console_api_client import SearchConsoleApiClient


param_date = '2021-02-17'
client = SearchConsoleApiClient('url')
data = client.query_search_analytics(datetime.strptime(param_date, '%Y-%m-%d'), ['query', 'page'])
data.to_csv('{}.csv'.format(param_date), index=False)

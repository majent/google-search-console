import pandas as pd
import json
import datetime
from typing import List
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class SearchConsoleApiClient:

    def __init__(self, url):
        self.url = url
        self.service_account_key = json.load(open('service-account-key.json'))
        self.api_client = self._build_google_api_client()

    def query_search_analytics(self, date_from: datetime, date_to: datetime, dimensions: List[str]) -> pd.DataFrame:
        i = 0
        result = None
        while True:
            df = self._query(date_from, date_to, dimensions, i)
            i += 1
            if df is None:
                break
            else:
                result = pd.concat([result, df])
        return result

    def _build_google_api_client(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            self.service_account_key,
            # json.load(self.service_account_key),
            ['https://www.googleapis.com/auth/webmasters.readonly']
        )
        return build('webmasters', 'v3', credentials=credentials)

    def _query(self, date_from: datetime, date_to: datetime, dimensions: List[str], i: int) -> pd.DataFrame:
        max_rows = 25000
        start_date = date_from.strftime('%Y-%m-%d')
        end_date = date_to.strftime('%Y-%m-%d')

        body = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': dimensions,
            'rowLimit': max_rows,
            'startRow': i * max_rows
        }
        print(f'row = {i * max_rows}')

        response = self.api_client.searchanalytics().query(siteUrl=self.url, body=body).execute()
        if 'rows' not in response:
            return None

        df = pd.json_normalize(response['rows'])

        for i, d in enumerate(dimensions):
            df[d] = df['keys'].apply(lambda x: x[i])

        df['date'] = start_date

        df.drop(columns='keys', inplace=True)
        return df

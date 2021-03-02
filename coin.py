import requests
import pandas as pd
from scipy import stats
import time

crypto = 'dogecoin'

url = 'https://rest.coinapi.io/v1/exchangerate/{0}/USD'.format(crypto)
headers = {'X-CoinAPI-Key' : '6A301630-B08B-4B73-8B0B-B04065262D67'}
response = requests.get(url, headers = headers)

content = response.json()
current_price = content['rate']
current_time = content['time']

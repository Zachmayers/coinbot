crypto = 'dogecoin'

url = 'https://rest.coinapi.io/v1/ohlcv/{0}/USD/latest?period_id=1DAY&limit=30'.format(crypto)
headers = {'X-CoinAPI-Key' : '6A301630-B08B-4B73-8B0B-B04065262D67'}
response = requests.get(url, headers=headers)

content = response.json()
df_30 = pd.DataFrame(content)

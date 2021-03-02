# bot.py
import os

import discord
from dotenv import load_dotenv

import requests
import pandas as pd
from scipy import stats
import time

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
coin_api_key = os.getenv('coin-api-key')

# define functions
def COINprices(crypto):
    # get current price
    url = 'https://rest.coinapi.io/v1/exchangerate/{0}/USD'.format(crypto)
    headers = {'X-CoinAPI-Key' : coin_api_key}
    response = requests.get(url, headers = headers)

    content = response.json()
    if content == None:
        return 0
    current_price = content['rate']
    current_time = content['time']

    # get historical prices (30 days)
    url = 'https://rest.coinapi.io/v1/ohlcv/{0}/USD/latest?period_id=1DAY&limit=30'.format(crypto)
    headers = {'X-CoinAPI-Key' : coin_api_key}
    response = requests.get(url, headers=headers)
    content = response.json()
    df_30 = pd.DataFrame(content)

    # get historical prices (90 days)
    url = 'https://rest.coinapi.io/v1/ohlcv/{0}/USD/latest?period_id=1DAY&limit=90'.format(crypto)
    headers = {'X-CoinAPI-Key' : coin_api_key}
    response = requests.get(url, headers=headers)
    content = response.json()
    df_90 = pd.DataFrame(content)

    # calculate percentiles
    day_30_percentile = stats.percentileofscore(df_30.price_close, current_price)
    day_90_percentile = stats.percentileofscore(df_90.price_close, current_price)

    return {'current_price': current_price, 'day_30_percentile': day_30_percentile , 'day_90_percentile': day_90_percentile}

def createMessage(crypto, current_price, day_30_percentile):
    if day_30_percentile <= 20:
        status = 'BARGIN'
    elif day_30_percentile <= 80:
        status = 'TYPICAL BUY'
    else:
        status = 'RIP-OFF'

    percentile_formatted = "{:.1%}".format(day_30_percentile/100)
    current_price_formatted = '${:,.2f}'.format(current_price)

    message = '{0} is a {1} today. The current price of {2} is higher than {3} of closing prices during the last 30 days.'.format(crypto, status, current_price_formatted, percentile_formatted)
    return(message)

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[len(message.content) - 1] == '!':
        print(message.content[:-1])

        crypto = message.content[:-1]
        result = COINprices(crypto)
        if result == 0:
            await message.channel.send("NO!")
        current_price = result['current_price']
        day_30_percentile = result['day_30_percentile']
        day_90_percentile = result['day_90_percentile']
        response = createMessage(crypto,current_price, day_30_percentile)
        print(crypto, current_price, day_30_percentile, day_90_percentile)
        await message.channel.send(response)

client.run(TOKEN)

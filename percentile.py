day_30_percentile = stats.percentileofscore(df_30.price_close, current_price)

# determine
if day_30_percentile <= 20:
    status = 'BARGIN'
elif day_30_percentile <= 80:
    status = 'NORMAL'
else:
    status = 'RIP-OFF'

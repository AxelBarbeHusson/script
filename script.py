# import the Shrimpy library for crypto exchange websockets
import shrimpy

# a sample error handler, it simply prints the incoming error
def error_handler(err):
    print(err)

exchanges_bbo = {}

# define the handler to manage the output stream
def handler(msg):
    bid_price = msg['content']['bids'][0]['price']
    ask_price = msg['content']['asks'][0]['price']
    exchanges_bbo[msg['exchange']] = {'bid': float(bid_price), 'ask': float(ask_price)}
    best_bid = 0.0
    best_ask = 100000.0
    best_bid_exchange = ''
    best_ask_exchange = ''
    for key, value in exchanges_bbo.items():
        if value['bid'] > best_bid:
            best_bid = value['bid']
            best_bid_exchange = key
        if value['ask'] < best_ask:
            best_ask = value['ask']
            best_ask_exchange = key
    if best_bid > best_ask:
        print("sell on " + best_bid_exchange + " for " + str(best_bid))
        print("buy on " + best_ask_exchange + " for " + str(best_ask))
    else:
        print("No Arbitrage Available")


# input your Shrimpy public and private key
public_key = '2060489f7ff9584718c8d54d7419aeed4b8caf1bc3eb139d15964c918d0a9bab'
private_key = '04201c22fe1061a50c8f57ad421cf2f9554239969f42e33b0c49a2237cfff2b9b4526c02079ef7876774f3f67a418ab73843b29c15f72eb07c6d27bcbb8c533e'

# create the Shrimpy websocket client
api_client = shrimpy.ShrimpyApiClient(public_key, private_key)
raw_token = api_client.get_token()
client = shrimpy.ShrimpyWsClient(error_handler, raw_token['token'])

# connect to the Shrimpy websocket and subscribe
client.connect()

# select exchanges to arbitrage
exchanges = ["bittrex", "binance", "kucoin"]
pair = "btc-usdt"

# subscribe to the websockets for the given pair on each exchange
for exchange in exchanges:
    subscribe_data = {
        "type": "subscribe",
        "exchange": exchange,
        "pair": pair,
        "channel": "bbo"
    }
    client.subscribe(subscribe_data, handler)

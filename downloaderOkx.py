import asyncio
import websockets
import json
import re
def remove_whitespace(s):
    return re.sub(r'\s+', '', s)  # \s matches any whitespace character (space, newline, tab, etc.)

async def okx_market_depth(symbol):
    ws_url = "wss://ws.okx.com:8443/ws/v5/public"
    filename = f"database/{symbol}_okx.txt"
    subscription_message = {
        "op": "subscribe",
        "args": [{
            "channel": "books5",  # Use 'books5' for top 5 levels of market depth (public data)
            "instId": symbol
        }]
    }
    
    try:
        async with websockets.connect(ws_url) as websocket:
            await websocket.send(json.dumps(subscription_message))  # Send subscription message
            
            with open(filename, 'a') as file:
                while True:
                    try:
                        data = await websocket.recv()
                        data_str = json.dumps(json.loads(data), indent=2)  # Convert and pretty print JSON to string
                        file.write(remove_whitespace(data_str) + "\n")  # Write string to file
                        # print(data_str)
                        # print("_________")
                    except websockets.exceptions.ConnectionClosed as e:
                        print(f"Connection closed with error: {e}")
                        break
    except asyncio.CancelledError:
        print(f"Stream closed after timeout for {symbol}")
    except Exception as e:
        print(f"An error occurred for {symbol}: {e}")

async def main():
    symbols = [
        "ADA-BTC", "ADA-ETH", "ADA-USDT", "ATOM-ETH", "ATOM-USDT",
        "BTC-ADA", "BTC-ETH", "BTC-LTC", "BTC-USDT", "DOT-ETH", "DOT-USDT",
        "ETH-ADA", "ETH-ATOM", "ETH-BTC", "ETH-DOT", "ETH-LTC", "ETH-USDT",
        "LTC-BTC", "LTC-ETH", "LTC-USDT", "USDT-ADA", "USDT-ATOM", "USDT-BTC",
        "USDT-DOT", "USDT-ETH", "USDT-LTC"
    ]
    
    for symbol in symbols:
        try:
            print(f"downloading data for {symbol}")
            await asyncio.wait_for(okx_market_depth(symbol), timeout=300)  # 5 seconds timeout
        except asyncio.TimeoutError:
            print(f"Timeout reached for {symbol}")
        except Exception as e:
            print(f"Program closed due to an error: {e}")

asyncio.get_event_loop().run_until_complete(main())

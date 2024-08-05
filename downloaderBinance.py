import asyncio
import websockets
import json
async def binance_l3_market_depth(symbol):
    ws_url = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@depth20@100ms"
    filename = f"database/{symbol}_binance.txt"
    try:
        async with websockets.connect(ws_url) as websocket:
            with open(filename, 'a') as file:
                while True:
                    try:
                        data = await websocket.recv()
                        data_str = json.dumps(data)  # Convert JSON to string
                        file.write(data_str + "\n")  # Write string to file
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
        "ADABTC", "ADAETH", "ADAUSDT", "ATOMETH", "ATOMUSDT",
        "BTCADA", "BTCETH", "BTCLTC", "BTCUSDT", "DOTETH", "DOTUSDT",
        "ETHADA", "ETHATOM", "ETHBTC", "ETHDOT", "ETHLTC", "ETHUSDT",
        "LTCBTC", "LTCETH", "LTCUSDT", "USDTADA", "USDTATOM", "USDTBTC",
        "USDTDOT", "USDTETH", "USDTLTC"
    ]
    for symbol in symbols:
        try:
            print(f"Downloading data for {symbol}")
            await asyncio.wait_for(binance_l3_market_depth(symbol), timeout=300)  # 5 seconds timeout
        except asyncio.TimeoutError:
            print(f"Timeout reached for {symbol}")
        except Exception as e:
            print(f"Program closed due to an error: {e}")

asyncio.get_event_loop().run_until_complete(main())

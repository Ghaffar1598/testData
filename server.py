import asyncio
import websockets
import json
import os

# Set to keep track of connected clients
clients = set()

async def handle_message(websocket, path):
    # Add the new client to the set of clients
    clients.add(websocket)
    try:
        async for message in websocket:
            try:
                # Parse the received message
                request = json.loads(message)
                symbol = request.get("symbol")
                exchange = request.get("exchange")
                
                # Build the filename based on the symbol and exchange
                filename = f"database/{symbol}_{exchange}.txt"
                
                if os.path.exists(filename):
                    # Read the file content line by line and send each line as a message
                    with open(filename, 'r') as file:
                        for line in file:
                            # Strip any extraneous whitespace characters
                            line = line.strip()
                            if line:
                                await websocket.send(line)
                            await asyncio.sleep(0.1)  # Optional: Add a small delay to avoid flooding
                    # Send an end-of-file marker or confirmation message
                    await websocket.send(json.dumps({"status": "done"}))
                else:
                    # Send an error message if the file does not exist
                    await websocket.send(json.dumps({"error": "File not found"}))
            
            except json.JSONDecodeError:
                # Handle JSON parsing errors
                await websocket.send(json.dumps({"error": "Invalid JSON format"}))
            except Exception as e:
                # Handle any other exceptions
                await websocket.send(json.dumps({"error": str(e)}))
    finally:
        # Remove the client from the set when disconnected
        clients.remove(websocket)

async def main():
    async with websockets.serve(handle_message, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Start the WebSocket server
asyncio.run(main())

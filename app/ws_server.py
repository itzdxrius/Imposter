import asyncio
import json
import threading

import websockets

HOST = "0.0.0.0"
PORT = 8765

_loop = None
_rooms = {}
_rooms_lock = threading.Lock()


async def _register(websocket, room_id):
    with _rooms_lock:
        _rooms.setdefault(room_id, set()).add(websocket)


async def _unregister(websocket, room_id):
    with _rooms_lock:
        clients = _rooms.get(room_id)
        if clients:
            clients.discard(websocket)
            if not clients:
                _rooms.pop(room_id, None)


async def _handle_connection(websocket):
    room_id = None
    try:
        async for raw_message in websocket:
            try:
                message = json.loads(raw_message)
            except (TypeError, ValueError):
                continue
            if message.get("type") == "join":
                room_id = str(message.get("room_id"))
                await _register(websocket, room_id)
    except websockets.ConnectionClosed:
        pass
    finally:
        if room_id:
            await _unregister(websocket, room_id)


async def _broadcast(room_id, payload):
    with _rooms_lock:
        clients = list(_rooms.get(room_id, ()))
    message = json.dumps(payload)
    for client in clients:
        try:
            await client.send(message)
        except websockets.ConnectionClosed:
            await _unregister(client, room_id)


async def _serve_forever():
    global _loop
    _loop = asyncio.get_running_loop()
    async with websockets.serve(_handle_connection, HOST, PORT):
        await asyncio.Future()


def start_in_background():
    thread = threading.Thread(target=lambda: asyncio.run(_serve_forever()), daemon=True)
    thread.start()


def broadcast_player_list(room_id, players):
    if _loop is None:
        return
    payload = {"type": "player_list_update", "players": players}
    asyncio.run_coroutine_threadsafe(_broadcast(str(room_id), payload), _loop)

## Creating a standalone WebSocket Server with FastApi and JWT Authentication in Python

In this post, I will show you how to create a WebSocket server in Python that uses JWT tokens for authentication. The server is designed to be independent of the main process, making it easy to integrate into existing applications. The client-side JavaScript will handle reconnections incrementally.

The WebSocket server will be created using FastApi, the web framework built on top of Starlette. This is the entrypoint.

```python
import logging

from fastapi import FastAPI

from lib.websockets import setup_app

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level='INFO',
    datefmt='%d/%m/%Y %X')

logger = logging.getLogger(__name__)
SECRET_KEY = "your_secret_key"

app = FastAPI()

app = setup_app(
    app=app,
    base_path='/ws',
    jwt_secret_key=SECRET_KEY,
)
```

The `setup_app` function is defined in the `lib.websockets` module. This function will set up the WebSocket server and the necessary routes.

```python
def setup_app(app, jwt_secret_key: str, base_path='/ws', jwt_algorithm: str = "HS256"):
    ws_router = get_ws_router(
        jwt_secret_key=jwt_secret_key,
        jwt_algorithm=jwt_algorithm,
        base_path=base_path
    )
    current_dir = Path(__file__).parent
    static_dir = current_dir / "static/js"

    app.mount("/js", StaticFiles(directory=static_dir), name="js")
    app.include_router(ws_router)

    return app
```

The `get_ws_router` function is defined in the same module. This function will create the WebSocket router and the necessary routes.

```python
def get_ws_router(jwt_secret_key: str, base_path='ws', jwt_algorithm: str = "HS256"):
    ws_router = APIRouter()

    current_dir = Path(__file__).parent
    static_dir = current_dir / "static/js"
    ws_router.mount(f"{base_path}/js", StaticFiles(directory=static_dir), name="js")

    manager = ConnectionManager(jwt_secret_key=jwt_secret_key, jwt_algorithm=jwt_algorithm)

    @ws_router.post(f"{base_path}/emmit")
    async def emmit_endpoint(request: Request):
        payload = await request.json()
        await manager.broadcast(payload["channel"], payload["payload"])
        return True

    @ws_router.websocket(f"{base_path}/")
    async def websocket_endpoint(websocket: WebSocket):
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=1008)
            raise HTTPException(status_code=401, detail="Token required")

        await manager.connect(websocket, token)
        try:
            while True:
                message: Message = await websocket.receive()
                if message["type"] == "websocket.disconnect":
                    manager.disconnect(websocket)
                    break
        except WebSocketDisconnect:
            manager.disconnect(websocket)

    return ws_router
```

Websockets are bidirectional communication channels that allow real-time data transfer between clients and servers, but I prefer to avoid the communication from the client to the server. When a client wants to send a message to the server, it will send an HTTP POST request to the `/emit` endpoint (via the main process). The server will then broadcast the message to all connected clients. The client will only receive messages from the server. Because of that we need a main wsgi process using FastApi or another web framework to handle the HTTP requests. 

This an example with FastApi:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Chat</title>
</head>
<body>
<h1>WebSocket Chat</h1>

<input type="text" id="messageText" autocomplete="off"/>
<button onclick="sendMessage()">Send</button>

<ul id='messages'>
</ul>
<script src="//localhost:8000/js/websockets.js"></script>
<script>
    async function sendMessage() {
        const channel = 'chat';
        const url = `/emit/${channel}`;
        const input = document.getElementById("messageText");
        const message = input.value;
        input.value = '';
        const body = JSON.stringify({channel: 'chat1', payload: message});
        const headers = {'Content-Type': 'application/json'};

        try {
            const response = await fetch(url, {method: 'POST', headers: headers, body: body});
        } catch (error) {
            console.error('Error:', error);
        }
    }

    (async function () {
        const getToken = async () => {
            const response = await fetch('/token');
            const {token} = await response.json();
            return token;
        };

        const messageCallback = (event) => {
            const messages = document.getElementById('messages');
            const message = document.createElement('li');
            message.textContent = event.data;
            messages.appendChild(message);
        };

        const wsManager = new WebSocketManager('ws://localhost:8000/ws/', getToken, messageCallback);
        await wsManager.connect();
    })();

</script>
</body>
</html>
```



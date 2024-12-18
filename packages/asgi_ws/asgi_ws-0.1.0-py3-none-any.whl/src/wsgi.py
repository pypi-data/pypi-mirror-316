from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
app = FastAPI()

DELTA = timedelta(seconds=5)

def emit_message_to_channel(channel, payload):
    url = "http://127.0.0.1:8000/ws/emmit"
    response = requests.post(
        url,
        json=dict(channel=channel, payload=payload),
        headers={"Content-Type": "application/json"})
    return response.ok

@app.post("/emit/{channel}")
async def send_message(channel: str, request: Request):
    payload = (await request.json()).get("payload")
    emit_message_to_channel(channel, payload)
    return JSONResponse(content={"message": "Message sent successfully"})

def create_jwt_token(data: dict, expires_delta: timedelta = DELTA):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get("/token")
async def token():
    return JSONResponse(content={"token": create_jwt_token({"user": "user"})})

html_content = """
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
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return html_content
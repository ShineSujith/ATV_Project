from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import TextInput
import json
import aio_pika
import os

app = FastAPI()

#Rabbit MQ
EXCHANGE_NAME = "ATV_Project_Exchange"
RABBIT_URL = os.getenv("RABBIT_URL")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_exchange():
    """
    Open a connection, create a channel and declare a topic exchange.
    Returns (connection, channel, exchange).
    """
    conn = await aio_pika.connect_robust(RABBIT_URL)
    ch = await conn.channel()
    ex = await ch.declare_exchange(EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC)
    return conn, ch, ex

@app.post("/api/sendTextInput")
async def send_text_input(payload: TextInput):
    conn, ch, ex = await get_exchange()
    msg = aio_pika.Message(body=json.dumps(payload.payload).encode())
    await ex.publish(msg, routing_key="text.send")
    await conn.close()
    return {"status": "sent"}

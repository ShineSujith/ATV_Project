from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .models import TextInput
import json
import aio_pika
import os
import speech_recognition as sr
import threading

listening = False
thread = None

recognizer = sr.Recognizer()

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

async def publish_text(text):
    conn, ch, ex = await get_exchange()
    msg = aio_pika.Message(body=json.dumps(text).encode())
    await ex.publish(msg, routing_key="text.send")
    await conn.close()
    return {"status": "sent"}

def listen_loop():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        print("Listening...")

        while listening:
            try:
                audio = recognizer.listen(source)

                text = recognizer.recognize_google(audio)
                print("TEXT:", text)

                publish_text(text)

            except sr.UnknownValueError:
                print("Could not understand audio")

            except Exception as e:
                print("Error:", e)

@app.post("/api/start")
def start():
    global listening, thread
    if not listening:
        listening = True
        thread = threading.Thread(target=listen_loop)
        thread.start()
    return {"status": "started"}


@app.post("/api/stop")
def stop():
    global listening
    listening = False
    return {"status": "stopped"}

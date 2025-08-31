# main.py

import pika
import pymongo
from datetime import datetime
import structlog

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
log = structlog.get_logger()

# MongoDB setup
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["mydatabase"]
collection = db["messages"]

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='test_queue')  # Ensure the queue exists

def callback(ch, method, properties, body):
    message = body.decode("utf-8")
    doc = {
        "timestamp": datetime.utcnow(),
        "message": message
    }
    collection.insert_one(doc)
    log.info("message_stored", **doc)

channel.basic_consume(
    queue='test_queue',
    on_message_callback=callback,
    auto_ack=True
)

log.info("waiting_for_messages")
channel.start_consuming()
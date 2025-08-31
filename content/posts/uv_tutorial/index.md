+++
title = "Optimizing Docker Images for Python Applications"
date = "2025-08-31T12:44:33-04:00"
author = "Noah Hefner"
cover = ""
tags = ["python", "docker", "uv"]
keywords = ["python", "docker", "uv", "container"]
description = ""
showFullContent = false
readingTime = false
draft = true
hideComments = false
+++

## Introduction

In my day job, I have recently been working a lot with Docker containers that run Python applications. This has led me down a deep rabbit hole of optimizing these Docker container images. In this article, I will attempt to document the journey that I went on to achieve, in my opinion, a pretty solid approach for containerizing Python applications.

The objectives are as follows:

- Minimize the size of the final Docker image
- Minimize build time for the Docker image

## Sample Project

To set the stage for this tutorial, lets assume a very basic Python program with a few dependencies. The program below does the following:

- Listens for a message from RabbitMQ
- Upon consuming a message, write the message and a timestamp to a MongoDB database

```python
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
```

This program uses the `pika` package for interacting with RabbitMQ, `pymongo` for writing to the MongoDB database, and `structlog` for structured logging in `JSON` format. Let's also assume our Python project makes use of some developer dependencies. My favorites are `black` for code formatting, `isort` for sorting imports, and `autoflake` for removing unused imports. If we generate a `requirments.txt` file for the project, it would look like this:

```plaintext
# requirments.txt
pika==1.3.2
pymongo==4.10.1
structlog==24.4.0
black==24.8.0
isort==5.13.2
autoflake==2.3.1
```

## Containerization: Take One

With the basics of our project established, lets take a look at one way we can containerize this application. Consider the following `Dockerfile`:

```dockerfile
# Start from Ubuntu
FROM ubuntu:24.04

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv

# Set work directory
WORKDIR /app

# Create virtual environment
RUN python3 -m venv /opt/venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]
```

In this Dockerfile, we start with Ubuntu 24.04 as the base image. Next, we install Python, `pip`, and `venv`. Then, we create a Python virtual environment using `venv`, add it to our path, then install our Python dependencies from the `requirments.txt` file using `pip`. Finally, we copy over the `main.py` file and execute it.

Building the image with this Dockerfile, we get the following output:

```plaintext
[+] Building 115.1s (12/12) FINISHED                                                          docker:default
 => [internal] load build definition from Dockerfile.take_one                                           0.1s
 => => transferring dockerfile: 665B                                                                    0.0s
 => [internal] load metadata for docker.io/library/ubuntu:24.04                                         2.2s
 => [internal] load .dockerignore                                                                       0.1s
 => => transferring context: 2B                                                                         0.0s
 => [1/7] FROM docker.io/library/ubuntu:24.04@sha256:7c06e91f61fa88c08cc74f7e1b7c69ae24910d745357e0dfe  6.9s
 => => resolve docker.io/library/ubuntu:24.04@sha256:7c06e91f61fa88c08cc74f7e1b7c69ae24910d745357e0dfe  0.2s
 => => sha256:7c06e91f61fa88c08cc74f7e1b7c69ae24910d745357e0dfe1d2c0322aaf20f9 6.69kB / 6.69kB          0.0s
 => => sha256:35f3a8badf2f74c1b320a643b343536f5132f245cbefc40ef802b6203a166d04 424B / 424B              0.0s
 => => sha256:e0f16e6366fef4e695b9f8788819849d265cde40eb84300c0147a6e5261d2750 2.29kB / 2.29kB          0.0s
 => => sha256:b71466b94f266b4c2e0881749670e5b88ab7a0fd4ca4a4cdf26cb45e4bde7e4e 29.72MB / 29.72MB        1.3s
 => => extracting sha256:b71466b94f266b4c2e0881749670e5b88ab7a0fd4ca4a4cdf26cb45e4bde7e4e               4.7s
 => [internal] load build context                                                                       0.3s
 => => transferring context: 1.45kB                                                                     0.0s
 => [2/7] RUN apt-get update && apt-get install -y     python3     python3-pip     python3-venv        75.2s
 => [3/7] WORKDIR /app                                                                                  0.1s 
 => [4/7] RUN python3 -m venv /opt/venv                                                                 5.6s 
 => [5/7] COPY requirements.txt .                                                                       0.2s 
 => [6/7] RUN pip install --no-cache-dir -r requirements.txt                                            9.0s 
 => [7/7] COPY src/main.py main.py                                                                      0.2s 
 => exporting to image                                                                                 15.1s 
 => => exporting layers                                                                                15.0s 
 => => writing image sha256:7f305fbf83187c0a6ac0ec601f15ceab932f63433e63d5deec5cbb7020e02306            0.0s
```

Notice from the first line of this output that the image took almost two minutes to build. That's quite a long time for such a simple script!

```plaintext
[+] Building 115.1s (12/12) 
```

We can also check the size of the image using the `docker image inspect` command:

```json
[
    {
        "Id": "sha256:7f305fbf83187c0a6ac0ec601f15ceab932f63433e63d5deec5cbb7020e02306",
        "RepoTags": [],
        "RepoDigests": [],
        "Parent": "",
        "Comment": "buildkit.dockerfile.v0",
        "Created": "2025-08-31T13:59:26.046247413-04:00",
        "DockerVersion": "",
        "Author": "",
        "Architecture": "amd64",
        "Os": "linux",
        "Size": 589982747,
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/x7evtxn5ko5prg38egtj3108v/diff:/var/lib/docker/overlay2/6vy6xzzttwioqkwmui2p32t3x/diff:/var/lib/docker/overlay2/nha5u6beay7qkhvxrh75uxb9p/diff:/var/lib/docker/overlay2/d42zkclw5dpznkknw9faw9y9g/diff:/var/lib/docker/overlay2/ni6ccxrx41m6qzd76w9668ab8/diff:/var/lib/docker/overlay2/f3a841789a23e8df2012e3f4ee27d16ccde44036bda182f9d24e65bb3e45b75b/diff",
                "MergedDir": "/var/lib/docker/overlay2/6ah4uigim2ih9b1xs6190nz7n/merged",
                "UpperDir": "/var/lib/docker/overlay2/6ah4uigim2ih9b1xs6190nz7n/diff",
                "WorkDir": "/var/lib/docker/overlay2/6ah4uigim2ih9b1xs6190nz7n/work"
            },
            "Name": "overlay2"
        },
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:cd9664b1462ea111a41bdadf65ce077582cdc77e28683a4f6996dd03afcc56f5",
                "sha256:490549fd05a0bfdb9cffdf068573eb00dd9e2446660a635dc75d7cdc7cd7fb35",
                "sha256:49e8685bade2abd47164d4fe00dee489ecd62d33d6599c14791bc1575487a8b7",
                "sha256:d86e36a128358d1833aebfd11bdfdc331c95ec796d8e05dce1330b50095357dc",
                "sha256:42ea22f9e492e8e3550c4deb054060a0b3573b894566e58fd9060242209af0a7",
                "sha256:b3f0a12bdf6589aff587f4a80de52c4ef9e2030f038f762ca5338b70d37b7773",
                "sha256:04ab7ffdb4b43685b118753bc2faa48a29831f7183484c12eb42ca37b3beeff1"
            ]
        },
        "Metadata": {
            "LastTagTime": "0001-01-01T00:00:00Z"
        },
        "Config": {
            "ArgsEscaped": true,
            "Cmd": [
                "python",
                "main.py"
            ],
            "Entrypoint": null,
            "Env": [
                "PATH=/opt/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Labels": {
                "org.opencontainers.image.ref.name": "ubuntu",
                "org.opencontainers.image.version": "24.04"
            },
            "OnBuild": null,
            "User": "",
            "Volumes": null,
            "WorkingDir": "/app"
        }
    }
]
```

You can see by the size field that the image is over half a gigabyte! **Surely** we can do better than that.

```plaintext
"Size": 589982747,
```

## Take Two

Even if you're new to containerization, there's a good chance you've already noticed the biggest red flag from our first attempt: using Ubuntu as the base image. 

By chosing a larger base image, our final image is going to contain a bunch of system libraries and utilities that our Python application doesn't need at runtime. The first improvement we can make is to select a slimmer base image that contains a lot less bloat. A good choice would be the `python:3.13-slim` image. This image is based on Debian, has Python preinstalled, and contains much less bloat than the Ubuntu image. 

Here's the updated `Dockerfile`:

```dockerfile
# Start from Python slim image
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]
```

Building this image with Docker, we can already see some huge improvements. The build time has been reduced from 115 seconds to just 30 seconds. This is because the base image

```plaintext
[+] Building 30.9s (11/11) FINISHED
```

```plaintext
"Size": 150981771,
```

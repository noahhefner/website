+++
title = "Optimizing Docker Images for Python Applications"
date = "2025-08-31T12:44:33-04:00"
author = "Noah Hefner"
cover = "docker_x_python.drawio.png"
tags = ["python", "docker", "uv"]
keywords = ["python", "docker", "uv", "container"]
description = "Covers containerizing a basic Python app with Docker and uv, from base image selection to multi-stage builds for a slimmer, faster, and more secure image."
showFullContent = false
readingTime = false
hideComments = false
draft = true
+++

In my day job, I have recently been working a lot with Docker containers that run Python applications. This has led me down a deep rabbit hole of optimizing these Docker container images. In this article, I will attempt to document the journey that I went on to achieve, in my opinion, a pretty solid approach for containerizing Python applications.

What does it mean to "optimize" a Docker image? In my experience, there are three key focus areas when it comes to containerizaiton:

1. **Build Time**: The amount of time it takes to build the container image. The longer it takes to build an image, the more of a pain in the neck it is to work with. If am image takes a long time to build, it becomes cumbersome to work with in a local development environment and can slow down CI-CD pipelines.
2. **Image Size**: The total size of the image after it is built. Tangentally related to build time, big images can slow down CD if the server is constantly having to download large image files. Smaller images result in faster deployments.
3. **Security Best Practices**: Containerization is not a security crutch. Containerized applications still need to follow security best practices to protect against bad actors.

This article will focus more heavily on the first two points, but I will include some security notes as well. We will start with an "unoptimized" image, then progressively enhance it by reducing the build time, reducing the image size, and improving the security of the image.

## Example Project

To set the stage for this article, lets assume a very basic Python program that makes use of a few dependency modules. The program below does the following:

- Creates a `structlog` configuration and initializes a logger object
- Creates a connection to a MongoDB database
- Creates a connection to RabbitMQ
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
pymongo==4.14.1
structlog==25.4.0
black==25.1.0
isort==6.0.1
autoflake==2.3.1
```



## Take One - Containerization with Ubuntu

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

In this Dockerfile, we start with Ubuntu 24.04 as the base image. Next, we install Python, `pip`, and `venv`. Then, we create a Python virtual environment using `venv`, add it to our path, then install our Python dependencies from the `requirments.txt` file using `pip`. Finally, we copy over the `main.py` file and execute it. This is a standard setup for containerizing a Python application.

To build our image, we can use the `docker build` command, along with a few options. The `-f take_1/Dockerfile` flag is to specify which Dockerfile to use. The `-t take_one:latest` will tag the image as `take_one:latest`. The period at the end specifies the context for the build (the current working directory in this case.)

```sh
docker build -f take_1/Dockerfile -t take_one:latest .
```

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

```json
"Size": 589982747
```

## Take Two - Choosing the right base image

Even if you're new to containerization, there's a good chance you've already noticed the biggest red flag from our first attempt: using Ubuntu as the base image. When `apt` installs Python into Ubuntu, it will also pull in a ton of other system dependencies, resulting in the 500MB image.

A good first step to reduce the overall image size is to **chose a slim base image**. For this article, I will use the `python:3.13-alpine3.22` image. This is an Alpine-based image with Python preinstalled. This image is very small and should result in a big reduction in build time.

Lets rebase our `Dockerfile` on `python:3.13-alpine3.22`:

```dockerfile
# Start from alpine image
FROM python:3.13-alpine3.22

# Set work directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install
COPY take_2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]
```

We can build the image with the following command:

```sh
docker build -f Dockerfile.take_2 -t take_two:latest .
```

We can already see some huge improvements in our output. The build time has been reduced from 115 seconds to just 42 seconds.

```plaintext
[+] Building 40.9s (11/11) FINISHED
```

Additionally, we end up with a much smaller resulting image, just 76MB:

```json
"Size": 76136781
```

For very small applications with few dependencies, this setup is pretty solid. However, for big projects that have lots of dependencies, there is still room for improvement. Next, we will swap `pip` for a faster dependency resolution tool for some additional speed gains.

## Take Three - Using [`uv`](https://github.com/astral-sh/uv) for dependency management

Up until this point, we've used `pip` to download all our dependency modules. While `pip` does get the job done, there exist more ergonomic and performant tools for installing Python modules. In this article, we will use `uv`, a Python project management utility developed by [Astral](https://astral.sh/) that prides itself on fast dependency resolution. `uv` bundles functionality from a handful of Python utilities like `venv` and `pip` into one slim package.

Astral *does* [publish thier own Docker images](https://docs.astral.sh/uv/guides/integration/docker/#available-images), but I prefer to simply copy the `uv` binary from the distro-less `uv` image as described [here](https://docs.astral.sh/uv/guides/integration/docker/#installing-uv) in the `uv` documentation. This method allows me to update my containers base image independently of the `uv` binary, without relying on Astral to update their images.

Here's what our `Dockerfile` looks like after swapping `pip` for `uv`:

```dockerfile
# Start from Python Alpine image
FROM python:3.13-alpine3.22

# Copy the uv binary from the distroless uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/app/.venv/bin:$PATH"

# Copy requirements and install
COPY take_3/pyproject.toml .

# Install Python modules
RUN uv sync --no-cache

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]
```

Note that I have also swapped the `requirements.txt` file for a `pyproject.toml` file. (This is the default for `uv` projects.) `pyproject.toml` is more more flexible than a `requirements.txt` file.

```toml
# pyproject.toml
[project]
name = "python-container-article"
version = "0.1.0"
description = "Example pyproject.toml file"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "autoflake>=2.3.1",
    "black>=25.1.0",
    "isort>=6.0.1",
    "pika>=1.3.2",
    "pymongo>=4.14.1",
    "structlog>=25.4.0",
]
```

We can build the image with the following command:

```sh
docker build -f Dockerfile.take_2 -t take_two:latest .
```

We see a smaller, but still significant reduction in build time:

```
[+] Building 27.3s (14/14) FINISHED
```

The size of the image did increase a fair bit from the previous iteration, but we will come back to that later.

```json
"Size": 101297013
```

## Take Four - Removing Developer Dependencies

Our `pyproject.toml` file contains a list of all the dependencies in our project, even dependencies that are only used for development and are not needed at run time such as `black`, `isort`, and `autoflake`. Running a shell in the image and inspecting the virtual environment, we can see that those modules are indeed being included in the final image.

```plaintext
/app/.venv/lib/python3.12/site-packages # ls
LICENSE                          click                            pathspec-0.12.1.dist-info
README.md                        click-8.2.1.dist-info            pika
_black_version.py                dns                              pika-1.3.2.dist-info
_virtualenv.pth                  dnspython-2.7.0.dist-info        platformdirs
_virtualenv.py                   gridfs                           platformdirs-4.4.0.dist-info
autoflake-2.3.1.dist-info        isort                            pyflakes
autoflake.py                     isort-6.0.1.dist-info            pyflakes-3.4.0.dist-info
black                            mypy_extensions-1.1.0.dist-info  pymongo
black-25.1.0.dist-info           mypy_extensions.py               pymongo-4.14.1.dist-info
blackd                           packaging                        structlog
blib2to3                         packaging-25.0.dist-info         structlog-25.4.0.dist-info
bson                             pathspec                         test_autoflake.py
```

We can rework our `pyproject.toml` file to use [dependency groups](https://docs.astral.sh/uv/concepts/projects/sync/#syncing-development-dependencies) so that we can exclude those modules when we build the image for production. Using `uv`, we can remove and reinstall these modules into the `dev` dependency group using the following commands:

```sh
uv remove black isort autoflake
uv add --dev black isort autoflake
```

The `--dev` flag will add those modules to a dependency group called `dev` containing those three modules. Here is the updated `pyproject.toml` file:

```toml
[project]
name = "python-container-article"
version = "0.1.0"
description = "Example pyproject.toml file"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "pika>=1.3.2",
    "pymongo>=4.14.1",
    "structlog>=25.4.0",
]

[dependency-groups]
dev = [
    "autoflake>=2.3.1",
    "black>=25.1.0",
    "isort>=6.0.1",
]
```

To exclude the `dev` dependency group modules from the final image, we can add the `--no-group dev` flag to our `uv sync` command.

```diff
- RUN uv sync --no-cache
+ RUN uv sync --no-cache --no-group dev
```

Now when we inspect the virtual environment inside the image, we don't have those development-only dependencies anymore.

```plaintext
/app/.venv/lib/python3.12/site-packages # ls
_virtualenv.pth             dnspython-2.7.0.dist-info   pymongo
_virtualenv.py              gridfs                      pymongo-4.14.1.dist-info
bson                        pika                        structlog
dns                         pika-1.3.2.dist-info        structlog-25.4.0.dist-info
```

We also get a small improvement in build time:

```plaintext
[+] Building 24.3s (14/14) FINISHED
```

And the image size is reduced from take three:

```json
"Size": 98975390
```

## Take Five - Removing Unnecessary Tools

We've removed unnessessary Python packages, but there is still more we can remove. Since we're using a single stage Dockerfile, the `uv` binary is included in the final image. We can see this by executing a shell on our image from the previous section and inspecting the `/bin` directory.

```plaintext
/app # cd /bin
/bin # ls -al | grep uv
-rwxr-xr-x    1 root     root      45564832 Aug 28 21:00 uv
/bin # 
```

At runtime, there is no need for `uv`, so it is safe (and good practice) to omit the binary from our final image. We can do this by splitting our Dockerfile into a [multi-stage build](https://docs.docker.com/build/building/multi-stage/). 

```dockerfile
# -----------------------
# Stage 1: Build
# -----------------------
FROM python:3.13-alpine3.22 AS builder

# Copy the uv binary from the distroless uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/app/.venv/bin:$PATH"

# Copy requirements and install dependencies
COPY take_5/pyproject.toml .
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Runtime
# -----------------------
FROM python:3.13-alpine3.22 AS runner

# Set work directory
WORKDIR /app

# Copy venv from builder stage
COPY --from=builder /app/.venv /app/.venv

# Ensure venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]
```

The first stage of this Dockerfile is the "build" stage. In this stage, we pull in the `uv` binary, create the virtual environment, and download our dependencies.

The second stage of the Dockerfile is the "run" stage. Since we're stating this stage from a bare `python:alpine` image, we don't inherit the `uv` binary from the first stage. In this stage, we simply copy over the virtual environment files that were created in the build stage and execute the script.

We can build the image with the following command:

```sh
docker build -f take_5/Dockerfile -t take_five:latest .
```

Build time remains roughly the same:

```plaintext
[+] Building 24.1s (16/16) FINISHED
```

The overall image size, however, has been cut down to under 50MB:

```json
"Size": 49673398
```

## Take Six - Security

The last thing we want to address with this image is security. If we run a shell with the take five image and run a `whoami`, you can see that the default user is root:

```plaintext
docker run -it take_five:latest sh
/app # whoami
root
/app #
```

This is [considered bad practice](https://www.docker.com/blog/understanding-the-docker-user-instruction/). If the container is compromised, the attacker would have root access to all the resources allocated to the container. As a safegaurd, it is considered best practice to create a non-root user and execute the container as that user.

In our Dockerfile, we can update the runner stage to create a new user and execute our script as that user.

```dockerfile
# -----------------------
# Stage 1: Build
# -----------------------
FROM python:3.13-alpine3.22 AS builder

# Copy the uv binary from the distroless uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy requirements and install dependencies
COPY take_5/pyproject.toml .
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Runtime
# -----------------------
FROM python:3.13-alpine3.22 AS runner

# Set work directory
WORKDIR /app

# Copy venv from builder stage
COPY --from=builder /app/.venv /app/.venv

# Ensure venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY src/main.py main.py

# Create a non-root user
RUN addgroup -S demo && adduser -S demo -G demo

# Give the non-root user permission to run the script
RUN chown demo:demo /app/main.py && \
    chmod u+rwx /app/main.py

# Switch to non-root user
USER demo

# Run the program
CMD ["python", "main.py"]
```

Now when we build the image and run a shell, we can see that the default user is `demo` instead of `root`:

```plaintext
docker run -it take_six:latest sh
/app $ whoami
demo
/app $ 
```

## Result Summary

| Image Description | Build Time | Size |
|-------------------|------------|------|
| Ubuntu Base Image | `115.1s` | `590MB` |
| `python:3.13-slim` Base Image | `30.9s` | `151MB` |
| `python:3.13-slim` Base Image + `uv` | `x.xs` | `xMB` |
| `python:3.13-slim` Base Image + `uv` + Multi-Stage Build | `x.xs` | `xMB` |
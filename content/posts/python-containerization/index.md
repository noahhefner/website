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
+++

In my day job, I’ve been spending a lot of time working with Docker containers that run Python applications. Along the way, I found myself digging deep into how to optimize these Docker images. In this article, I’ll walk through the steps I took to build what I think is a solid approach to containerizing Python applications.

What does it mean to optimize a Docker image? I see three main focus areas in containerization:

1. **Build Time**: How long it takes to build the container image. Longer build times make local development cumbersome and can slow down CI/CD pipelines.
2. **Image Size**: The total size of the built image. Large images can slow down deployments if servers frequently download them, while smaller images result in faster, more efficient deployments.
3. **Security Best Practices**: Containerization is not a crutch for poor security practices. Container security presents unique challenges and requires its own set of best practices.

This article will focus more heavily on the first two points, but I will include some security notes as well. We will start with an “unoptimized” image, then progressively enhance it by reducing the build time, reducing the image size, and improving the security of the image.

All code for this article is available in my GitHub website repository [here](https://github.com/noahhefner/website/tree/main/content/posts/python-containerization). If you're following along, all the commands in this article are run from the directory `content/posts/python-containerization` in that repository.

*Sidenote: For benchmarking / testing purposes, the Docker build cache was cleared in between builds for each of these images.*

## Example Project

To set the stage, lets assume we want to containerize a very basic Python program:

```python
# src/main.py

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

 This program does the following:

- Creates a `structlog` configuration and initializes a logger object
- Creates a connection to a MongoDB database
- Creates a connection to RabbitMQ
- Listens for a message from RabbitMQ
- Upon consuming a message, write the message and a timestamp to a MongoDB database

This program is a bit contrived, but the important part is that it makes use of several dependencies that will need to be resolved before run time.

- The `pika` package is used for interacting with a RabbitMQ server
- The `pymongo` package is used for writing to a MongoDB database
- The `structlog` package is used for structured logging in `JSON` format

Let's also assume our Python project makes use of some developer dependencies like code linters and formaters:

- `black` for code formatting
- `isort` for sorting import statements
- `autoflake` for removing unused imports

If we use `pip` to manage our packages, we might generate a `requirments.txt` file for the project, which would look like this:

```plaintext
# take_1/requirments.txt

pika==1.3.2
pymongo==4.14.1
structlog==25.4.0
black==25.1.0
isort==6.0.1
autoflake==2.3.1
```

## Take One - Containerization with Ubuntu

With the basics of our project established, let's consider how we might containerize this application. In our container, we will install a couple of tools:

- The Python interpreter
- `pip` for downloading the dependencies
- `venv` for creating a virtual environment for those dependencies

We will start with the following `Dockerfile`:

```dockerfile
# take_1/Dockerfile

# Start from Ubuntu
FROM ubuntu:24.04

# Install Python, pip, and venv
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

# Copy requirements.txt
COPY take_1/requirements.txt .

# Install Python modules
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]
```

In this Dockerfile, Ubuntu 24.04 is used as the base image. Next, we install the Python interpreter, `pip`, and `venv`. Then, we create a Python virtual environment using `venv`, add it to our path, and then install our Python dependencies from the `requirments.txt` file using `pip`. Finally, we copy over the `main.py` file and execute it.

To build our image, we can use the `docker build` command:

```sh
docker build -f take_1/Dockerfile -t take_one:latest .
```

We get the following output:

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

Notice from the first line of this output that the image took almost **two minutes** to build.

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

You can see by the `Size` field (measured in bytes) that the image is over **half a gigabyte**!

```json
"Size": 589982747
```

## Take Two - Choosing the right base image

Why was our first Docker image so large? Although the Ubuntu base image today is surprisingly compact—typically around 70MB—installing Python via `apt` also pulls in a lengthy list of dependencies, including build tools, libraries, and system utilities. This cascade of packages can cause the final image to balloon well past 500MB.

An easy way to avoid pulling in all those extra packages is to start from a slim, purpose-built base image. For this article, we’ll use `python:3.13-alpine3.22`, an Alpine-based image with the Python interpreter and other tooling preinstalled. Because it contains only the essentials, it’s much smaller than the Ubuntu + `apt` approach and should also speed up our build times.

Let's rebase our `Dockerfile` on `python:3.13-alpine3.22`:

```dockerfile
# take_2/Dockerfile

# Start from Python Alpine image
FROM python:3.13-alpine3.22

# Set work directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements.txt
COPY take_1/requirements.txt .

# Install Python modules
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

We can already see some huge improvements in our output. The build time has been reduced from 115 seconds to just 41 seconds. (I will omit the rest of the build logs from this point forward for brevity.)

```plaintext
[+] Building 40.9s (11/11) FINISHED
```

Additionally, we end up with a much smaller resulting image, just 76MB. (Also omitting irrelevant information from the `docker inspect` command from this point forward for brevity.)

```json
"Size": 76136781
```

From a security perspective, we're also reducing our attack surface. By stripping away unnecessary packages, we leave fewer potential vulnerabilities inside the container. This is one key advantage of using purpose-built base images such as `python:alpine` or `python:slim`—they are designed to be lightweight, fast to build, and easier to secure.

For small applications with minimal dependencies, this `Dockerfile` is already quite solid. For larger projects with many dependencies, however, there’s still room for improvement. In the next step, we’ll swap out `pip` for a faster dependency resolution tool to gain some additional speed.

## Take Three - Speeding Up Dependency Downloads

So far, we’ve used `pip` to install all the dependencies in our virtual environment. While `pip` gets the job done, it can be slow and inefficient. One effective way to speed up build times is to accelerate dependency installation.

Enter [`uv`](https://docs.astral.sh/uv/). `uv` is a modern Python project management utility developed by [Astral](https://astral.sh/) that consolidates and replaces tools like `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, `virtualenv`, and more. Astral claims that `uv` is "10-100x faster than `pip`." By swapping `pip` for `uv`, dependencies install much faster, and build times shrink significantly. (Even if you aren't containerizing your Python application, `uv` is, in my opinion, much more ergonomic from a developer experience perspective than traditional tools.)

To use `uv` in our Dockerfile, we can start from one of [Astral's Docker images](https://docs.astral.sh/uv/guides/integration/docker/#available-images). For this article, we'll use `ghcr.io/astral-sh/uv:python3.13-alpine`, which is essentially the `python:3.13-alpine` image with `uv` preinstalled.

Here's the updated `Dockerfile`:

```dockerfile
# take_3/Dockerfile

# Start from uv image
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml
COPY take_3/pyproject.toml .

# Install Python modules
RUN uv sync --no-cache

# Copy application code
COPY src/main.py main.py

# Ensure venv is used for all Python calls
ENV PATH="/app/.venv/bin:$PATH"

# Run the program
CMD ["python", "main.py"]
```

Notice that I have swapped the `requirements.txt` file for a `pyproject.toml` file. (This is the default for `uv` projects.) `pyproject.toml` is more flexible than a `requirements.txt` file. Along with other metadata about the project, it also contains a list of dependencies, similar to a `requirements.txt` file.

```toml
# take_3/pyproject.toml

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
docker build -f Dockerfile.take_3 take_three:latest .
```

Our build time is cut (almost) in half:

```
[+] Building 25.0s (11/11) FINISHED
```

The size of the image actually increases a fair bit, 105MB up from 76MB in the previous iteration, but we will revisit this in Take Five.

```json
"Size": 104666309
```

## Take Four - Removing Developer Dependencies

Our `pyproject.toml` file lists all project dependencies, including development-only tools like `black`, `isort`, and `autoflake`. If we include these in the build, they’ll end up in the final image and unnecessarily increase its size.

We can rework our `pyproject.toml` file to take advantage of [dependency groups](https://docs.astral.sh/uv/concepts/projects/sync/#syncing-development-dependencies) so that we can exclude those modules when we build the image for production. I won't cover how to set up dependency groups in this article, but here is what the updated `pyproject.toml` looks like:

```toml
# take_4/pyproject.toml

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

Notice how the development dependencies have been moved to a dependency group called `dev`. To exclude the `dev` dependency group modules from the final image, we can add `--no-group dev` to our `uv sync` command in the `Dockerfile`. This will instruct `uv` not to fetch the dependencies from the `dev` group.

```diff
# take_4/Dockerfile

- RUN uv sync --no-cache
+ RUN uv sync --no-cache --no-group dev
```

We can build the image with the following command:

```sh
docker build -f Dockerfile.take_4 take_four:latest .
```

We shave a few seconds off the build time:

```plaintext
[+] Building 22.8s (11/11) FINISHED
```

The image size is reduced by a few MB:

```json
"Size": 102344686
```

The amount of time and image size saved with this technique will vary from project to project, depending on the number of development dependencies used. In this example, the improvements were fairly minimal. However, by removing these modules from the image, we're continuing to shrink our attack surface, making our image more secure.

## Take Five - Removing Build Tools

In Take Three, we sped up the dependency resolution process by swapping `pip` for `uv`. While this did reduce the build time, it also **increased** the total image size. This is because the `uv` binary itself is ~40MB in size at the time of writing. Ironically, we can reduce the total image size by *removing* `uv` from the image. We only need `uv` to configure the virtual environment, so we can safely remove it from the final image.

We can accomplish this by splitting our Dockerfile into two stages. This strategy is commonly referred to as a [multi-stage build](https://docs.docker.com/build/building/multi-stage/).

```dockerfile
# take_5/Dockerfile

# -----------------------
# Stage 1: Build
# -----------------------
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml
COPY take_5/pyproject.toml .

# Install Python modules
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Run
# -----------------------
FROM python:3.13-alpine3.22 AS runner

# Set work directory
WORKDIR /app

# Copy venv from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/main.py main.py

# Ensure venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Run the program
CMD ["python", "main.py"]
```

The first stage of this Dockerfile is the "builder" stage. In this stage, we create the virtual environment and download our dependencies.

The second stage of the Dockerfile is the "runner" stage. Since we're starting this stage from `python:alpine`, we are excluding the `uv` binary from the first stage. The second stage simply copies over the virtual environment files that were created in the builder stage and execute the script.

We can build the image with the following command:

```sh
docker build -f take_5/Dockerfile -t take_five:latest .
```

Build time remains roughly the same:

```plaintext
[+] Building 18.8s (15/15) FINISHED
```

The overall image size, however, has been cut down to under 50MB:

```json
"Size": 49673398
```

Stripping `uv` from the final image provides yet another reduction in the container's attack surface. In my opinion, this step is even more important than removing development dependencies. If we use a little common sense, it seems like a good idea to remove a binary *designed to download artifacts from the internet* from the container. By keeping `uv` only in the builder stage, we reduce the number of tools available in production, making the container leaner and less susceptible to misuse or exploitation.

## Take Six - Running as a Non-Root User

By default, containers run as the `root` user. If we run a shell inside our Take Five image and check the current user, we can verify this behavior:

```plaintext
docker run -it take_five:latest sh
/app # whoami
root
/app #
```

Running as root inside a container is [discouraged](https://www.docker.com/blog/understanding-the-docker-user-instruction/). If the container is ever compromised, the attacker would immediately have elevated privileges within the container. A simple safeguard is to create a dedicated non-root user and run the application as that user instead.

We can update the `runner` stage of our Dockerfile to create a non-root user called `demo`. We will also add commands to give that user ownership and execution rights on the `main.py` file. Finally, the `USER` command will switch to the `demo` user before executing the script.

```dockerfile
# take_6/Dockerfile

# -----------------------
# Stage 1: Build
# -----------------------
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml
COPY take_6/pyproject.toml .

# Install Python modules
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Runtime
# -----------------------
FROM python:3.13-alpine3.22 AS runner

# Set work directory
WORKDIR /app

# Copy venv from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/main.py main.py

# Create a non-root user
RUN addgroup -S demo && adduser -S demo -G demo

# Give the non-root user permission to run the script
RUN chown demo:demo /app/main.py && \
    chmod u+rwx /app/main.py

# Ensure venv is used
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER demo

# Run the program
CMD ["python", "main.py"]
```

Now, when we build the image and open a shell, we can confirm that the container runs under the `demo` user instead of `root`:

```plaintext
docker run -it take_six:latest sh
/app $ whoami
demo
/app $ 
```

## Wrap Up

In this article, we explored several strategies for optimizing Docker images when running Python applications. By reducing image size and prioritizing faster build times, we created a compact and more secure container well-suited for Python codebases.

In summary:

- Prefer **lightweight, purpose-built base images** such as `python:alpine` to minimize size and exclude unnecessary libraries, binaries, and packages.
- Use **modern Python tooling** like `uv` to speed up dependency resolution and installation.
- **Exclude development dependencies** (e.g., formatters, linters) from the final image. Tools that support `pyproject.toml`, such as `uv` or `poetry`, make this easy by organizing dependencies into groups.
- Apply **multi-stage builds** to separate environment setup from runtime execution, keeping the final image clean and minimal.
- Run as a **non-root user** to reduce the risk of privilege escalation if the container is compromised.
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

{{< gh-blockquote type="note" >}}
Code for this post is in [my GitHub repo for this website](https://github.com/noahhefner/website/tree/main/content/posts/python-containerization).
{{< /gh-blockquote >}}

In my day job, I’ve been spending a lot of time working with Docker containers that run Python applications. Along the way, I found myself digging deep into how to optimize these Docker images. In this article, I’ll walk through the steps I took to build what I think is a solid approach to containerizing Python applications.

What does it mean to optimize a Docker image? I see three main focus areas in containerization:

1. **Build Time**: How long it takes to build the container image. Longer build times make local development cumbersome and can slow down CI/CD pipelines.
2. **Image Size**: The total size of the built image. Large images can slow down deployments if servers frequently download them, while smaller images result in faster, more efficient deployments.
3. **Security Best Practices**: Containerization is not a crutch for poor security practices. Container security presents unique challenges and requires its own set of best practices.

This article will focus more heavily on the first two points, but I will include some security notes as well. We will start with an “unoptimized” image, then progressively enhance it by reducing the build time, reducing the image size, and improving the security of the image.

All code for this article is available in my GitHub website repository [here](https://github.com/noahhefner/website/tree/main/content/posts/python-containerization). If you're following along, all the commands in this article are run from the directory `content/posts/python-containerization` in that repository.

{{< gh-blockquote type="note" >}}
For benchmarking / testing purposes, the Docker build cache was cleared in between builds for each of these images.
{{< /gh-blockquote >}}

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

- `ruff` for code formatting
- `ty` for code linting
- `isort` for sorting import statements

If we use `pip` to manage our packages, we might generate a `requirments.txt` file for the project, which would look like this:

```plaintext
# take_1/requirments.txt

pika==1.4.0
pymongo==4.17.0
structlog==25.5.0
ruff==0.15.13
ty==0.0.38
isort==8.0.1
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
FROM ubuntu:26.04

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

In this Dockerfile, Ubuntu 26.04 is used as the base image. Next, we install the Python interpreter, `pip`, and `venv`. Then, we create a Python virtual environment using `venv`, add it to our path, and then install our Python dependencies from the `requirments.txt` file using `pip`. Finally, we copy over the `main.py` file and execute it.

To build our image, we can use the `docker build` command:

```sh
docker build -f take_1/Dockerfile -t take_one:latest .
```

We get the following output:

```plaintext
[+] Building 141.7s (12/12) FINISHED                                                                                           docker:default
 => [internal] load build definition from Dockerfile                                                                                     0.1s
 => => transferring dockerfile: 631B                                                                                                     0.0s
 => [internal] load metadata for docker.io/library/ubuntu:26.04                                                                          0.6s
 => [internal] load .dockerignore                                                                                                        0.1s
 => => transferring context: 2B                                                                                                          0.0s
 => [internal] load build context                                                                                                        0.1s
 => => transferring context: 1.29kB                                                                                                      0.0s
 => [1/7] FROM docker.io/library/ubuntu:26.04@sha256:f3d28607ddd78734bb7f71f117f3c6706c666b8b76cbff7c9ff6e5718d46ff64                    8.2s
 => => resolve docker.io/library/ubuntu:26.04@sha256:f3d28607ddd78734bb7f71f117f3c6706c666b8b76cbff7c9ff6e5718d46ff64                    0.1s
 => => sha256:1c24335ddd46023ff99bd665bd8ea6798464f7bbf501718edcf2eb4696e5f408 387B / 387B                                               0.1s
 => => sha256:6f5c5aa4e145204b113f983c003ff8ad6489394294ef95ec030bc94e3daded54 41.55MB / 41.55MB                                         5.1s
 => => extracting sha256:6f5c5aa4e145204b113f983c003ff8ad6489394294ef95ec030bc94e3daded54                                                2.8s
 => => extracting sha256:1c24335ddd46023ff99bd665bd8ea6798464f7bbf501718edcf2eb4696e5f408                                                0.0s
 => [2/7] RUN apt-get update && apt-get install -y     python3     python3-pip     python3-venv                                         46.2s
 => [3/7] WORKDIR /app                                                                                                                   0.3s 
 => [4/7] RUN python3 -m venv /opt/venv                                                                                                  3.6s 
 => [5/7] COPY take_1/requirements.txt .                                                                                                 0.1s 
 => [6/7] RUN pip install --no-cache-dir -r requirements.txt                                                                             9.7s 
 => [7/7] COPY src/main.py main.py                                                                                                       0.1s 
 => exporting to image                                                                                                                  72.4s 
 => => exporting layers                                                                                                                 60.1s 
 => => exporting manifest sha256:34f26c1b95af49be50cfd74fabed4c42d695c6ec4d96f07b9b7d40f31a06f91b                                        0.0s 
 => => exporting config sha256:aa2bc3cfb8d6f29bbfb977c63d3c278cf3ff71e47067d0b6d4c5f6619c67e155                                          0.0s 
 => => exporting attestation manifest sha256:c009e1cac2f1fce82c1066a1495b502335ac43c7f5dc19ea4ea5a5beb9c54b0e                            0.0s 
 => => exporting manifest list sha256:9d4f32d0d7a9216d6115fb9cac183c1d776ad1c1b8a40228c58f3a47583a01c5                                   0.0s
 => => naming to docker.io/library/take_one:latest                                                                                       0.0s
 => => unpacking to docker.io/library/take_one:latest                                                                                   12.2s
```

Notice from the first line of this output that the image took over **two minutes** to build.

```plaintext
[+] Building 141.7s (12/12)
```

We can also check the size of the image using the `docker image inspect` command:

```json
[
    {
        "Id": "sha256:9d4f32d0d7a9216d6115fb9cac183c1d776ad1c1b8a40228c58f3a47583a01c5",
        "RepoTags": [
            "take_one:latest"
        ],
        "RepoDigests": [
            "take_one@sha256:9d4f32d0d7a9216d6115fb9cac183c1d776ad1c1b8a40228c58f3a47583a01c5"
        ],
        "Comment": "buildkit.dockerfile.v0",
        "Created": "2026-05-20T09:17:07.745571237-04:00",
        "Config": {
            "Env": [
                "PATH=/opt/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
            ],
            "Cmd": [
                "python",
                "main.py"
            ],
            "WorkingDir": "/app",
            "Labels": {
                "org.opencontainers.image.created": "2026-04-21T17:23:54.324551+00:00",
                "org.opencontainers.image.description": "The Ubuntu container image maintained by Canonical\n\nUbuntu is a Debian-based Linux operating system that runs from the desktop to the cloud, to all your internet connected things.\nIt is the world's most popular operating system across public clouds and OpenStack clouds.\nIt is the number one platform for containers; from Docker to Kubernetes to LXD, Ubuntu can run your containers at scale.\nFast, secure and simple, Ubuntu powers millions of PCs worldwide.\n",
                "org.opencontainers.image.title": "ubuntu",
                "org.opencontainers.image.version": "26.04"
            },
            "ArgsEscaped": true
        },
        "Architecture": "amd64",
        "Os": "linux",
        "Size": 255391136,
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:0c3db79307ab91dad11fad2b136a2b56df6efeeb567c4c99e6e316b63885c9f6",
                "sha256:f421a7e99ead34566fcb11403f6f38675b53035f39937394893eaf7d87c39f83",
                "sha256:0bb90bf7a165faac4a652ad9d2431cdc40f34a152c5e63910d1eda70468b8f32",
                "sha256:367934895ccb5d8cc185db06f38e5df9dc173f6b6bb40d28132cdfdf9b483415",
                "sha256:3cf0c8d9c35695f3e113b7e0f854141a558b9a64531a8b7d527382b1de0a9954",
                "sha256:8bbce59f22be1fdc7e75e4c42b848caf443582e2ed6a971e2143fe6c210def68",
                "sha256:4270b2eec59c5b05c0d8557c6140ca74f3c08eee0311cf3c6ebe43bbb08f78e1",
                "sha256:07c33e3e3c5157f1cde4188559dc1ffcc2cd9fe360d718758da74f0f79546232"
            ]
        },
        "Metadata": {
            "LastTagTime": "2026-05-20T13:18:08.006329621Z"
        },
        "Descriptor": {
            "mediaType": "application/vnd.oci.image.index.v1+json",
            "digest": "sha256:9d4f32d0d7a9216d6115fb9cac183c1d776ad1c1b8a40228c58f3a47583a01c5",
            "size": 856
        },
        "Identity": {
            "Build": [
                {
                    "Ref": "y6t48sja6h8rdcn3ilw9k0c3t",
                    "CreatedAt": "2026-05-20T09:18:20.176151158-04:00"
                }
            ]
        }
    }
]
```

You can see by the `Size` field (measured in bytes) that the image is over **quarter of a gigabyte**!

```json
"Size": 255391136,
```

## Take Two - Choosing the right base image

Why was our first Docker image so large? Although the Ubuntu base image today is surprisingly compact—typically around 70MB—installing Python via `apt` also pulls in a lengthy list of dependencies, including build tools, libraries, and system utilities. This cascade of packages can cause the final image to balloon well past 200MB.

An easy way to avoid pulling in all those extra packages is to start from a slim, purpose-built base image. For this article, we’ll use `python:3.14-alpine3.23`, an Alpine-based image with the Python interpreter and other tooling preinstalled. Because it contains only the essentials, it’s much smaller than the Ubuntu + `apt` approach and should also speed up our build times.

Let's rebase our `Dockerfile` on `python:3.14-alpine3.23`:

```dockerfile
# take_2/Dockerfile

# Start from Python Alpine image
FROM python:3.14-alpine3.23

# Set work directory
WORKDIR /app

# Create virtual environment
RUN python -m venv /opt/venv

# Ensure venv is used for all Python/Pip calls
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements.txt
COPY take_2/requirements.txt .

# Install Python modules
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/main.py main.py

# Run the program
CMD ["python", "main.py"]
```

We can build the image with the following command:

```sh
docker build -f take_2/Dockerfile -t take_two:latest .
```

We can already see some huge improvements in our output. The build time has been reduced from 141 seconds to 73 seconds. (I will omit the rest of the build logs from this point forward for brevity.)

```plaintext
[+] Building 73.9s (11/11)
```

Additionally, we end up with a much smaller resulting image, just 52MB. (Also omitting irrelevant information from the `docker inspect` command from this point forward for brevity.)

```json
"Size": 51921311,
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
FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml and uv.lock
COPY take_3/pyproject.toml take_3/uv.lock .

# Install Python modules
RUN uv sync --no-cache

# Copy application code
COPY src/main.py main.py

# Ensure venv is used for all Python calls
ENV PATH="/app/.venv/bin:$PATH"

# Run the program
CMD ["python", "main.py"]
```

Notice that the `requirements.txt` file has been replaced by `pyproject.toml` and `uv.lock`. `pyproject.toml` is more flexible than a `requirements.txt` file. Along with other metadata about the project, it contains a list of dependencies, just like `requirements.txt`. 

The `uv.lock` file works similar to a `package-lock.json` file for JavaScript project. It tracks exact package versions for the entire dependency tree, ensuring the runtime environment is exactly the same across all deployments.

```toml
# take_3/pyproject.toml

[project]
name = "python-container-article"
version = "0.1.0"
description = "Example pyproject.toml file"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "isort>=6.0.1",
    "pika>=1.3.2",
    "pymongo>=4.14.1",
    "ruff>=0.15.13",
    "structlog>=25.4.0",
    "ty>=0.0.38",
]
```

We can build the image with the following command:

```sh
docker build -f take_3/Dockerfile -t take_three:latest .
```

Our build time is cut in half:

```
[+] Building 30.5s (11/11) FINISHED
```

The size of the image actually increases a bit, 68MB up from 52MB in the previous iteration, but we will revisit this in Take Five.

```json
"Size": 68599042,
```

## Take Four - Removing Developer Dependencies

Our `pyproject.toml` file lists all project dependencies, including development-only tools like `ty`, `ruff`, and `isort`. If we include these in the build, they’ll end up in the final image and unnecessarily increase its size.

We can rework our `pyproject.toml` file to take advantage of [dependency groups](https://docs.astral.sh/uv/concepts/projects/sync/#syncing-development-dependencies) so that we can exclude those modules when we build the image for production. I won't cover how to set up dependency groups in this article, but here is what the updated `pyproject.toml` looks like:

```toml
# take_4/pyproject.toml

[project]
name = "python-container-article"
version = "0.1.0"
description = "Example pyproject.toml file"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "pika>=1.3.2",
    "pymongo>=4.14.1",
    "structlog>=25.4.0",
]

[dependency-groups]
dev = [
    "isort>=8.0.1",
    "ruff>=0.15.13",
    "ty>=0.0.38",
]
```

Notice how the development dependencies have been moved to a dependency group called `dev`. We can now update our Dockerfile to exclude the `dev` dependency group modules from the final image. To do this, we can add `--no-group dev` to our `uv sync` command. This will instruct `uv` not to fetch the dependencies from the `dev` group when constructing the virtual environment.

```diff
# take_4/Dockerfile

- RUN uv sync --no-cache
+ RUN uv sync --no-cache --no-group dev
```

We can build the image with the following command:

```sh
docker build -f take_4/Dockerfile -t take_four:latest .
```

We shave a few seconds off the build time:

```plaintext
[+] Building 19.1s (11/11) FINISHED
```

The image size is reduced by a few MB:

```json
"Size": 45249862,
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
FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml and uv.lock
COPY take_5/pyproject.toml take_5/uv.lock .

# Install Python modules
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Run
# -----------------------
FROM python:3.14-alpine3.23 AS runner

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

The first stage of this Dockerfile is the "builder" stage. In this stage, we create the virtual environment and download our dependencies with `uv`.

The second stage of the Dockerfile is the "runner" stage. Since we're starting this stage from `python:alpine`, we are excluding the `uv` binary from the first stage. The second stage simply copies over the virtual environment files that were created in the builder stage and execute the script.

{{< gh-blockquote type="note" >}}
When using multi-stage builds for Python containers, ensure that both base images use the same system libraries. For example, if you build a virtual environment using an image based on glibc (such as Ubuntu) and then try to run it on an image based on musl (such as Alpine), you will likely encounter runtime issues.
{{< /gh-blockquote >}}

We can build the image with the following command:

```sh
docker build -f take_5/Dockerfile -t take_five:latest .
```

Build time remains roughly the same:

```plaintext
[+] Building 18.8s (15/15) FINISHED
```

The overall image size, however, has been cut down to just 18MB:

```json
"Size": 18823226,
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
FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

# Set work directory
WORKDIR /app

# Create virtual environment
RUN uv venv

# Copy pyproject.toml and uv.lock
COPY take_6/pyproject.toml take_6/uv.lock .

# Install Python modules
RUN uv sync --no-cache --no-group dev

# -----------------------
# Stage 2: Runtime
# -----------------------
FROM python:3.14-alpine3.23 AS runner

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

## Changelog

- **20 May 2026**: Fixed typos in Docker build commands, updated package versions, use different dev dependencies, add uv lock file to build commands.

---
title: "Building an AI Tool Without AI"
date: "2026-08-26T07:28:36-04:00"
cover: ""
tags: ["python", "ai", "terminal", "software design"]
description: ""
draft: true
---

## Problem Statement

I manage the servers in my homelab exclusively through the command line. Whether I'm managing Docker containers, performing routine system updates, or organizing files (like movies for Jellyfin), it's almost always over SSH with Bash.

As a developer, I'm no stranger to the command line. I open a terminal every single day for one reason or another. But with the shear number of CLI programs I work with, I can't remember every flag and every argument for every tool. There are of course the `man` pages for researching how to use a tool. Or for a faster, "this is probably what you're looking for" utility, there is `tldr`, which gives you an overview of the program you're interrested in along with multiple examples of common use cases. 

But while I am [cosplaying as a sysadmin](https://www.jeffgeerling.com/blog/2022/cosplaying-sysadmin/) with my homelab, I am frequently in need of a bespoke, weird command to do something very specific on the system. In these instances, I usually need to flip over to my browser and Google "how do I XYZ", or in current year, ask an AI.

For example, I recently needed to stop all my running Docker containers, except one. A quick prompt to Chat Gippity and I got back the following command that does just that:

```bash
docker stop $(docker ps -q --filter "name!=my-app")
```

A hyper-specific, irregular command like that is not going to show up in any man pages. 

This experience gave me an idea. What if I had a utility right in my terminal where I could quickly ask AI for assistance with a terminal-based task? A tool similar to `tldr`, but turbocharged with the power of AI.

## Learning Opportunities

I'm sure there are a ton of projects out there already that do exactly what I need. But I decided to intentionally not do any research on existing tools so that I could take this opportunity to build my own and learn some new skills along the way. (The finished product is never really the objective of side projects anyway. 🙂)

For this project, I (ironically) wanted to use as little AI assistance for coding the tool as possible. As AI takes on more coding responsibilities, the opportunities for engineers to exercise our software design muscles are only shrinking. With a few exceptions, this project should be built entirely by hand.

## Project Requirements

I started by creating a list of hard requirements that the tool had to meet.

1. **Run in Headless Environments**: This tool is going to run on my server, so it needs to work with no graphical dependencies.
2. **Cross-Platform**: The tool should run on Linux, Windows, and MacOS.
3. **Easy to Install**: Even though this is a personal project, I want the deployment process to be painless and easy. I have several systems this tool will be installed on.
4. **OS and Shell Aware**: The tool needs to understand the environment in which it's running. I don't want it to suggest a Powershell command if I'm invoking it from a Debian server.

## Technical Design

With my requirements set, the next phase of the project is the technical design. This involves defining exactly how I want the UX to work, selecting the language, researching which libraries to use, and thinking through the architecture of the system.

### Language Choice

I chose to build this tool in Python because Python is my favorite language and I don't care to add "learn a whole new language ecosystem" to the list of objectives for this project. (One day, Rust.) Since Python runs everywhere, it meets my cross-platform requirement. I can also publish the Python package to PyPI so that it can be easily installed from any machine with `pip` or `uv`.

### Usage Examples

Before writing any code, I wrote out some examples of how I wanted the tool to work. I wanted it to be extremely simple. I put in a request, hit enter, and get back some commands I can work with. I wanted to be able to select a command and have it automatically populate the command line after I hit enter. That way the user can hit enter again to execute the selected command:

```bash
$ how "list all files over 10mb"   <- Ask question

Thinking...   <- Generate responses from LLM

Select a command:
  * find / -type f -size +10M 2>/dev/null   <- Hit enter to select this command
    find / -type f -size +10M -exec ls -lh {} + 2>/dev/null
    find / -type f -size +10M -printf '%s %p\n' 2>/dev/null | sort -n
    Cancel

$ find / -type f -size +10M 2>/dev/null   <- Auto populated next line in the terminal
```

To make the UI look nice, I found [rich](https://github.com/textualize/rich), a Python library for rich text and formatting in the terminal. I also made use of [questionary](https://github.com/tmbo/questionary) for user prompts.

### Multiple Model Support

I wanted this tool to support multiple LLM providers. To start, I wanted the tool to support Gemini and Groq, simply because both of these providers have a free tier. They also both have solid Python libraries with [python-genai](https://github.com/googleapis/python-genai) and [groq-python](https://github.com/groq/groq-python).

From a software design perspective, this was the perfect use case for an abstract class. An LLM provider abstract class provides a single, uniform interface for interacting with Gemini, Groq, and any providers that I add in the future. Each provider can subclass `LLMProvider` and implement its provider-specific logic in the abstract methods.

```python
from abc import ABC, abstractmethod

from how_tui.models.command import CommandResponse


class LLMProvider(ABC):
    @staticmethod
    @abstractmethod
    def generate_commands(
        prompt: str,
        model: str,
    ) -> CommandResponse: ...

    @staticmethod
    @abstractmethod
    def authenticate(force: bool = False) -> None: ...

    @staticmethod
    @abstractmethod
    def unauthenticate() -> None: ...

    @staticmethod
    @abstractmethod
    def get_models() -> list[str]: ...
```

Now, this use case for an abstract class was extremely obvious. A CS101 student in high school would be able to implement this. But what this trivial example revealed to me is how AI has flipped the software development process upside down. **Instead of writing code to meet the project requirements, engineers are now working in the opposite direction: the code is generated near instantly and the role of the engineer is to verify that it meets the project requirements.**

Personally, I found the process of writing code manually quite refreshing. Not only did I understand the code better because I wrote it, but I understood the project requirements better too. When you write code yourself, you identify problems and edge cases organically. This inherently leads to a deeper understanding of the code base and better positions the engineer for fixing bugs in the future.

### Configuration File

To keep track of the user's preferred LLM provider and model, I wanted to implement a configuration file system. The configuration file should store information like the user's LLM provider (Gemini, Groq) and their preferred model from that provider.

Keeping with my cross-platform requirement, I found a really cool package called [platformdirs](https://github.com/tox-dev/platformdirs) which offers an OS-agnostic interface for accessing commonly used directories on the host system. For this project, I can leverage it to locate a directory where I can store the configuration file on any platform.

For example:

```python
from platformdirs import PlatformDirs

dirs = PlatformDirs("MyApp", "MyCompany")
config_dir = dirs.user_config_dir  
# config_dir = ~/Library/Application Support/MyApp (MacOS)
# config_dir = ~/.config/MyApp (Linux)
# config_dir = C:\Users\<username>\AppData\Local\MyCompany\MyApp (Windows)
```

### Securely Storing Authentication Credentials

Finally, I needed a way to securely store authentication credentials on the user's machine in order to interact with the LLM APIs. I could have just informed the user to set environment variables on their machine, but I wanted a better UX than that.

I found a library called [keyring](https://github.com/jaraco/keyring) which provides an interface for securely storing sensitive passwords (or in our case, API keys) on the host. Like the other libraries, it is OS-agnostic. Keyring supports the following storage backends:

- macOS [Keychain](https://en.wikipedia.org/wiki/Keychain_%28software%29)
- Freedesktop [Secret Service](http://standards.freedesktop.org/secret-service/) supports many DE including
  GNOME (requires [secretstorage](https://pypi.python.org/pypi/secretstorage))
- KDE4 & KDE5 [KWallet](https://en.wikipedia.org/wiki/KWallet)
  (requires [dbus](https://pypi.python.org/pypi/dbus-python))
- [Windows Credential Locker](https://docs.microsoft.com/en-us/windows/uwp/security/credential-locker)

Usage is very straightforward:

```python
>>> import keyring
>>> keyring.set_password("system", "username", "password")
>>> keyring.get_password("system", "username")
'password'
```

---

[WORK IN PROGRESS FROM HERE DOWN]

That last requirement of auto populating the selected command onto the next line in the terminal proved to be quite the challenge. From my research, it seems that there is simply not a way to inject text onto the input buffer for the next command, at least not with bash. I explored options like writing the selected command to a temporary file and wrapping the Python script in a bash script to capture the output, but I couldn't find a satisfactory solution. (If you know how to do this, please open an issue in the GitHub repository for this project. I would love to have this feature working.) However, even if I could get it working, this would almost certainly need bespoke implementations for every shell, which would add another level of complexity.

To avoid getting sidetracked and pouring tons of hours into such a small piece of the puzzle, I decided to omit that part of the tool and simply print the commands to the terminal after getting them back from the LLM:

```bash
$ how "list all files over 10mb"

Thinking...   <- Generate responses from LLM

Suggested commands:
  - find / -type f -size +10M 2>/dev/null
  - find / -type f -size +10M -exec ls -lh {} + 2>/dev/null
  - find / -type f -size +10M -printf '%s %p\n' 2>/dev/null | sort -n

$
```
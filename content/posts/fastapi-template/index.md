---
title: "Our FastAPI Project Template"
date: "2026-05-11T09:41:30-04:00"
cover: "fastapi-logo.png"
---

{{< gh-blockquote type="note" >}}
The template repository can be found on GitHub [here](https://github.com/noahhefner/fastapi-template).
{{< /gh-blockquote >}}

FastAPI is a fantastic tool for building REST APIs in Python. However, many tutorials, guides, and project templates set developers up for failure as their APIs grow in scope and complexity. A quick search for “FastAPI project templates” reveals a recurring pattern:

```plaintext
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── internal/
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── db/
│       ├── __init__.py
│       ├── database.py
│       └── migrations/
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_users.py
│   ├── test_items.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── run.sh
```

While this setup is fine for smaller projects, our team has found that the developer ergonomics suffer as the API expands. This is primarily because developers are forced to jump between multiple directory trees to work on related logic.

We found that organizing code by **domain** instead of **function** results in a much more scalable and flexible codebase. Every endpoint is organized under a domain folder, and all code for a given endpoint is encapsulated within its own directory.

In this configuration, code is colocated, meaning you no longer need to jump between `services/`, `routers/`, `models/`, and `schemas/` directories when working on a single endpoint.

```plaintext
├── domains
│   ├── __init__.py
│   ├── items
│   │   ├── get_all_items
│   │   │   ├── __init__.py
│   │   │   └── test_get_all_items.py
│   │   ├── get_item_by_id
│   │   │   ├── __init__.py
│   │   │   └── test_get_item_by_id.py
│   │   └── __init__.py
│   └── orders
│       ├── get_all_orders
│       │   ├── __init__.py
│       │   └── test_get_all_orders.py
│       ├── get_order_by_id
│       │   ├── __init__.py
│       │   ├── errors.py
│       │   ├── get_order_by_id.py
│       │   ├── models.py
│       │   └── test_get_order_by_id.py
│       └── __init__.py
```

Since each endpoint is isolated in its own folder, they are free to scale independently of one another. Simple endpoints might execute a short SQL query and return a response (e.g., items endpoints) in a single file. More complex endpoints—involving dynamic query building, third-party APIs, or sophisticated authorization—can be broken down into separate files for models, business logic, and errors, all while staying within that same endpoint directory (e.g., get_order_by_id).

I created a [template repository](https://github.com/noahhefner/fastapi-template) to capture and share the methods that have worked for our team. If you are building a quick proof-of-concept or a single-domain API, this structure may be overkill. However, if your API has many domains, is expected to scale, or you simply prefer that related code stay grouped together, this structure is, in my opinion, an excellent starting point.
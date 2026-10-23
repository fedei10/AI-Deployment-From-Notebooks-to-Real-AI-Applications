# AI-deployement
# FastAPI for AI Engineers

**From machine learning notebooks to real-world APIs**  
*A beginner-friendly, hands-on guide to building Python backends for AI applications.*

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Why FastAPI for AI Applications?](#2-why-fastapi-for-ai-applications)
- [3. Getting Started](#3-getting-started)
  - [Virtual Environments](#31-virtual-environments)
  - [Project Structure](#32-project-structure)
  - [Installation](#33-installation)
- [4. Your First FastAPI Application](#4-your-first-fastapi-application)
  - [Hello World](#41-hello-world)
  - [Run the Server](#42-run-the-server)
  - [API Documentation and OpenAPI](#43-api-documentation-and-openapi)
  - [Understanding the Code](#44-understanding-the-code)
- [5. Path and Query Parameters](#5-path-and-query-parameters)
  - [Path Parameters](#51-path-parameters)
  - [Query Parameters](#52-query-parameters)
  - [Required vs. Optional Parameters](#53-required-vs-optional-parameters)
  - [Automatic Type Conversion](#54-automatic-type-conversion-and-validation)
  - [Validation with Path and Query](#55-custom-validation-with-path-and-query)
  - [Pagination](#56-pagination-with-skip-and-limit)
  - [Route Ordering](#57-route-ordering)
- [6. Introduction to Pydantic](#6-introduction-to-pydantic)

---

## 1. Introduction

Hey there! I'm an AI engineer, and believe me, I've been lost before—just like you might be right now.

When I started learning AI, I spent most of my time in **Jupyter Notebook** and **Google Colab**. I learned how to train models, process data, fine-tune them, and build machine learning projects. But when I landed my first job, I started asking myself:

> **What's the next step? How do I turn my AI models into real applications that people can actually use?**

Things got complicated. Moving from notebooks to local development and then to cloud deployment isn't as easy as it sounds. Suddenly, you need to understand how to **structure projects, build APIs, manage databases, validate data, and connect everything together**.

I know AI tools can generate code quickly, but understanding what's happening under the hood is crucial for debugging and becoming a stronger software or AI engineer—not just another *vibe coder*.

**So let's get started.**

---

## 2. Why FastAPI for AI Applications?

### What is FastAPI?

[FastAPI](https://fastapi.tiangolo.com/) is a modern, high-performance Python web framework for building APIs. It is built on:

- **Starlette:** The web framework foundation, including routing, requests, and ASGI support.
- **Pydantic:** Data parsing, validation, and serialization using Python type annotations.

### Why choose FastAPI for an AI backend?

#### 1. Native async support for I/O-heavy workloads

AI services often spend time **waiting** for an external LLM API, a vector database, or a network request. FastAPI supports Python's `async` / `await` syntax, allowing the server to handle other work while compatible asynchronous I/O is in progress.

> **Important:** `async` does not automatically make CPU-heavy model inference faster. Blocking or CPU-intensive tasks may need separate workers, threads, processes, or dedicated inference services.

#### 2. Data validation with Pydantic

AI applications require predictable inputs: JSON structures, text fields, numerical features, and more. By declaring types and validation rules, FastAPI can reject malformed requests **before your endpoint function runs**.

For example, you can require a numerical feature to be nonnegative, or a text field to have a minimum length. Specialized constraints—such as a tensor's shape—still need explicit validation logic.

#### 3. Integration with the Python ecosystem

Most AI/ML tools already use Python, including PyTorch, TensorFlow, scikit-learn, Hugging Face Transformers, and LangChain. This makes it practical to expose Python-based models and workflows through HTTP APIs.

---

## 3. Getting Started

This chapter covers the initial setup and a project layout that can grow with your application.

### 3.1 Virtual Environments

Before installing dependencies, it's a good practice to create a **virtual environment**. A virtual environment isolates project dependencies so that different applications can use different package versions.

#### Why use a virtual environment?

Imagine two projects:

| Project | Dependency | Reason |
| :-- | :-- | :-- |
| **Project A** | `django==3.2` | Legacy application |
| **Project B** | `django==5.0` | Newer application |

If you install both versions into the same Python environment, one installation can replace the other. A separate virtual environment for each project avoids that conflict.

#### Step 1 — Open the project directory

```bash
mkdir my-fastapi-project
cd my-fastapi-project
```

#### Step 2 — Create a virtual environment

**Linux / Ubuntu:**

```bash
python3 -m venv .venv
```

**Windows (PowerShell or Command Prompt):**

```powershell
py -m venv .venv
```

> **Ubuntu tip:** If the `venv` module is unavailable, install the appropriate package, such as `python3-venv`.

#### Step 3 — Activate the virtual environment

**Linux / macOS (Bash or Zsh):**

```bash
source .venv/bin/activate
```

**Windows — Command Prompt:**

```bat
.venv\Scripts\activate.bat
```

**Windows — PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

After activation, your terminal usually shows `(.venv)` at the beginning of the prompt.

**Useful commands:**

| Command | Purpose |
| :-- | :-- |
| `python -m pip list` | List installed packages |
| `python -m pip freeze` | Show installed package versions |
| `deactivate` | Leave the virtual environment |

### 3.2 Project Structure

There is no single perfect folder structure. Choose one that fits the size of your application. The main idea is to separate **routes**, **business logic**, **data models**, and **configuration**.

#### Option A — Layered structure (good for smaller and medium apps)

```text
.
├── pyproject.toml            # Project configuration and dependencies
├── alembic.ini               # Database migrations configuration
└── app/
    ├── __init__.py
    ├── main.py                # FastAPI application entry point
    ├── core/
    │   ├── config.py         # Application settings
    │   ├── security.py       # Authentication-related utilities
    │   └── db.py             # Database engine and sessions
    ├── api/
    │   ├── deps.py           # Shared dependencies
    │   └── v1/
    │       ├── api.py        # Combine versioned routers
    │       └── endpoints/
    │           ├── users.py
    │           └── items.py
    ├── models/                # Database models
    │   ├── user.py
    │   └── item.py
    ├── schemas/               # Request/response schemas
    │   ├── user.py
    │   └── item.py
    ├── crud/                  # Data-access operations
    │   ├── crud_user.py
    │   └── crud_item.py
    └── tests/                 # Automated tests
```

**What do the main folders do?**

| File or folder | Responsibility |
| :-- | :-- |
| `app/main.py` | Create the FastAPI instance and register routers |
| `app/api/` | Define HTTP endpoints |
| `app/core/` | Shared settings, security, and database configuration |
| `app/models/` | Define database tables/entities |
| `app/schemas/` | Validate request data and describe response data |
| `app/crud/` | Organize database operations |
| `app/tests/` | Test endpoints and application behavior |

#### Option B — Feature-based structure (useful as apps grow)

```text
app/
├── main.py
├── core/
└── modules/
    ├── users/
    │   ├── __init__.py
    │   ├── router.py          # User endpoints
    │   ├── models.py          # User database models
    │   ├── schemas.py         # User validation schemas
    │   └── service.py         # User business logic
    └── items/
        ├── router.py
        ├── models.py
        ├── schemas.py
        └── service.py
```

In a feature-based structure, everything related to a particular resource lives together. We will explore these architectures later; for now, a single `main.py` file is enough.

**References:** [Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/), [Full Stack FastAPI Template](https://fastapi.tiangolo.com/project-generation/), [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices).

### 3.3 Installation

With your virtual environment active, install FastAPI and Uvicorn:

```bash
python -m pip install fastapi uvicorn
```

- `fastapi` — The API framework.
- `uvicorn` — An ASGI server that runs your application.

You can also install FastAPI with its commonly used standard dependencies:

```bash
python -m pip install "fastapi[standard]"
```

Open the folder in VS Code:

```bash
code .
```

---

## 4. Your First FastAPI Application

### 4.1 Hello World

Create a file named **`main.py`**:

```python
# main.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}
```

### 4.2 Run the Server

Run this command from the folder containing `main.py`:

```bash
uvicorn main:app --reload
```

| Part | Meaning |
| :-- | :-- |
| `uvicorn` | Starts the ASGI server |
| `main` | Imports the module `main.py` |
| `app` | Uses the `app = FastAPI()` object |
| `--reload` | Reloads on code changes **during development** |

> **Note:** `--reload` is a development option, not a production deployment setting.

**Screenshot — server startup (original Obsidian reference):**

![[Pasted image 20261020122458.png]]

#### Check the API

Open <http://127.0.0.1:8000/> in your browser. You should see:

```json
{
  "message": "Hello, World!"
}
```

**Screenshot — JSON response:**

![[Pasted image 20261020122631.png]]

### 4.3 API Documentation and OpenAPI

FastAPI generates an OpenAPI schema and interactive documentation for your endpoints.

| URL | Purpose |
| :-- | :-- |
| <http://127.0.0.1:8000/docs> | Interactive Swagger UI documentation |
| <http://127.0.0.1:8000/redoc> | Alternative ReDoc documentation |
| <http://127.0.0.1:8000/openapi.json> | Machine-readable OpenAPI specification |

**Swagger UI:**

![[Pasted image 20261020122612.png]]

**ReDoc:**

![[Pasted image 20261020122645.png]]

#### What is a schema?

A **schema** describes the structure of something, rather than implementing the actual behavior.

- **API schema:** Describes available endpoints, HTTP methods, parameters, and responses.
- **Data schema:** Describes fields, data types, and constraints for data objects.

FastAPI uses the **OpenAPI** standard to describe APIs. That schema powers its documentation and can also be used by API development tools.

### 4.4 Understanding the Code

Let's break down the Hello World example line by line.

**Original overview screenshot:**

![[Pasted image 20261020122959.png]]

#### Step 1 — Import FastAPI

```python
from fastapi import FastAPI
```

`FastAPI` is the Python class we use to create our application.

![[Pasted image 20261020123038.png]]

#### Step 2 — Create the application instance

```python
app = FastAPI()
```

`app` is an instance of `FastAPI`. We register our routes on this object.

![[Pasted image 20261020123110.png]]

#### Step 3 — Define a path operation

```python
@app.get("/")
```

Two concepts matter here:

- **Path:** The URL path, such as `/`, `/items`, or `/users/42`.
- **Operation:** The HTTP method used with that path, such as `GET` or `POST`.

For the URL `https://example.com/items/foo`, the path is `/items/foo`.

![[Pasted image 20261020123212.png]]

**Common HTTP methods:**

| HTTP method | Typical use | FastAPI decorator |
| :-- | :-- | :-- |
| `GET` | Read data | `@app.get()` |
| `POST` | Create data or submit an operation | `@app.post()` |
| `PUT` | Replace an existing resource | `@app.put()` |
| `PATCH` | Partially update a resource | `@app.patch()` |
| `DELETE` | Delete a resource | `@app.delete()` |

Other HTTP methods include `HEAD`, `OPTIONS`, and `TRACE`, although you will use them less frequently when first learning FastAPI.

#### Step 4 — Define the endpoint function

```python
async def read_root():
    return {"message": "Hello, World!"}
```

FastAPI calls this function when a client sends a matching `GET /` request.

- `async def` defines an asynchronous function.
- You can also use a normal `def` function for suitable synchronous endpoints.
- Choose based on what the endpoint actually does; [FastAPI's async guide](https://fastapi.tiangolo.com/async/) explains the distinction.

![[Pasted image 20261020123343.png]]

#### Step 5 — Return the response

```python
return {"message": "Hello, World!"}
```

FastAPI converts supported Python return values—such as dictionaries, lists, and strings—into appropriate HTTP responses. A dictionary like this normally becomes a JSON response.

You can also return Pydantic models; we'll cover those later.

![[Pasted image 20261020123606.png]]

#### Quick recap

1. Import `FastAPI`.
2. Create an application instance with `app = FastAPI()`.
3. Register a route with a decorator such as `@app.get("/")`.
4. Define the function that handles the request.
5. Return a response and run the development server.

---

## 5. Path and Query Parameters

Remember this decorator?

```python
@app.get("/")
```

Until now, the URL has been fixed. But what if a client needs to request a specific product or filter a list of results? That's where **path parameters** and **query parameters** come in.

### 5.1 Path Parameters

A **path parameter** is a dynamic value inside a URL path. It often identifies a **specific resource**.

FastAPI declares a path parameter using curly braces: `{parameter_name}`.

```python
# Add these routes to your existing main.py
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str):
    return {"user_id": user_id, "item_id": item_id}
```

#### Example request

```http
GET /items/10
```

| Code or URL part | Meaning |
| :-- | :-- |
| `@app.get(...)` | Registers a GET route |
| `/items/` | The fixed part of the URL |
| `{item_id}` | The dynamic part of the URL |
| `item_id: int` | Requests an integer value |
| `10` | The value supplied by the client |

**Why use path parameters?** Without them, we would need a separate hard-coded route for every item. One dynamic route can work with many IDs.

#### Path parameters and CRUD operations

| HTTP method | URL | Typical purpose |
| :-- | :-- | :-- |
| `GET` | `/products/5` | Retrieve product 5 |
| `PUT` | `/products/5` | Replace product 5 |
| `PATCH` | `/products/5` | Partially update product 5 |
| `DELETE` | `/products/5` | Delete product 5 |
| `GET` | `/products` | List products |
| `POST` | `/products` | Create a product |

The URL identifies the resource; the HTTP method indicates what we want to do with it.

### 5.2 Query Parameters

**Query parameters** are `key=value` pairs placed after the `?` in the URL. You can use them to **filter**, **search**, **sort**, or **paginate** results.

For example:

```http
GET /items/?skip=0&limit=10
```

| URL part | Purpose |
| :-- | :-- |
| `/items/` | The endpoint path |
| `?` | Begins the query string |
| `skip=0` | Skip zero records |
| `&` | Separates parameters |
| `limit=10` | Request at most ten records |

Here is the FastAPI code:

```python
# main.py (continued — use the same app instance)
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


@app.get("/search/")
async def search_items(q: str | None = None):
    if q:
        return {"query": q}
    return {"message": "No query provided"}
```

#### Understanding these function parameters

| Parameter | Type | Default | Explanation |
| :-- | :-- | :-- | :-- |
| `skip` | `int` | `0` | Number of results to skip |
| `limit` | `int` | `10` | Maximum number of results requested |
| `q` | `str \| None` | `None` | Optional search query |

For now, these handlers **echo the supplied values**. They do not yet query a real database or implement search or pagination.

### 5.3 Required vs. Optional Parameters

Not every API request needs every possible value. Some parameters must be supplied, while others can use a default.

#### A. Required path parameter

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}
```

```http
GET /items/5
```

The URL needs an `item_id` to match this route.

#### B. Required query parameter

```python
@app.get("/search-required/")
async def search_required(q: str):
    return {"query": q}
```

```http
GET /search-required/?q=python
```

Because `q` has **no default value**, it is required. Omitting it results in an HTTP 422 validation response.

#### C. Optional query parameter

```python
@app.get("/search-optional/")
async def search_optional(q: str | None = None):
    return {"query": q}
```

In `q: str | None = None`:

- `str` means that non-null supplied values are strings.
- `| None` allows `None` as a Python value.
- `= None` supplies the default value and **makes this query parameter optional**.

```http
GET /search-optional/
GET /search-optional/?q=python
```

Both requests work. The first uses `q = None`; the second uses `q = "python"`.

> **Key distinction:** `str | None` alone does **not** make a query parameter optional. The default value (`= None`) does.

#### Why does this matter?

Optional parameters let clients request just what they need. FastAPI also shows which inputs are required and which have defaults in its automatically generated documentation.

### 5.4 Automatic Type Conversion and Validation

Values in URLs arrive as text. FastAPI converts them according to the types declared in your endpoint signature.

```python
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    return {"product_id": product_id}
```

**Valid request:**

```http
GET /products/10
```

FastAPI parses `"10"` as the integer `10`.

**Invalid request:**

```http
GET /products/abc
```

`"abc"` cannot be parsed as an integer, so FastAPI rejects the request **before** running your endpoint function.

| Status | Meaning | Example |
| :-- | :-- | :-- |
| `200 OK` | Request succeeded | `GET /products/10` with valid input |
| `404 Not Found` | A route or requested resource was not found | A missing product, when your code checks for it |
| `422 Unprocessable Content` | Request failed input validation | `GET /products/abc` |

> **Remember:** Declaring `product_id: int` checks the ID's type, not whether a product with that ID exists in the database. Resource existence and authorization checks are your responsibility.

### 5.5 Custom Validation with `Path()` and `Query()`

Sometimes checking the type isn't enough. We may also want to require:

- A product ID greater than zero.
- A search query between two and fifty characters.
- A result limit between one and one hundred.

FastAPI provides `Path()` and `Query()` to declare constraints.

```python
from typing import Annotated
from fastapi import Path, Query


@app.get("/products/{product_id}/search")
async def search_product(
    product_id: Annotated[int, Path(gt=0)],
    q: Annotated[str | None, Query(min_length=2, max_length=50)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return {
        "product_id": product_id,
        "query": q,
        "limit": limit,
    }
```

#### Parameter-by-parameter explanation

| Expression | What it does |
| :-- | :-- |
| `product_id: Annotated[int, Path(gt=0)]` | Required integer path parameter; must be `> 0` |
| `q: Annotated[str \| None, Query(min_length=2, max_length=50)] = None` | Optional query string; if supplied, must contain 2–50 characters |
| `limit: Annotated[int, Query(ge=1, le=100)] = 10` | Optional integer query parameter, default `10`, allowed range 1–100 |

**What is `Annotated`?** It comes from Python's `typing` module and lets us attach metadata—such as FastAPI validation settings—to a type annotation.

#### Common validation options

| Rule | Meaning |
| :-- | :-- |
| `gt=0` | Greater than zero (`> 0`) |
| `ge=1` | Greater than or equal to one (`>= 1`) |
| `lt=100` | Less than one hundred (`< 100`) |
| `le=100` | Less than or equal to one hundred (`<= 100`) |
| `min_length=2` | At least two characters |
| `max_length=50` | At most fifty characters |

**Valid request:**

```http
GET /products/5/search?q=laptop&limit=20
```

**Invalid request:**

```http
GET /products/5/search?q=a&limit=200
```

It fails because `q` is only one character long, and `limit` exceeds the maximum allowed value of 100. FastAPI responds with HTTP 422 and details about the invalid inputs.

### 5.6 Pagination with `skip` and `limit`

Imagine a database contains **10,000 records**. Fetching everything every time would waste bandwidth and processing resources. **Pagination** divides results into smaller groups.

For a page size of 10:

| Page | `skip` | `limit` | Records returned |
| :--: | --: | --: | :-- |
| 1 | 0 | 10 | 1–10 |
| 2 | 10 | 10 | 11–20 |
| 3 | 20 | 10 | 21–30 |
| 4 | 30 | 10 | 31–40 |

#### Working example using a Python list

```python
fake_items_db = [
    {"name": "Laptop"},
    {"name": "Mouse"},
    {"name": "Keyboard"},
    {"name": "Monitor"},
    {"name": "Headphones"},
    {"name": "Phone"},
]


@app.get("/paginated-items/")
async def read_paginated_items(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return fake_items_db[skip : skip + limit]
```

Send:

```http
GET /paginated-items/?skip=2&limit=3
```

Python evaluates:

```python
fake_items_db[2:5]
```

**Response:**

```json
[
  {"name": "Keyboard"},
  {"name": "Monitor"},
  {"name": "Headphones"}
]
```

We skipped the first two items and retrieved the next three.

> **Production note:** For large datasets, apply pagination in your database query. Avoid loading the entire table into memory. Use a stable ordering when paginating real database results.

### 5.7 Route Ordering

FastAPI processes matching routes in their declaration order. When a fixed path could also match a dynamic parameter, **declare the fixed route first**.

```python
@app.get("/users/me")
async def read_current_user():
    return {"message": "Current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

`/users/me` should appear before `/users/{user_id}` so that the word `me` isn't treated as an arbitrary user ID.

#### Path vs. query: quick comparison

| Feature | Path parameter | Query parameter |
| :-- | :-- | :-- |
| Example | `/users/42` | `/users?limit=10` |
| Typical purpose | Identify a resource | Search, filter, sort, paginate |
| Declared in route path? | Yes: `{user_id}` | No: function argument or `Query()` |
| Can it be optional? | No | Yes, with a default |

**Try this yourself:** Open <http://127.0.0.1:8000/docs>, expand an endpoint, click **Try it out**, enter different parameter values, and inspect the request URL and response.

#### Chapter recap

1. **Path parameters** identify resources and are required.
2. **Query parameters** customize requests and may be optional.
3. Type hints let FastAPI **parse and validate** inputs automatically.
4. `Path()` and `Query()` add constraints to parameter values.
5. Invalid inputs usually produce an **HTTP 422** response.
6. `skip` and `limit` support pagination, while route order helps avoid ambiguous matches.

---

## 6. Introduction to Pydantic

So far, we've used path and query parameters to pass relatively simple values. What happens if a client needs to send an entire JSON object—such as the input features for a machine learning model?

This is where **request bodies** and **Pydantic** become important.

### What is Pydantic?

[Pydantic](https://docs.pydantic.dev/) is a Python library for parsing and validating structured data using type annotations. FastAPI uses it extensively to define and validate request bodies and describe response models.

**Key benefits:**

| Feature | Why it matters |
| :-- | :-- |
| **Validation** | Check required fields, types, and constraints |
| **Serialization** | Convert structured data into JSON-compatible representations |
| **Settings** | Manage application configuration using the separate `pydantic-settings` package |
| **IDE support** | Improve autocomplete and clarity through typed models |

starting with BaseModel 

# DevLog API

DevLog API is a FastAPI backend for a personal developer journal. It allows users to register, log in, create journal entries, and attach code snippets to those entries.

## Features

- User registration
- User login with JWT authentication
- Create, read, update, and delete journal entries
- Search journal entries with pagination using `search_journal`, `limit`, and `offset`
- Create code snippets under journal entries
- Protected routes with authenticated user access
- PostgreSQL database integration with SQLAlchemy ORM

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT
- pwdlib with Argon2 password hashing

## Project Structure

```bash
app/
├── config.py
├── database.py
├── deps.py
├── main.py
├── models.py
├── ouath2.py
├── schemas.py
├── util.py
└── routers/
    ├── auth.py
    ├── entries.py
    └── snippets.py
```

## Setup

1. Clone the repository

```bash
git clone <your-repo-url>
cd devlog_api
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

Or if you use `uv`:

```bash
uv sync
```

4. Create a `.env` file

```env
DB_DRIVER=postgresql+psycopg
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=devlog_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run the server

```bash
uvicorn app.main:app --reload
```

## Authentication

This API uses JWT bearer tokens.

After login, include your token in requests like this:

```bash
Authorization: Bearer <your_token>
```

## Main Endpoints

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Entries
- `POST /entries`
- `GET /entries`
- `GET /entries/{entry_id}`
- `PUT /entries/{entry_id}`
- `DELETE /entries/{entry_id}`

### Snippets
- `POST /snippets/{entry_id}`

## Query Parameters for Entries

`GET /entries` supports:

- `search_journal`: search by entry title
- `limit`: number of results to return
- `offset`: number of results to skip

Example:

```bash
GET /entries?search_journal=python&limit=5&offset=0
```



## Author

Built by Victor Adeniyi

# API Documentation

## Project Structure
```
app/
├── auth/           # Authentication module
├── chatbot/        # Chatbot functionality
├── core/           # Core utilities
├── jobs/          # Job-related features
├── profiles/      # User profiles
├── rag/           # Retrieval-Augmented Generation
├── resumes/       # Resume handling
├── users/         # User management
├── __init__.py
├── config.py      # Configuration settings
└── main.py        # Application entry point
```

## Authentication Endpoints

### POST `/auth/register`
Register new user.
```python
Request:
{
    "email": str,
    "username": str,
    "password": str
}

Response:
{
    "id": str,
    "email": str,
    "username": str
}
```

### POST `/auth/login`
Authenticate user.
```python
Request:
{
    "email": str,
    "password": str
}

Response:
{
    "access_token": str,
    "refresh_token": str,
    "token_type": str
}
```

### POST `/auth/token/refresh`
Refresh authentication tokens.
```python
Request:
{
    "refresh_token": str
}

Response:
{
    "access_token": str,
    "refresh_token": str,
    "token_type": str
}
```

### GET `/auth/me`
Get authenticated user profile.
```python
Response:
{
    "id": str,
    "email": str,
    "username": str
}
```

## RAG Endpoints

### POST `/rag/query`
Process user query using RAG engine.
```python
Request:
{
    "query": str
}

Response:
{
    "answer": str,
    "sources": List[str]
}
```

### GET `/rag/history`
Retrieve user's query history.
```python
Response:
[
    {
        "role": str,
        "content": str,
        "timestamp": datetime
    }
]
```

## Authentication
All endpoints except `/auth/register` and `/auth/login` require JWT authentication:
```
Authorization: Bearer <access_token>
```
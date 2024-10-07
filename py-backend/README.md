# My FastAPI Project

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Create a `.env` file with the following content:
    ```env
    PINECONE_API_KEY=your_pinecone_api_key
    PINECONE_INDEX=your_pinecone_index
    GOOGLE_API_KEY=your_google_api_key
    ```

3. Run the FastAPI server:
    ```bash
    uvicorn main:app --reload --host localhost --port 3003
    ```

## Endpoints

- `GET /ping`: Health check endpoint.
- `POST /query`: Query endpoint that processes the text and returns the result.

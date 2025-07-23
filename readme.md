# URL Shortener Service

A FastAPI-based microservice for shortening URLs, backed by a MySQL database and SQLAlchemy ORM.

## Features

- Shorten long URLs to unique short codes
- Retrieve original URLs from short codes
- RESTful API endpoints
- Asynchronous database operations
- Dockerized for easy deployment

## Project Structure

```
main.py
requirements.txt
common/
    exceptions.py
    utils.py
database_service/
    abcs/
    models.py
    mysql_service/
    service.py
    __test__/
url_shortener_service/
    models.py
    router.py
    schema.py
    service.py
    __test__/
docker/
    docker-compose.yml
    Dockerfile
.env
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose

### Installation

1. Clone the repository:
    ```sh
    git clone <your-repo-url>
    cd url_shortener
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Copy `.env.example` to `.env` and configure as needed.

### Running with Docker

Start the application and MySQL database using Docker Compose:

```sh
docker compose -f docker/docker-compose.yml up --build
```

### Running Locally

1. Start MySQL and create a database named `testdb`.
2. Set `DATABASE_URL` in `.env` (e.g., `mysql://root:root@localhost:3306/testdb`).
3. Run the FastAPI app:
    ```sh
    uvicorn main:app --reload
    ```

## API Endpoints

- `POST /url_shortener/shorten`  
  Shorten a long URL.  
  **Body:** `{ "long_url": "<your-url>" }`

- `GET /url_shortener/{short_url}`  
  Retrieve the original long URL.

## Testing

Unit tests are located in the `__test__` directories.  
Run tests with:

```
pytest
```
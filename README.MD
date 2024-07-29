# Challenger Dev Python

This project is a web application with a frontend built using Streamlit and a backend built using FastAPI. The application also uses MongoDB as its database.

## Prerequisites

- Docker
- Docker Compose


### Installing Docker

#### For Windows and Mac:

1. Download Docker Desktop from [Docker's official website](https://www.docker.com/products/docker-desktop).
2. Follow the installation instructions provided in the link above.
3. After installation, Docker Desktop should start automatically. If not, you can start it from the Start menu (Windows) or Applications folder (Mac).

#### For Linux:

1. Update your existing list of packages:

    ```bash
    sudo apt-get update
    ```

2. Install a few prerequisite packages which let `apt` use packages over HTTPS:

    ```bash
    sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
    ```

3. Add the GPG key for the official Docker repository to your system:

    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

4. Add the Docker repository to `apt` sources:

    ```bash
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    ```

5. Update your existing list of packages again for the changes to take effect:

    ```bash
    sudo apt-get update
    ```

6. Install Docker:

    ```bash
    sudo apt-get install docker-ce
    ```

7. To ensure Docker is running:

    ```bash
    sudo systemctl status docker
    ```

8. (Optional) To run Docker commands without `sudo`:

    ```bash
    sudo usermod -aG docker ${USER}
    ```

    Then log out and back in so that the group membership is re-evaluated.

### Installing Docker Compose

1. Download the Docker Compose binary into the `/usr/local/bin` directory:

    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

2. Apply executable permissions to the binary:

    ```bash
    sudo chmod +x /usr/local/bin/docker-compose
    ```

3. Test the installation:

    ```bash
    docker-compose --version
   ```
## Environment Variables
Create a `.env` file in the `frontend` directory with the following content:
```dotenv
API_URL="http://backend:8000"
```
Create a `.env` file in the `backend` directory with the following content:

```dotenv
SECRET_KEY="S3gtd2fcIJYtp_TJoMcKUyksWl9kXtr8ssiwzH9HTQM"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DB_URL='mongodb://mongo:27017'
```

## Getting Started

### Clone the Repository

```bash
   git clone https://github.com/jguerrero10/challengeN5.git
   
   cd challengeN5
   ```


### Build and Run the Containers

#### Use Docker Compose to build and run the containers.

```bash
   docker-compose build
   docker-compose up -d
```

This will start the following services:

- frontend: Runs on port `8501`
- backend: Runs on port `8000`
- mongo: MongoDB instance running on port `27017`

### Create an Admin User

Once the containers are up and running, you need to create an admin user. Run the following command in your terminal:

```bash
   docker-compose exec backend python /app/create_user_admin.py admin adminpassword
```

Replace `admin` and `adminpassword` with your desired username and password.

### Docker Configuration

#### Docker Compose

Here is the docker-compose.yml configuration:

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    volumes:
      - .:/code
  mongo:
    image: mongo:latest
    volumes:
      - mongodata:/data/db
    ports:
      - '27017:27017'

volumes:
  mongodata:

```

#### Frontend Dockerfile

Here is the Dockerfile for the frontend service:

```dockerfile
FROM python:3.10-slim
LABEL authors="Joel Guerrero"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Backend Dockerfile
Here is the Dockerfile for the backend service:

```dockerfile
FROM python:3.10-alpine
LABEL authors="Joel Guerrero"

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### Creating an Admin User

The script create_user_admin.py is used to create an admin user. Here is the content of the script:

```python
from typing import Any, Dict

import typer
from pymongo import MongoClient, errors

from config import Settings
from utils.enums import Role
from utils.hash_password_utils import get_password_hash

settings = Settings()

def find_or_create_document(db_name: str, collection_name: str, query: Dict[str, Any], new_document: Dict[str, Any]):
    try:
        client = MongoClient(settings.db_url)
        db = client[db_name]
        collection = db[collection_name]
        document = collection.find_one(query)
        if document:
            print("User already exists")
            return
        else:
            result = collection.insert_one(new_document)
            created_document = collection.find_one({"_id": result.inserted_id})
            print("Document created:", created_document)
            return created_document
    except errors.PyMongoError as e:
        print(f"Error interacting with MongoDB: {e}")
        return None
    finally:
        client.close()

def main(username: str, password: str):
    query = {"username": username}
    user_data = {
        "username": username,
        "hashed_password": get_password_hash(password),
        "role": Role.ADMIN.value
    }
    find_or_create_document("challenger", "users", query, user_data)

if __name__ == '__main__':
    typer.run(main)
```
### Accessing the Application

- Frontend: Open your browser and navigate to http://localhost:8501.
- Backend: The API documentation can be accessed at http://localhost:8000/docs.


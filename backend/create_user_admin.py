from typing import Any, Dict

import typer
from pymongo import MongoClient, errors

from config import Settings
from utils.enums import Role
from utils.hash_password_utils import get_password_hash

settings = Settings()


def find_or_create_document(db_name: str, collection_name: str, query: Dict[str, Any], new_document: Dict[str, Any]):
    """
    It searches for a document in a MongoDB collection and if not found, creates it.

    :param db_name: Database name
    :param collection_name: Collection name
    :param query: Dictionary representing the query to find the document
    :param new_document: Dictionary representing the new document to be inserted if not found.
    :return: Document found or created
    """
    try:
        # Connection to the MongoDB client
        client = MongoClient(settings.db_url)

        # Connection to the MongoDB client
        db = client[db_name]
        collection = db[collection_name]

        # Document search
        document = collection.find_one(query)

        if document:
            print("User already exists")
            return
        else:
            # If not found, a new document is created.
            result = collection.insert_one(new_document)
            created_document = collection.find_one({"_id": result.inserted_id})
            print("Document created:", created_document)
            return created_document
    except errors.PyMongoError as e:
        print(f"Error interacting with MongoDB: {e}")
        return None
    finally:
        # Closing the connection
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

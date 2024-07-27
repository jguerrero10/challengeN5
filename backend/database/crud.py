from typing import Any, Dict, List

from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from database.db import database


async def add_object(collection_name: str, data: Dict[str, Any]) -> Any:
    collection = database.get_collection(collection_name)
    object_data = jsonable_encoder(data)
    new_object = await collection.insert_one(object_data)
    created_object = await collection.find_one({"_id": new_object.inserted_id})
    return created_object


async def update_object(collection_name: str, object_id: str, data: Dict[str, Any]) -> Any:
    document = await get_object(collection_name, object_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    collection = database.get_collection(collection_name)
    data = {k: v for k, v in data.items() if v is not None}
    await collection.update_one({"_id": ObjectId(object_id)}, {"$set": data})
    updated_document = await collection.find_one({"_id": ObjectId(object_id)})
    return updated_document


async def delete_object(collection_name: str, object_id: str) -> Any:
    document = await get_object(collection_name, object_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")
    collection = database.get_collection(collection_name)
    delete_result = await collection.delete_one({"_id": ObjectId(object_id)})
    return delete_result.deleted_count


async def get_object(collection_name: str, object_id: str) -> Any:
    collection = database.get_collection(collection_name)
    document = await collection.find_one({"_id": ObjectId(object_id)})
    return document


async def get_all_objects(collection_name: str) -> List[Any]:
    collection = database.get_collection(collection_name)
    documents = []
    async for document in collection.find():
        documents.append(document)
    return documents


async def search_objects(collection_name: str, field_name: str, field_value: str) -> Any:
    collection = database.get_collection(collection_name)
    query = {field_name: field_value}
    documents = []
    async for document in collection.find(query):
        documents.append(document)
    return documents

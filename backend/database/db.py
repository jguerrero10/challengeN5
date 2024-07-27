from typing import Any

import motor.motor_asyncio

MONGO_DETAILS = "mongodb://mongo:27017"

client: Any = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.challenger

from typing import Any

import motor.motor_asyncio

from config import Settings

settings = Settings()
MONGO_DETAILS = settings.db_url

client: Any = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.challenger

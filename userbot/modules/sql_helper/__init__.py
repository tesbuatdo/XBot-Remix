from pymongo import MongoClient, collection
from userbot import MONGO_URI, LOGGER


LOGGER.info("Connecting to MongoDB")

DB_CLIENT = MongoClient(MONGO_URI)

_DB = DB_CLIENT["xbot"]


def get_collection(name: str) -> collection:
    """Get the collection from database."""
    return _DB[name]

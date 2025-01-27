from mongoengine import connect
from pymongo import MongoClient

def connect_to_mongo():
    """Establishes a connection to MongoDB using both PyMongo and MongoEngine."""
    try:
        # PyMongo connection (optional, if needed)
        client = MongoClient(host="localhost", port=27017)
        db = client["backend_challenge_db"]

        # MongoEngine connection
        connect(
            db="backend_challenge_db",  # Database name
            host="mongodb://localhost:27017/backend_challenge_db",  # Connection URI
            alias="default"  # Alias for default connection
        )

        print("Connected to MongoDB successfully with MongoEngine!")
        return db  # Return the PyMongo database instance if needed
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

if __name__ == "__main__":
    db = connect_to_mongo()
    if db is not None:
        print(db.list_collection_names())

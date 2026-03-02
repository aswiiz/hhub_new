from pymongo import MongoClient
import os

# Using environment variable for production, or hardcoded string for development
MONGO_URI = os.environ.get('MONGO_URI', "")

def get_db():
    client = MongoClient(MONGO_URI)
    db = client['healthcare_db']
    return db

def init_db():
    # MongoDB creates databases and collections lazily, but we can verify connection
    try:
        db = get_db()
        # Trigger a command to check connection
        db.command('ping')
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

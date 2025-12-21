from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from environment
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Error: MONGO_URI not found in environment variables!")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Select database and collection
db = client["resume_analyzer_db"]
collection = db["analysis_results"]

print("✅ MongoDB connected successfully!")
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
import uuid
import pandas as pd

load_dotenv()

class Database:
    def __init__(self):
        # Get MongoDB URI from environment
        self.mongo_uri = os.getenv("MONGO_URI")
        if not self.mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")
        
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.feedback_db
        self.collection = self.db.submissions
        self._init_database()
    
    def _init_database(self):
        """Create indexes if they don't exist."""
        try:
            self.collection.create_index("timestamp")
            self.collection.create_index("user_rating")
            self.collection.create_index("sentiment")
            print("MongoDB connected and indexes created")
        except Exception as e:
            print(f"Database initialization warning: {e}")
    
    def add_submission(self, user_rating, user_review, ai_response, ai_summary, ai_actions, sentiment="neutral"):
        """Add a new submission to MongoDB."""
        try:
            submission = {
                "_id": str(uuid.uuid4()),
                "timestamp": datetime.now(),
                "user_rating": int(user_rating),
                "user_review": str(user_review),
                "ai_response": str(ai_response),
                "ai_summary": str(ai_summary),
                "ai_actions": str(ai_actions),
                "sentiment": str(sentiment)
            }
            
            result = self.collection.insert_one(submission)
            return str(submission["_id"])
        except Exception as e:
            print(f"Error adding submission: {e}")
            return None
    
    def get_all_submissions(self):
        """Get all submissions."""
        try:
            cursor = self.collection.find().sort("timestamp", -1)
            submissions = list(cursor)
            
            if not submissions:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(submissions)
            
            # Convert timestamp to string for display
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['timestamp_str'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Rename _id to id for consistency
            if '_id' in df.columns:
                df['id'] = df['_id']
            
            return df
        except Exception as e:
            print(f"Error getting submissions: {e}")
            return pd.DataFrame()
    
    def get_stats(self):
        """Get statistics from database."""
        try:
            # Total submissions
            total = self.collection.count_documents({})
            
            # Average rating
            pipeline = [
                {"$group": {"_id": None, "avg_rating": {"$avg": "$user_rating"}}}
            ]
            result = list(self.collection.aggregate(pipeline))
            avg_rating = result[0]["avg_rating"] if result else 0
            
            # Sentiment distribution
            pipeline = [
                {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
            ]
            sentiment_counts = {}
            for item in self.collection.aggregate(pipeline):
                sentiment_counts[item["_id"]] = item["count"]
            
            return {
                "total_submissions": total,
                "average_rating": round(avg_rating, 2) if avg_rating else 0,
                "sentiment_distribution": sentiment_counts
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                "total_submissions": 0,
                "average_rating": 0,
                "sentiment_distribution": {}
            }
    
    def delete_all_submissions(self):
        """Delete all submissions (for testing/reset)."""
        try:
            result = self.collection.delete_many({})
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting submissions: {e}")
            return 0

# Create a global database instance
db = Database()
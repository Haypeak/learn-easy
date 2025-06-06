from flask import Flask
from flask_pymongo import PyMongo
from bson import ObjectId
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("video_fixes.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Updated YouTube video mappings for specific courses
COURSE_VIDEO_MAPPINGS = {
    # Map course titles to specific video categories and URLs
    "Introduction to Python Programming": {
        "video_urls": {
            "Getting Started with Python - Video Lesson": "https://www.youtube.com/embed/rfscVS0vtbw",
            "Variables and Data Types - Video Lesson": "https://www.youtube.com/embed/rfscVS0vtbw",
            "Control Structures - Video Lesson": "https://www.youtube.com/embed/rfscVS0vtbw",
            "Python Installation Demo": "https://www.youtube.com/embed/YYXdXT2l-Gg"
        }
    },
    "Web Development with JavaScript": {
        "video_urls": {
            "JavaScript Fundamentals - Video Lesson": "https://www.youtube.com/embed/W6NZfCO5SIk",
            "DOM Manipulation - Video Lesson": "https://www.youtube.com/embed/5fb2aPlgoys",
            "Modern JavaScript (ES6+) - Video Lesson": "https://www.youtube.com/embed/NCwa_xi0Uuc",
            "Asynchronous JavaScript - Video Lesson": "https://www.youtube.com/embed/ZYb_ZU8LNxs"
        }
    },
    "Public Speaking": {
        "video_urls": {
            "Speech Structure and Organization - Video Lesson": "https://www.youtube.com/embed/8S0FDjFBj8o",
            "Delivery and Body Language - Video Lesson": "https://www.youtube.com/embed/ZK3jSXYBNak",
            "Persuasive Speaking - Video Lesson": "https://www.youtube.com/embed/eIho2S0ZahI",
            "Speaking in Different Contexts - Video Lesson": "https://www.youtube.com/embed/LpX2fCy2dqo"
        }
    },
    "Advanced Data Structures and Algorithms": {
        "video_urls": {
            "Advanced Tree Structures - Video Lesson": "https://www.youtube.com/embed/1-l_UOFi1Xw",
            "Graph Algorithms - Video Lesson": "https://www.youtube.com/embed/tWVWeAqZ0WU",
            "Dynamic Programming - Video Lesson": "https://www.youtube.com/embed/oBt53YbR9Kk",
            "Advanced Algorithm Analysis - Video Lesson": "https://www.youtube.com/embed/0JUN9aDxVmI"
        }
    }
}

def fix_mismatched_videos():
    """
    Update videos for courses that were detected as having mismatched content.
    """
    with app.app_context():
        try:
            total_updated = 0
            
            # Process each course in our mapping
            for course_title, mapping in COURSE_VIDEO_MAPPINGS.items():
                logging.info(f"Processing course: {course_title}")
                
                # Find the course by title
                course = mongo.db.courses.find_one({"title": course_title})
                if not course:
                    logging.warning(f"Course not found: {course_title}")
                    continue
                
                course_id = course["_id"]
                video_urls = mapping.get("video_urls", {})
                
                # Update each video in the course
                for video_title, new_url in video_urls.items():
                    video = mongo.db.course_content.find_one({
                        "course_id": course_id,
                        "title": video_title,
                        "type": "video"
                    })
                    
                    if not video:
                        logging.warning(f"Video not found: {video_title} in course {course_title}")
                        continue
                    
                    old_url = video.get("content", "")
                    
                    # Update the video URL
                    mongo.db.course_content.update_one(
                        {"_id": video["_id"]},
                        {"$set": {"content": new_url}}
                    )
                    
                    total_updated += 1
                    logging.info(f"Updated video: '{video_title}'")
                    logging.info(f"Old URL: {old_url}")
                    logging.info(f"New URL: {new_url}")
            
            logging.info(f"Successfully updated {total_updated} videos with more relevant content")
            
        except Exception as e:
            logging.error(f"Error in fix_mismatched_videos: {str(e)}")

if __name__ == "__main__":
    logging.info("Starting fix for mismatched videos...")
    fix_mismatched_videos()
    logging.info("Fix completed.")


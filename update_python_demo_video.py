from flask import Flask
from flask_pymongo import PyMongo
import logging
import sys
import re
from bson import ObjectId

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("python_demo_fix.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"
mongo = PyMongo(app)

def find_python_courses():
    """
    Find all Python-related courses in the database.
    Uses case-insensitive regex pattern to find any course with 'python' in the title.
    """
    with app.app_context():
        # Use regex to find any course with 'python' in the title (case-insensitive)
        python_courses = list(mongo.db.courses.find({
            "title": {"$regex": "python", "$options": "i"}
        }))
        
        logging.info(f"Found {len(python_courses)} Python-related courses")
        
        # Print details of each found course
        for idx, course in enumerate(python_courses, 1):
            logging.info(f"Course {idx}: {course.get('title')} (ID: {course.get('_id')})")
            logging.info(f"  Level: {course.get('level')}")
            logging.info(f"  Topics: {', '.join(course.get('topics', []))}")
        
        return python_courses

def find_python_videos(course_id):
    """
    Find all video content items for a specific course.
    """
    with app.app_context():
        videos = list(mongo.db.course_content.find({
            "course_id": course_id,
            "type": "video"
        }))
        
        logging.info(f"Found {len(videos)} videos for course ID: {course_id}")
        
        # Print details of each found video
        for idx, video in enumerate(videos, 1):
            logging.info(f"Video {idx}: {video.get('title')}")
            logging.info(f"  Content: {video.get('content')}")
            logging.info(f"  Order: {video.get('order', 'N/A')}")
        
        return videos

def update_python_demo_video():
    """
    Update the Python Installation Demo video to use the correct YouTube URL.
    """
    with app.app_context():
        try:
            # Find all Python courses
            python_courses = find_python_courses()
            
            if not python_courses:
                logging.error("No Python courses found")
                return
            
            # Check each course for Python demo videos
            updated = False
            
            for course in python_courses:
                course_id = course["_id"]
                course_title = course["title"]
                
                logging.info(f"Checking videos for course: {course_title}")
                
                # Find all videos for this course
                videos = find_python_videos(course_id)
                
                # Try to find a Python installation video
                python_installation_videos = []
                
                for video in videos:
                    video_title = video.get('title', '').lower()
                    if 'python' in video_title and ('install' in video_title or 'demo' in video_title):
                        python_installation_videos.append(video)
                
                # Process found installation videos
                if python_installation_videos:
                    logging.info(f"Found {len(python_installation_videos)} Python installation videos")
                    
                    for video in python_installation_videos:
                        video_id = video["_id"]
                        video_title = video.get('title', '')
                        old_content = video.get('content', '')
                        
                        # Set the new YouTube URL with the correct ID
                        new_content = "https://www.youtube.com/embed/YYXdXT2l-Gg"
                        
                        logging.info(f"Updating video: {video_title}")
                        
                        # Update the video content
                        result = mongo.db.course_content.update_one(
                            {"_id": video_id},
                            {"$set": {"content": new_content}}
                        )
                        
                        if result.modified_count > 0:
                            logging.info(f"Successfully updated video: {video_title}")
                            logging.info(f"Old content: {old_content}")
                            logging.info(f"New content: {new_content}")
                            updated = True
                        else:
                            logging.warning(f"No changes made to video: {video_title}")
                else:
                    logging.warning(f"No Python installation videos found for course: {course_title}")
            
            if not updated:
                # No installation videos found, try to update any Python video
                logging.info("No Python installation videos found. Attempting to update any Python-related video...")
                
                # Find a Python video to update
                for course in python_courses:
                    videos = find_python_videos(course["_id"])
                    
                    if videos:
                        # Use the first video
                        video = videos[0]
                        video_id = video["_id"]
                        video_title = video.get('title', '')
                        old_content = video.get('content', '')
                        
                        # Set the new YouTube URL
                        new_content = "https://www.youtube.com/embed/YYXdXT2l-Gg"
                        
                        logging.info(f"Updating Python video: {video_title}")
                        
                        # Update the video content
                        result = mongo.db.course_content.update_one(
                            {"_id": video_id},
                            {"$set": {"content": new_content}}
                        )
                        
                        if result.modified_count > 0:
                            logging.info(f"Successfully updated video: {video_title}")
                            logging.info(f"Old content: {old_content}")
                            logging.info(f"New content: {new_content}")
                            updated = True
                            break
            
            # Verify the updates
            if updated:
                verify_updates()
            else:
                logging.error("No videos were updated")
                
        except Exception as e:
            logging.error(f"Error updating Python video: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())

def verify_updates():
    """
    Verify the Python videos were updated correctly.
    """
    with app.app_context():
        try:
            # Find all Python courses
            python_courses = find_python_courses()
            
            if not python_courses:
                return
            
            logging.info("\nVERIFICATION:")
            
            # Check each course
            for course in python_courses:
                course_id = course["_id"]
                course_title = course["title"]
                
                # Get all videos for this course
                videos = list(mongo.db.course_content.find({
                    "course_id": course_id,
                    "type": "video"
                }))
                
                if videos:
                    logging.info(f"Videos for course '{course_title}':")
                    
                    for video in videos:
                        video_title = video.get('title', '')
                        video_url = video.get('content', '')
                        
                        logging.info(f"Video: '{video_title}'")
                        logging.info(f"Content URL: {video_url}")
                        
                        # Check if Python Installation Demo has the correct URL
                        if 'install' in video_title.lower() or 'demo' in video_title.lower():
                            if video_url == "https://www.youtube.com/embed/YYXdXT2l-Gg":
                                logging.info("✓ Video has the correct YouTube URL")
                            else:
                                logging.warning("✗ Video does not have the correct YouTube URL")
                        
                        logging.info("---")
                
        except Exception as e:
            logging.error(f"Error in verify_updates: {str(e)}")

if __name__ == "__main__":
    logging.info("Starting Python Installation Demo video update...")
    update_python_demo_video()
    logging.info("Update process completed.")


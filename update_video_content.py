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
        logging.FileHandler("video_updates.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"
mongo = PyMongo(app)

# YouTube video mapping by topic and level
# Format: {topic_keyword: {level: youtube_url}}
YOUTUBE_VIDEOS = {
    # Information Technology videos
    "cybersecurity": {
        "beginner": "https://www.youtube.com/embed/inWWhr5tnEA",  # Intro to Cybersecurity by Simplilearn
        "intermediate": "https://www.youtube.com/embed/rcDO8km6R6c"  # Network Security by freeCodeCamp
    },
    "network": {
        "beginner": "https://www.youtube.com/embed/3QhU9jd03a0",  # Computer Networking by Network Direction
        "intermediate": "https://www.youtube.com/embed/qiQR5rTSshw"  # Computer Networking Complete Course by freeCodeCamp
    },
    "database": {
        "beginner": "https://www.youtube.com/embed/HXV3zeQKqGY",  # SQL Tutorial by freeCodeCamp
        "intermediate": "https://www.youtube.com/embed/ztHopE5Wnpc"  # Database Design Course by freeCodeCamp
    },
    "cloud": {
        "beginner": "https://www.youtube.com/embed/M988_fsOSWo",  # Cloud Computing Explained by AWS
        "intermediate": "https://www.youtube.com/embed/2LaAJq1lB1Q"  # AWS Certified Cloud Practitioner by freeCodeCamp
    },
    
    # Programming Languages
    "python": {
        "beginner": "https://www.youtube.com/embed/rfscVS0vtbw",  # Python Tutorial for Beginners by freeCodeCamp
        "intermediate": "https://www.youtube.com/embed/HGOBQPFzWKo"  # Intermediate Python by Corey Schafer
    },
    "javascript": {
        "beginner": "https://www.youtube.com/embed/W6NZfCO5SIk",  # JavaScript Tutorial for Beginners by Programming with Mosh
        "intermediate": "https://www.youtube.com/embed/PkZNo7MFNFg"  # Learn JavaScript by freeCodeCamp
    },
    "web development": {
        "beginner": "https://www.youtube.com/embed/QA0XpGhiz5w",  # Web Development Roadmap by Traversy Media
        "intermediate": "https://www.youtube.com/embed/0pThnRneDjw"  # Web Development in 2023 by Traversy Media
    },
    
    # Mathematics videos
    "calculus": {
        "beginner": "https://www.youtube.com/embed/HfACrKJ_Y2w",  # Calculus 1 by Professor Leonard
        "intermediate": "https://www.youtube.com/embed/WsQQvHm4lSw"  # Essence of Calculus by 3Blue1Brown
    },
    "linear algebra": {
        "beginner": "https://www.youtube.com/embed/fNk_zzaMoSs",  # Linear Algebra by 3Blue1Brown
        "intermediate": "https://www.youtube.com/embed/JnTa9XtvmfI"  # Linear Algebra by MIT OpenCourseWare
    },
    "statistics": {
        "beginner": "https://www.youtube.com/embed/xxpc-HPKN28",  # Statistics Made Easy by StatQuest
        "intermediate": "https://www.youtube.com/embed/zouPoc49xbk"  # Statistics by Khan Academy
    },
    "discrete": {
        "beginner": "https://www.youtube.com/embed/rdXw7Ps9vxc",  # Discrete Math by TheTrevTutor
        "intermediate": "https://www.youtube.com/embed/2gFA9y6X2QA"  # Discrete Math by Trefor Bazett
    },
    
    # Language Arts videos
    "writing": {
        "beginner": "https://www.youtube.com/embed/GgkRoYPLhts",  # Creative Writing by Brandon Sanderson
        "intermediate": "https://www.youtube.com/embed/N4ZDBOc2tX8"  # Fiction Writing by Reedsy
    },
    "communication": {
        "beginner": "https://www.youtube.com/embed/Unzc731iCUY",  # How to Speak by MIT
        "intermediate": "https://www.youtube.com/embed/RO16LNL-YJY"  # Business Communication by Study IQ
    },
    "speaking": {
        "beginner": "https://www.youtube.com/embed/8S0FDjFBj8o",  # Public Speaking for Beginners by Communication Coach Alex Lyon
        "intermediate": "https://www.youtube.com/embed/Xe2MbMxuUuY"  # TED Talk on Public Speaking
    },
    "public speaking": {
        "beginner": "https://www.youtube.com/embed/8S0FDjFBj8o",  # Public Speaking for Beginners by Communication Coach Alex Lyon
        "intermediate": "https://www.youtube.com/embed/Xe2MbMxuUuY"  # TED Talk on Public Speaking
    },
    "literature": {
        "beginner": "https://www.youtube.com/embed/MSYw502dJNY",  # How to Analyze Literature by CrashCourse
        "intermediate": "https://www.youtube.com/embed/QM4LzhF-Vp8"  # English Literature by Crash Course
    },
    
    # Default videos (fallback)
    "default": {
        "beginner": "https://www.youtube.com/embed/yfoY53QXEnI",  # CSS Crash Course by Traversy Media
        "intermediate": "https://www.youtube.com/embed/hdI2bqOjy3c"  # JavaScript Crash Course by Traversy Media
    }
}

def find_appropriate_video(course, section_title):
    """
    Find the most appropriate YouTube video URL based on course info and section title.
    """
    course_title = course.get('title', '').lower()
    course_level = course.get('level', 'beginner').lower()
    course_topics = [topic.lower() for topic in course.get('topics', [])]
    section_title = section_title.lower()
    
    # Try to match based on section title first
    for keyword in YOUTUBE_VIDEOS.keys():
        if keyword in section_title:
            return YOUTUBE_VIDEOS[keyword].get(course_level, YOUTUBE_VIDEOS[keyword]['beginner'])
    
    # Then try to match with course title
    for keyword in YOUTUBE_VIDEOS.keys():
        if keyword in course_title:
            return YOUTUBE_VIDEOS[keyword].get(course_level, YOUTUBE_VIDEOS[keyword]['beginner'])
    
    # Then check course topics
    for topic in course_topics:
        for keyword in YOUTUBE_VIDEOS.keys():
            if keyword in topic:
                return YOUTUBE_VIDEOS[keyword].get(course_level, YOUTUBE_VIDEOS[keyword]['beginner'])
    
    # Use default if no match is found
    return YOUTUBE_VIDEOS['default'].get(course_level, YOUTUBE_VIDEOS['default']['beginner'])

def update_video_content():
    """
    Update all video content in the database with appropriate YouTube URLs.
    """
    with app.app_context():
        try:
            # Find all video content items
            video_content_items = list(mongo.db.course_content.find({"type": "video"}))
            logging.info(f"Found {len(video_content_items)} video content items to update")
            
            update_count = 0
            for video_item in video_content_items:
                try:
                    video_id = video_item.get('_id')
                    course_id = video_item.get('course_id')
                    video_title = video_item.get('title', '')
                    
                    # Get the corresponding course
                    course = mongo.db.courses.find_one({"_id": course_id})
                    if not course:
                        logging.warning(f"Course not found for video item {video_id}")
                        continue
                    
                    # Get current content
                    old_content = video_item.get('content', '')
                    
                    # Find appropriate YouTube URL
                    youtube_url = find_appropriate_video(course, video_title)
                    
                    # Update the video content with the YouTube URL
                    mongo.db.course_content.update_one(
                        {"_id": video_id},
                        {"$set": {"content": youtube_url}}
                    )
                    
                    update_count += 1
                    logging.info(f"Updated video: '{video_title}' for course: '{course.get('title')}'")
                    logging.info(f"Old content: {old_content}")
                    logging.info(f"New content: {youtube_url}")
                    
                except Exception as e:
                    logging.error(f"Error updating video item {video_item.get('_id')}: {str(e)}")
                    
            logging.info(f"Successfully updated {update_count} out of {len(video_content_items)} video items")
            
            # Verify updates
            verify_updates()
            
        except Exception as e:
            logging.error(f"Error in update_video_content: {str(e)}")

def verify_updates():
    """
    Verify that video content was updated correctly.
    """
    with app.app_context():
        try:
            # Sample a few updated video items to verify
            sample_videos = list(mongo.db.course_content.find({"type": "video"}).limit(5))
            
            logging.info("\nVERIFICATION OF UPDATES:")
            for video in sample_videos:
                course = mongo.db.courses.find_one({"_id": video.get('course_id')})
                course_title = course.get('title') if course else "Unknown Course"
                
                logging.info(f"Video: '{video.get('title')}'")
                logging.info(f"Course: '{course_title}'")
                logging.info(f"Content URL: {video.get('content')}")
                logging.info("---")
                
            logging.info("Verification complete.")
            
        except Exception as e:
            logging.error(f"Error in verify_updates: {str(e)}")

if __name__ == "__main__":
    logging.info("Starting video content update process...")
    update_video_content()
    logging.info("Video content update process completed.")


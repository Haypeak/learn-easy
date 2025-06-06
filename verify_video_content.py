from flask import Flask
from flask_pymongo import PyMongo
from bson import ObjectId
from tabulate import tabulate
import re

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Dictionary to categorize YouTube videos
YOUTUBE_CATEGORIES = {
    "cybersecurity": ["inWWhr5tnEA", "rcDO8km6R6c"],
    "network": ["3QhU9jd03a0", "qiQR5rTSshw"],
    "database": ["HXV3zeQKqGY", "ztHopE5Wnpc"],
    "cloud": ["M988_fsOSWo", "2LaAJq1lB1Q"],
    "calculus": ["HfACrKJ_Y2w", "WsQQvHm4lSw"],
    "linear algebra": ["fNk_zzaMoSs", "JnTa9XtvmfI"],
    "statistics": ["xxpc-HPKN28", "zouPoc49xbk"],
    "discrete": ["rdXw7Ps9vxc", "2gFA9y6X2QA"],
    "writing": ["GgkRoYPLhts", "N4ZDBOc2tX8"],
    "communication": ["Unzc731iCUY", "RO16LNL-YJY"],
    "speaking": ["8S0FDjFBj8o", "ZK3jSXYBNak", "eIho2S0ZahI", "LpX2fCy2dqo", "Unzc731iCUY", "Xe2MbMxuUuY"],
    "literature": ["MSYw502dJNY", "QM4LzhF-Vp8"],
    "default": ["yfoY53QXEnI", "hdI2bqOjy3c"],
    "python": ["rfscVS0vtbw", "YYXdXT2l-Gg", "HGOBQPFzWKo"],
    "javascript": ["W6NZfCO5SIk", "5fb2aPlgoys", "NCwa_xi0Uuc", "ZYb_ZU8LNxs", "PkZNo7MFNFg"],
    "algorithms": ["1-l_UOFi1Xw", "tWVWeAqZ0WU", "oBt53YbR9Kk", "0JUN9aDxVmI"]
}

def extract_video_id(url):
    """Extract YouTube video ID from embed URL"""
    if not url:
        return None
    match = re.search(r'embed/([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None

def determine_category(video_id):
    """Determine which category a video ID belongs to"""
    for category, ids in YOUTUBE_CATEGORIES.items():
        if video_id in ids:
            return category
    return "unknown"

def verify_match(course_topics, video_category):
    """Verify if the video category matches any of the course topics"""
    course_topics_lower = [topic.lower() for topic in course_topics]
    
    # Check for direct match
    if video_category in course_topics_lower:
        return "✓ Match"
    
    # Check for partial match
    for topic in course_topics_lower:
        if video_category in topic or topic in video_category:
            return "✓ Partial match"
    
    # Use broader category matching
    category_mappings = {
        "cybersecurity": ["security", "cyber", "protection", "threat"],
        "network": ["networking", "tcp/ip", "admin", "infrastructure"],
        "database": ["sql", "nosql", "data", "mongodb"],
        "cloud": ["aws", "azure", "computing", "saas", "paas", "iaas"],
        "calculus": ["math", "derivatives", "limits", "differentiation"],
        "linear algebra": ["math", "matrices", "vectors", "eigenvalue"],
        "statistics": ["math", "probability", "data", "regression"],
        "discrete": ["math", "combinatorics", "graph theory", "logic"],
        "writing": ["creative", "fiction", "non-fiction", "narrative"],
        "communication": ["business", "professional", "email"],
        "speaking": ["public", "speech", "presentation", "persuasive"],
        "literature": ["english", "poetry", "novel", "literary"]
    }
    
    if video_category in category_mappings:
        for keyword in category_mappings[video_category]:
            for topic in course_topics_lower:
                if keyword in topic:
                    return "✓ Topic match"
    
    return "✗ No match"

def verify_video_content():
    """
    Verify the video content updates by displaying course and video information
    and checking if videos match course topics.
    """
    with app.app_context():
        # Get all courses
        courses = list(mongo.db.courses.find().sort("title", 1))
        
        print(f"\n{'='*100}")
        print(f"VERIFICATION OF VIDEO CONTENT UPDATES - FOUND {len(courses)} COURSES")
        print(f"{'='*100}\n")
        
        # Iterate through each course
        for course in courses:
            course_id = course["_id"]
            course_title = course["title"]
            course_level = course.get("level", "unknown")
            course_topics = course.get("topics", [])
            
            # Get videos for this course
            videos = list(mongo.db.course_content.find(
                {"course_id": course_id, "type": "video"}
            ).sort("order", 1))
            
            if not videos:
                continue
                
            print(f"\nCOURSE: {course_title}")
            print(f"Level: {course_level}")
            print(f"Topics: {', '.join(course_topics)}")
            print("-" * 100)
            
            # Prepare data for tabulation
            table_data = []
            for video in videos:
                video_title = video.get("title", "Untitled")
                video_url = video.get("content", "")
                video_id = extract_video_id(video_url)
                video_category = determine_category(video_id)
                match_status = verify_match(course_topics, video_category)
                
                table_data.append([
                    video_title,
                    video_url,
                    video_category,
                    match_status
                ])
            
            # Display video information in a table
            print(tabulate(
                table_data,
                headers=["Video Title", "URL", "Category", "Match Status"],
                tablefmt="grid"
            ))
            print("\n")
            
def get_video_category_stats():
    """Generate statistics on video categories used"""
    with app.app_context():
        # Get all video content
        videos = list(mongo.db.course_content.find({"type": "video"}))
        
        # Count videos by category
        category_counts = {}
        
        for video in videos:
            video_url = video.get("content", "")
            video_id = extract_video_id(video_url)
            category = determine_category(video_id)
            
            if category not in category_counts:
                category_counts[category] = 0
            category_counts[category] += 1
        
        # Display statistics
        print(f"\n{'='*50}")
        print("VIDEO CATEGORY STATISTICS")
        print(f"{'='*50}")
        
        table_data = [[category, count] for category, count in category_counts.items()]
        table_data.sort(key=lambda x: x[1], reverse=True)
        table_data.append(["TOTAL", sum(category_counts.values())])
        
        print(tabulate(
            table_data,
            headers=["Category", "Count"],
            tablefmt="grid"
        ))

if __name__ == "__main__":
    print("Starting video content verification...")
    verify_video_content()
    get_video_category_stats()
    print("\nVerification complete!")


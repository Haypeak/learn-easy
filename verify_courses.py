from flask import Flask, jsonify, request, abort
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from dotenv import load_dotenv
from tabulate import tabulate
from bson import ObjectId

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority")
app.config["MONGO_URI"] = MONGO_URI

# Initialize PyMongo
mongo = PyMongo(app)

def display_category_summary():
    """Display summary of courses by category"""
    print("\n===== COURSE SUMMARY BY CATEGORY =====")
    
    categories = ["Information Technology", "Mathematics", "Language Arts"]
    
    table_data = []
    total_courses = 0
    
    for category in categories:
        course_count = mongo.db.courses.count_documents({"category": category})
        total_courses += course_count
        table_data.append([category, course_count])
    
    # Add total row
    table_data.append(["TOTAL", total_courses])
    
    print(tabulate(table_data, headers=["Category", "Number of Courses"], tablefmt="grid"))

def list_courses_by_category():
    """List all courses grouped by category"""
    categories = ["Information Technology", "Mathematics", "Language Arts"]
    
    for category in categories:
        print(f"\n===== {category.upper()} COURSES =====")
        
        courses = mongo.db.courses.find({"category": category})
        
        table_data = []
        for course in courses:
            # Run verification functions
            display_category_summary()
            list_courses_by_category()
            # show_course_sample() function is not defined, so this line is removed
            show_statistics()
            
            print("\nTo view results in a web browser:")
            print("1. Run 'flask --app verify_courses run'")
            print("2. Visit http://localhost:5000/api/courses or http://localhost:5000/api/statistics")
            print("3. Access course details at http://localhost:5000/learning/courses/<course_id>")
    """Display detailed information for one course from each category"""
    categories = ["Information Technology", "Mathematics", "Language Arts"]
    
    for category in categories:
        print(f"\n===== SAMPLE {category.upper()} COURSE =====")
        
        # Get first course in category
        course = mongo.db.courses.find_one({"category": category})
        
        if course:
            print(f"Title: {course['title']}")
            print(f"Description: {course['description']}")
            print(f"Level: {course['level']}")
            print(f"Author: {course['author']}")
            print(f"Topics: {', '.join(course['topics'])}")
            print(f"Created at: {course['created_at']}")
            
            # Display sections
            print("\nSections:")
            for i, section in enumerate(course["structure"]["sections"], 1):
                print(f"  {i}. {section['title']}")
            
            # Show content samples for this course
            print("\nContent Samples:")
            course_id = course["_id"]
            content_samples = mongo.db.course_content.find({"course_id": course_id}).limit(3)
            
            for content in content_samples:
                print(f"\n  Title: {content['title']}")
                print(f"  Type: {content['type']}")
                print(f"  Order: {content['order']}")
                
                # Truncate content to keep output manageable
                content_text = content['content']
                if len(content_text) > 100:
                    content_text = content_text[:100] + "..."
                print(f"  Content: {content_text}")

def show_statistics():
    """Display database statistics"""
    print("\n===== DATABASE STATISTICS =====")
    
    # Course statistics
    course_count = mongo.db.courses.count_documents({})
    content_count = mongo.db.course_content.count_documents({})
    
    # Calculate average sections per course
    pipeline = [
        {"$project": {"sectionCount": {"$size": "$structure.sections"}}},
        {"$group": {"_id": None, "avgSections": {"$avg": "$sectionCount"}}}
    ]
    avg_result = list(mongo.db.courses.aggregate(pipeline))
    avg_sections = avg_result[0]["avgSections"] if avg_result else 0
    
    # Count content types
    article_count = mongo.db.course_content.count_documents({"type": "article"})
    video_count = mongo.db.course_content.count_documents({"type": "video"})
    exercise_count = mongo.db.course_content.count_documents({"type": "exercise"})
    quiz_count = mongo.db.course_content.count_documents({"type": "quiz"})
    
    # Display statistics
    print(f"Total courses: {course_count}")
    print(f"Total content items: {content_count}")
    print(f"Average sections per course: {avg_sections:.2f}")
    print("\nContent breakdown:")
    print(f"  Articles: {article_count}")
    print(f"  Videos: {video_count}")
    print(f"  Exercises: {exercise_count}")
    print(f"  Quizzes: {quiz_count}")

@app.route('/api/statistics')
def statistics_api():
    """API endpoint to get database statistics"""
    # Course statistics
    course_count = mongo.db.courses.count_documents({})
    content_count = mongo.db.course_content.count_documents({})
    
    # Count by category
    categories = ["Information Technology", "Mathematics", "Language Arts"]
    category_counts = {}
    for category in categories:
        category_counts[category] = mongo.db.courses.count_documents({"category": category})
    
    # Count content types
    content_types = {
        "articles": mongo.db.course_content.count_documents({"type": "article"}),
        "videos": mongo.db.course_content.count_documents({"type": "video"}),
        "exercises": mongo.db.course_content.count_documents({"type": "exercise"}),
        "quizzes": mongo.db.course_content.count_documents({"type": "quiz"})
    }
    
    return jsonify({
        "total_courses": course_count,
        "total_content_items": content_count,
        "courses_by_category": category_counts,
        "content_by_type": content_types
    })

@app.route('/learning/courses/<course_id>', methods=['GET', 'OPTIONS'])
def get_course_details(course_id):
    """API endpoint to get detailed course information by ID"""
    if request.method == 'OPTIONS':
        # Handle OPTIONS request (pre-flight request)
        return jsonify({"message": "CORS preflight request successful"}), 200
    
    try:
        # Verify if the course ID is a valid ObjectId
        if not ObjectId.is_valid(course_id):
            return jsonify({"error": "Invalid course ID format"}), 400
        
        # Find the course by ID
        course = mongo.db.courses.find_one({"_id": ObjectId(course_id)})
        
        if not course:
            return jsonify({"error": "Course not found"}), 404
        
        # Convert ObjectId to string for JSON serialization
        course_dict = dict(course)
        course_dict["_id"] = str(course_dict["_id"])
        
        # Convert datetime to string for JSON serialization
        if "created_at" in course_dict:
            course_dict["created_at"] = course_dict["created_at"].isoformat()
        
        # Get all content for this course
        course_content = list(mongo.db.course_content.find({"course_id": ObjectId(course_id)}))
        
        # Process course content for JSON serialization
        content_list = []
        for content in course_content:
            content_dict = dict(content)
            content_dict["_id"] = str(content_dict["_id"])
            content_dict["course_id"] = str(content_dict["course_id"])
            content_list.append(content_dict)
        
        # Sort content by order field
        content_list.sort(key=lambda x: x.get("order", 0))
        
        # Create the response object
        response = {
            "course": course_dict,
            "content": content_list
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a general error handler for 404 errors
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "The requested resource was not found"}), 404

# Add a general error handler for other errors
@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500
    # Course statistics
    course_count = mongo.db.courses.count_documents({})
    content_count = mongo.db.course_content.count_documents({})
    
    # Count by category
    categories = ["Information Technology", "Mathematics", "Language Arts"]
    category_counts = {}
    for category in categories:
        category_counts[category] = mongo.db.courses.count_documents({"category": category})
    
    # Count content types
    content_types = {
        "articles": mongo.db.course_content.count_documents({"type": "article"}),
        "videos": mongo.db.course_content.count_documents({"type": "video"}),
        "exercises": mongo.db.course_content.count_documents({"type": "exercise"}),
        "quizzes": mongo.db.course_content.count_documents({"type": "quiz"})
    }
    
    return jsonify({
        "total_courses": course_count,
        "total_content_items": content_count,
        "courses_by_category": category_counts,
        "content_by_type": content_types
    })

if __name__ == "__main__":
    with app.app_context():
        try:
            # Check database connection
            mongo.db.command("ping")
            print("Connected to MongoDB!\n")
            
            # Run verification functions
            display_category_summary()
            list_courses_by_category()
            show_course_sample()
            show_statistics()
            
            print("\nTo view results in a web browser:")
            print("1. Run 'flask --app verify_courses run'")
            print("2. Visit http://localhost:5000/api/courses or http://localhost:5000/api/statistics")
            
        except Exception as e:
            print(f"Database error: {e}")

from pymongo import MongoClient
from collections import Counter

# MongoDB connection
MONGO_URI = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Learn_Easy"]

def print_separator():
    print("-" * 80)

# 1. List all courses with their basic information
print_separator()
print("COURSES SUMMARY")
print_separator()

courses = list(db.courses.find())
print(f"Total courses found: {len(courses)}")
print()

for i, course in enumerate(courses, 1):
    print(f"Course {i}: {course['title']}")
    print(f"ID: {course['_id']}")
    print(f"Level: {course['level']}")
    print(f"Author: {course['author']}")
    print(f"Topics: {', '.join(course['topics'])}")
    print(f"Description: {course['description'][:100]}...")
    
    # Count sections
    sections_count = len(course['structure']['sections'])
    
    # Count content items for this course
    content_count = db.course_content.count_documents({"course_id": course["_id"]})
    
    print(f"Number of sections: {sections_count}")
    print(f"Number of content items: {content_count}")
    print()

# 2. Course level distribution
print_separator()
print("COURSE LEVEL DISTRIBUTION")
print_separator()

level_counter = Counter([course['level'] for course in courses])
for level, count in level_counter.items():
    print(f"{level.capitalize()}: {count} course(s)")
print()

# 3. Topic distribution
print_separator()
print("TOPIC DISTRIBUTION")
print_separator()

# Flatten the list of topics from all courses
all_topics = []
for course in courses:
    all_topics.extend(course['topics'])

topic_counter = Counter(all_topics)
for topic, count in topic_counter.most_common():
    print(f"{topic}: {count} occurrence(s)")
print()

# 4. Content type distribution
print_separator()
print("CONTENT TYPE DISTRIBUTION")
print_separator()

all_content = list(db.course_content.find())
content_type_counter = Counter([content['type'] for content in all_content])
for content_type, count in content_type_counter.items():
    print(f"{content_type.capitalize()}: {count} item(s)")
print()

print_separator()
print("VERIFICATION COMPLETE")
print_separator()


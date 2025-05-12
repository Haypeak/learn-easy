from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import uuid

# MongoDB connection
MONGO_URI = "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["Learn_Easy"]

def generate_quiz_id():
    """Generate a unique quiz ID"""
    return str(uuid.uuid4())

# Clear existing courses and course_content (optional, comment out if you want to keep existing data)
db.courses.delete_many({})
db.course_content.delete_many({})

# Define courses
courses = [
    {
        "title": "Introduction to Python Programming",
        "description": "Learn the fundamentals of Python programming language, from variables and data types to functions and file handling.",
        "level": "beginner",
        "topics": ["Python", "Programming Basics", "Control Flow", "Functions"],
        "created_at": datetime.utcnow(),
        "author": "Dr. Sarah Johnson",
        "content": "<p>This comprehensive course covers Python basics for complete beginners.</p>",
        "structure": {
            "sections": [
                {
                    "title": "Getting Started with Python",
                    "description": "Learn about Python's history, installation, and write your first Python program.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Python Fundamentals Quiz"
                        }
                    ]
                },
                {
                    "title": "Variables and Data Types",
                    "description": "Understand Python's data types, variables, and basic operations.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Data Types and Variables Quiz"
                        }
                    ]
                },
                {
                    "title": "Control Structures",
                    "description": "Learn about conditionals, loops, and flow control in Python.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Control Flow Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Web Development with JavaScript",
        "description": "Master JavaScript for web development. Learn DOM manipulation, event handling, and modern ES6+ features.",
        "level": "intermediate",
        "topics": ["JavaScript", "Web Development", "DOM", "ES6"],
        "created_at": datetime.utcnow(),
        "author": "Mark Thompson",
        "content": "<p>Enhance your web development skills with modern JavaScript techniques.</p>",
        "structure": {
            "sections": [
                {
                    "title": "JavaScript Fundamentals",
                    "description": "Review core JavaScript concepts and syntax.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "JavaScript Basics Quiz"
                        }
                    ]
                },
                {
                    "title": "DOM Manipulation",
                    "description": "Learn to interact with and modify HTML elements using JavaScript.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "DOM Manipulation Quiz"
                        }
                    ]
                },
                {
                    "title": "Modern JavaScript (ES6+)",
                    "description": "Explore arrow functions, destructuring, modules, and other modern JavaScript features.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "ES6 Features Quiz"
                        }
                    ]
                },
                {
                    "title": "Asynchronous JavaScript",
                    "description": "Master promises, async/await, and handling asynchronous operations.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Async JavaScript Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Advanced Data Structures and Algorithms",
        "description": "Deep dive into complex data structures and algorithms for efficient problem solving and technical interviews.",
        "level": "advanced",
        "topics": ["Algorithms", "Data Structures", "Time Complexity", "Problem Solving"],
        "created_at": datetime.utcnow(),
        "author": "Prof. Alex Rivera",
        "content": "<p>Master advanced algorithmic concepts and complex data structures for competitive programming and technical interviews.</p>",
        "structure": {
            "sections": [
                {
                    "title": "Advanced Tree Structures",
                    "description": "Explore balanced trees, tries, and specialized tree structures.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Advanced Trees Quiz"
                        }
                    ]
                },
                {
                    "title": "Graph Algorithms",
                    "description": "Learn about graph traversal, shortest path algorithms, and network flow.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Graph Algorithms Quiz"
                        }
                    ]
                },
                {
                    "title": "Dynamic Programming",
                    "description": "Master the art of solving complex problems using dynamic programming techniques.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Dynamic Programming Quiz"
                        }
                    ]
                },
                {
                    "title": "Advanced Algorithm Analysis",
                    "description": "Learn to analyze algorithm efficiency, optimization techniques, and complexity theory.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Algorithm Analysis Quiz"
                        }
                    ]
                }
            ]
        }
    }
]

# Insert courses and create course content
for course in courses:
    # Insert course and get its ID
    course_result = db.courses.insert_one(course)
    course_id = course_result.inserted_id
    print(f"Inserted course: {course['title']} with ID: {course_id}")
    
    # Create and insert course content for each section
    order = 1
    for section in course["structure"]["sections"]:
        # Add introduction content
        intro_content = {
            "course_id": course_id,
            "title": f"Introduction to {section['title']}",
            "type": "article",
            "content": f"<p>{section['description']}</p><p>This module will guide you through {section['title'].lower()} with practical examples and exercises.</p>",
            "order": order
        }
        db.course_content.insert_one(intro_content)
        order += 1
        
        # Add video lesson
        video_content = {
            "course_id": course_id,
            "title": f"{section['title']} - Video Lesson",
            "type": "video",
            "content": f"<p>Video URL: https://example.com/videos/{course['level']}/{section['title'].replace(' ', '-').lower()}</p>",
            "order": order
        }
        db.course_content.insert_one(video_content)
        order += 1
        
        # Add practice exercise
        exercise_content = {
            "course_id": course_id,
            "title": f"{section['title']} - Practice Exercise",
            "type": "exercise",
            "content": f"<p>Complete the following exercises to practice {section['title'].lower()}:</p><ul><li>Exercise 1: Basic implementation</li><li>Exercise 2: Problem solving</li><li>Exercise 3: Advanced application</li></ul>",
            "order": order
        }
        db.course_content.insert_one(exercise_content)
        order += 1
        
        # Add quiz content reference (linked to the quiz IDs in the course structure)
        for quiz in section["quizzes"]:
            quiz_content = {
                "course_id": course_id,
                "title": quiz["title"],
                "type": "quiz",
                "content": f"<p>This quiz will test your knowledge of {section['title'].lower()}. Good luck!</p>",
                "order": order,
                "quiz_id": quiz["id"]
            }
            db.course_content.insert_one(quiz_content)
            order += 1

print("Course creation completed successfully!")

# Verify data
course_count = db.courses.count_documents({})
content_count = db.course_content.count_documents({})
print(f"Total courses created: {course_count}")
print(f"Total content items created: {content_count}")


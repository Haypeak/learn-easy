from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://hughesneal88:u9nkwE2XKnbvA1VM@eam-cluster0.urstk.mongodb.net/Learn_Easy?retryWrites=true&w=majority")
client = MongoClient(MONGO_URI)
db = client["Learn_Easy"]

def generate_quiz_id():
    """Generate a unique quiz ID"""
    return str(uuid.uuid4())

# Define courses
courses = [
    # ======= INFORMATION TECHNOLOGY COURSES =======
    {
        "title": "Introduction to Cybersecurity",
        "description": "Learn the fundamentals of cybersecurity, including threat identification, security principles, and basic defensive techniques.",
        "level": "beginner",
        "topics": ["Cybersecurity", "Network Security", "Information Security", "Security Fundamentals"],
        "created_at": datetime.now(timezone.utc),
        "author": "Dr. Emily Chen",
        "content": "<p>This comprehensive course introduces you to the world of cybersecurity and provides essential knowledge for protecting digital assets.</p>",
        "category": "Information Technology",
        "structure": {
            "sections": [
                {
                    "title": "Cybersecurity Fundamentals",
                    "description": "Learn about core cybersecurity concepts, common threats, and security principles.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Cybersecurity Basics Quiz"
                        }
                    ]
                },
                {
                    "title": "Network Security",
                    "description": "Understand network vulnerabilities, security protocols, and defensive mechanisms.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Network Security Quiz"
                        }
                    ]
                },
                {
                    "title": "Security Risk Assessment",
                    "description": "Learn how to identify, analyze, and prioritize security risks.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Risk Assessment Quiz"
                        }
                    ]
                },
                {
                    "title": "Security Best Practices",
                    "description": "Explore industry-standard security practices and implementation strategies.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Security Practices Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Database Management Systems",
        "description": "Explore database design, implementation, and administration with focus on relational and NoSQL databases.",
        "level": "intermediate",
        "topics": ["Databases", "SQL", "NoSQL", "Data Modeling", "Database Administration"],
        "created_at": datetime.utcnow(),
        "author": "Prof. James Wilson",
        "content": "<p>Master the art of designing, implementing, and managing databases for optimal performance and data integrity.</p>",
        "category": "Information Technology",
        "structure": {
            "sections": [
                {
                    "title": "Database Design Principles",
                    "description": "Learn about data modeling, normalization, and database design methodologies.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Database Design Quiz"
                        }
                    ]
                },
                {
                    "title": "SQL Fundamentals",
                    "description": "Master SQL queries, data manipulation, and transaction management.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "SQL Fundamentals Quiz"
                        }
                    ]
                },
                {
                    "title": "NoSQL Database Systems",
                    "description": "Explore document-oriented, key-value, and graph databases.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "NoSQL Databases Quiz"
                        }
                    ]
                },
                {
                    "title": "Database Administration",
                    "description": "Learn backup strategies, performance tuning, and security implementation.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Database Administration Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Cloud Computing Fundamentals",
        "description": "Understand cloud service models, deployment strategies, and leading cloud platforms.",
        "level": "beginner",
        "topics": ["Cloud Computing", "IaaS", "PaaS", "SaaS", "Cloud Deployment"],
        "created_at": datetime.utcnow(),
        "author": "Dr. Michael Roberts",
        "content": "<p>Dive into the world of cloud computing and learn how businesses are leveraging cloud technologies for scalability and efficiency.</p>",
        "category": "Information Technology",
        "structure": {
            "sections": [
                {
                    "title": "Introduction to Cloud Computing",
                    "description": "Learn about cloud service models, benefits, and challenges.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Cloud Computing Basics Quiz"
                        }
                    ]
                },
                {
                    "title": "Cloud Service Models",
                    "description": "Understand IaaS, PaaS, SaaS, and other service models.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Cloud Services Quiz"
                        }
                    ]
                },
                {
                    "title": "Major Cloud Platforms",
                    "description": "Explore AWS, Azure, Google Cloud, and other major providers.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Cloud Platforms Quiz"
                        }
                    ]
                },
                {
                    "title": "Cloud Security",
                    "description": "Learn about security considerations and best practices for cloud environments.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Cloud Security Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Network Administration Basics",
        "description": "Learn practical skills for managing and troubleshooting computer networks.",
        "level": "beginner",
        "topics": ["Networking", "TCP/IP", "Network Protocols", "Network Management"],
        "created_at": datetime.utcnow(),
        "author": "Prof. Sarah Martinez",
        "content": "<p>Develop essential skills for managing network infrastructure, implementing security, and resolving connectivity issues.</p>",
        "category": "Information Technology",
        "structure": {
            "sections": [
                {
                    "title": "Network Fundamentals",
                    "description": "Understand networking concepts, topologies, and the OSI model.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Network Fundamentals Quiz"
                        }
                    ]
                },
                {
                    "title": "IP Addressing and Subnetting",
                    "description": "Master IP addressing schemes, subnetting, and DHCP management.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "IP Addressing Quiz"
                        }
                    ]
                },
                {
                    "title": "Network Infrastructure",
                    "description": "Learn about routers, switches, firewalls, and other network devices.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Network Infrastructure Quiz"
                        }
                    ]
                },
                {
                    "title": "Network Troubleshooting",
                    "description": "Develop skills for diagnosing and resolving common network issues.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Network Troubleshooting Quiz"
                        }
                    ]
                }
            ]
        }
    },
    
    # ======= MATHEMATICS COURSES =======
    {
        "title": "Calculus I",
        "description": "Master the fundamentals of differential calculus, including limits, derivatives, and applications.",
        "level": "intermediate",
        "topics": ["Calculus", "Limits", "Derivatives", "Applications of Derivatives"],
        "created_at": datetime.utcnow(),
        "author": "Dr. Rebecca Thompson",
        "content": "<p>Explore the beautiful world of calculus and learn powerful mathematical tools for analyzing change and motion.</p>",
        "category": "Mathematics",
        "structure": {
            "sections": [
                {
                    "title": "Limits and Continuity",
                    "description": "Understand the concept of limits and continuous functions.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Limits Quiz"
                        }
                    ]
                },
                {
                    "title": "Derivatives and Differentiation",
                    "description": "Learn techniques for finding derivatives and understanding their meaning.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Derivatives Quiz"
                        }
                    ]
                },
                {
                    "title": "Applications of Derivatives",
                    "description": "Apply derivatives to rate of change, optimization, and related rates problems.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Derivative Applications Quiz"
                        }
                    ]
                },
                {
                    "title": "Curve Sketching",
                    "description": "Use differential calculus to analyze and graph functions.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Curve Sketching Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Linear Algebra",
        "description": "Study vector spaces, linear transformations, matrices, and their applications.",
        "level": "intermediate",
        "topics": ["Linear Algebra", "Vectors", "Matrices", "Linear Transformations", "Eigenvalues"],
        "created_at": datetime.utcnow(),
        "author": "Prof. David Chang",
        "content": "<p>Develop a strong foundation in linear algebra, a fundamental mathematical discipline with applications in data science, physics, and engineering.</p>",
        "category": "Mathematics",
        "structure": {
            "sections": [
                {
                    "title": "Vectors and Vector Spaces",
                    "description": "Learn about vectors, vector operations, and vector space properties.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Vectors Quiz"
                        }
                    ]
                },
                {
                    "title": "Matrices and Matrix Operations",
                    "description": "Master matrix algebra, determinants, and matrix properties.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Matrices Quiz"
                        }
                    ]
                },
                {
                    "title": "Linear Transformations",
                    "description": "Understand how matrices represent transformations in space.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Linear Transformations Quiz"
                        }
                    ]
                },
                {
                    "title": "Eigenvalues and Eigenvectors",
                    "description": "Explore eigenvalues, eigenvectors, and their applications.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Eigenvalues Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Statistics and Probability",
        "description": "Learn statistical methods and probability theory for data analysis and decision making.",
        "level": "intermediate",
        "topics": ["Statistics", "Probability", "Data Analysis", "Hypothesis Testing", "Regression"],
        "created_at": datetime.utcnow(),
        "author": "Dr. Lisa Rodriguez",
        "content": "<p>Develop statistical thinking and learn practical methods for analyzing data, testing hypotheses, and making data-driven decisions.</p>",
        "category": "Mathematics",
        "structure": {
            "sections": [
                {
                    "title": "Descriptive Statistics",
                    "description": "Learn methods for summarizing and visualizing data.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Descriptive Statistics Quiz"
                        }
                    ]
                },
                {
                    "title": "Probability Theory",
                    "description": "Understand probability concepts, random variables, and distributions.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Probability Quiz"
                        }
                    ]
                },
                {
                    "title": "Statistical Inference",
                    "description": "Master confidence intervals, hypothesis testing, and p-values.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Statistical Inference Quiz"
                        }
                    ]
                },
                {
                    "title": "Regression Analysis",
                    "description": "Learn linear regression, correlation, and predictive modeling.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Regression Analysis Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Discrete Mathematics",
        "description": "Explore mathematical structures that are fundamentally discrete rather than continuous.",
        "level": "intermediate",
        "topics": ["Discrete Math", "Logic", "Set Theory", "Combinatorics", "Graph Theory"],
        "created_at": datetime.utcnow(),
        "author": "Prof. Thomas Wright",
        "content": "<p>Dive into the mathematics of countable structures with applications in computer science, cryptography, and information theory.</p>",
        "category": "Mathematics",
        "structure": {
            "sections": [
                {
                    "title": "Logic and Proofs",
                    "description": "Learn propositional and predicate logic, and proof techniques.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Logic and Proofs Quiz"
                        }
                    ]
                },
                {
                    "title": "Set Theory and Relations",
                    "description": "Understand sets, functions, relations, and their properties.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Set Theory Quiz"
                        }
                    ]
                },
                {
                    "title": "Combinatorics",
                    "description": "Study counting, arrangement, and selection techniques.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Combinatorics Quiz"
                        }
                    ]
                },
                {
                    "title": "Graph Theory",
                    "description": "Explore graphs, trees, networks, and their applications.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Graph Theory Quiz"
                        }
                    ]
                }
            ]
        }
    },
    
    # ======= LANGUAGE ARTS COURSES =======
    {
        "title": "Creative Writing",
        "description": "Develop your creative writing skills across multiple genres including fiction, poetry, and creative non-fiction.",
        "level": "beginner",
        "topics": ["Fiction Writing", "Poetry", "Creative Non-Fiction", "Storytelling", "Narrative Techniques"],
        "created_at": datetime.utcnow(),
        "author": "Prof. Emily Anderson",
        "content": "<p>Express yourself through writing and unlock your creativity in this engaging and supportive course.</p>",
        "category": "Language Arts",
        "structure": {
            "sections": [
                {
                    "title": "Elements of Fiction",
                    "description": "Learn about character development, plot structure, setting, and point of view.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Fiction Elements Quiz"
                        }
                    ]
                },
                {
                    "title": "Poetic Forms and Techniques",
                    "description": "Explore different poetic forms, rhythms, and literary devices.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Poetry Techniques Quiz"
                        }
                    ]
                },
                {
                    "title": "Creative Non-Fiction",
                    "description": "Discover how to craft engaging personal essays, memoirs, and narrative journalism.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Creative Non-Fiction Quiz"
                        }
                    ]
                },
                {
                    "title": "Narrative Voice and Style",
                    "description": "Develop your unique writing voice and stylistic approach.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Writing Style Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Business Communication",
        "description": "Master essential communication skills for professional environments, including writing, presenting, and interpersonal communication.",
        "level": "intermediate",
        "topics": ["Business Writing", "Professional Communication", "Presentation Skills", "Email Etiquette"],
        "created_at": datetime.utcnow(),
        "author": "Dr. Robert Keller",
        "content": "<p>Enhance your professional communication skills to advance your career and effectively navigate workplace interactions.</p>",
        "category": "Language Arts",
        "structure": {
            "sections": [
                {
                    "title": "Business Writing Essentials",
                    "description": "Learn to craft clear, concise, and effective business documents.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Business Writing Quiz"
                        }
                    ]
                },
                {
                    "title": "Professional Email Communication",
                    "description": "Master the art of writing professional emails and managing email interactions.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Email Communication Quiz"
                        }
                    ]
                },
                {
                    "title": "Presentation Skills",
                    "description": "Develop techniques for creating and delivering impactful presentations.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Presentation Skills Quiz"
                        }
                    ]
                },
                {
                    "title": "Interpersonal Communication",
                    "description": "Improve your ability to communicate effectively in various professional contexts.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Interpersonal Communication Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "Public Speaking",
        "description": "Develop confidence and skill in public speaking for academic, professional, and social contexts.",
        "level": "beginner",
        "topics": ["Speech Preparation", "Delivery Techniques", "Audience Analysis", "Persuasive Speaking"],
        "created_at": datetime.utcnow(),
        "author": "Prof. Michelle Garcia",
        "content": "<p>Overcome your fear of public speaking and learn to captivate audiences with powerful, persuasive presentations.</p>",
        "category": "Language Arts",
        "structure": {
            "sections": [
                {
                    "title": "Speech Structure and Organization",
                    "description": "Learn to structure speeches for maximum impact and clarity.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Speech Structure Quiz"
                        }
                    ]
                },
                {
                    "title": "Delivery and Body Language",
                    "description": "Master the art of effective delivery, including voice modulation and body language.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Speech Delivery Quiz"
                        }
                    ]
                },
                {
                    "title": "Persuasive Speaking",
                    "description": "Develop techniques for crafting and delivering persuasive arguments.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Persuasive Speaking Quiz"
                        }
                    ]
                },
                {
                    "title": "Speaking in Different Contexts",
                    "description": "Adapt your speaking style for various situations and audiences.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Contextual Speaking Quiz"
                        }
                    ]
                }
            ]
        }
    },
    {
        "title": "English Literature Fundamentals",
        "description": "Explore major literary movements, authors, and works from various periods of English literature.",
        "level": "intermediate",
        "topics": ["Literary Analysis", "Poetry", "Prose", "Drama", "Literary Criticism"],
        "created_at": datetime.utcnow(),
        "author": "Dr. Sophia Williams",
        "content": "<p>Develop a deeper appreciation for English literature through close readings, historical context, and critical analysis.</p>",
        "category": "Language Arts",
        "structure": {
            "sections": [
                {
                    "title": "Introduction to Literary Analysis",
                    "description": "Learn essential concepts and methods for analyzing literary texts.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Literary Analysis Quiz"
                        }
                    ]
                },
                {
                    "title": "Poetry Through the Ages",
                    "description": "Explore poetic traditions from different literary periods.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Poetry Analysis Quiz"
                        }
                    ]
                },
                {
                    "title": "Evolution of the Novel",
                    "description": "Trace the development of the novel from its origins to contemporary forms.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Novel Analysis Quiz"
                        }
                    ]
                },
                {
                    "title": "Dramatic Literature",
                    "description": "Study major dramatic works and theatrical traditions in English literature.",
                    "quizzes": [
                        {
                            "id": generate_quiz_id(),
                            "title": "Drama Analysis Quiz"
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

# Count courses by category
it_courses = db.courses.count_documents({"category": "Information Technology"})
math_courses = db.courses.count_documents({"category": "Mathematics"})
language_courses = db.courses.count_documents({"category": "Language Arts"})

print(f"Total courses created: {course_count}")
print(f"Total content items created: {content_count}")
print(f"Information Technology courses: {it_courses}")
print(f"Mathematics courses: {math_courses}")
print(f"Language Arts courses: {language_courses}")

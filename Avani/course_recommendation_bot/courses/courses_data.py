# courses_data.py

course_catalog = [
    {
        "id": "DS001",
        "title": "Introduction to Data Science",
        "category": "Data Science",
        "level": "Beginner",
        "description": "Learn the fundamentals of data science, including data manipulation, visualization, and basic machine learning concepts.",
        "skills_gained": ["Python", "Pandas", "Matplotlib", "Basic ML"],
        "duration": "4 weeks",
        "prerequisites": "None"
    },
    {
        "id": "ML002",
        "title": "Machine Learning Fundamentals",
        "category": "Data Science",
        "level": "Intermediate",
        "description": "Dive deeper into machine learning algorithms, model evaluation, and practical applications. Covers supervised and unsupervised learning.",
        "skills_gained": ["Scikit-learn", "TensorFlow/PyTorch", "Model Evaluation"],
        "duration": "8 weeks",
        "prerequisites": "Introduction to Data Science or equivalent"
    },
    {
        "id": "WEB003",
        "title": "Full-Stack Web Development",
        "category": "Web Development",
        "level": "Intermediate",
        "description": "Build dynamic web applications from front-end to back-end using modern frameworks. Covers React, Node.js, and databases.",
        "skills_gained": ["HTML", "CSS", "JavaScript", "React", "Node.js", "MongoDB"],
        "duration": "12 weeks",
        "prerequisites": "Basic programming knowledge"
    },
    {
        "id": "AI004",
        "title": "Generative AI with watsonx.ai",
        "category": "Artificial Intelligence",
        "level": "Advanced",
        "description": "Explore the concepts and applications of generative AI using IBM watsonx.ai. Learn prompt engineering, foundation models, and RAG.",
        "skills_gained": ["Prompt Engineering", "Foundation Models", "RAG", "watsonx.ai"],
        "duration": "6 weeks",
        "prerequisites": "Machine Learning Fundamentals or strong AI background"
    },
    {
        "id": "CLOUD005",
        "title": "Cloud Computing Basics (IBM Cloud)",
        "category": "Cloud Computing",
        "level": "Beginner",
        "description": "Understand core cloud concepts and learn to deploy applications on IBM Cloud. Covers IaaS, PaaS, and SaaS.",
        "skills_gained": ["Cloud Concepts", "IBM Cloud Services", "Deployment"],
        "duration": "3 weeks",
        "prerequisites": "None"
    },
    {
        "id": "CYBER006",
        "title": "Cybersecurity Essentials",
        "category": "Cybersecurity",
        "level": "Beginner",
        "description": "An introduction to fundamental cybersecurity principles, threats, and defense mechanisms.",
        "skills_gained": ["Network Security", "Threat Detection", "Cryptography"],
        "duration": "5 weeks",
        "prerequisites": "None"
    },
    {
        "id": "DATA007",
        "title": "SQL for Data Analysis",
        "category": "Data Science",
        "level": "Beginner",
        "description": "Master SQL for querying and managing relational databases, essential for data analysis.",
        "skills_gained": ["SQL", "Database Management", "Data Querying"],
        "duration": "3 weeks",
        "prerequisites": "None"
    },
    {
        "id": "PYTHON008",
        "title": "Python Programming for Beginners",
        "category": "Programming",
        "level": "Beginner",
        "description": "Learn the basics of Python programming, from variables to functions and data structures.",
        "skills_gained": ["Python Syntax", "Data Structures", "Functions"],
        "duration": "6 weeks",
        "prerequisites": "None"
    }
]

def search_courses(query, criteria):
    """
    Simulates searching the course catalog based on query and criteria.
    In a real RAG system, this would involve embedding the query and
    performing a vector search on embedded course descriptions.
    """
    results = []
    query_lower = query.lower()

    for course in course_catalog:
        match = False
        # Simple keyword matching for demonstration
        if "interest" in criteria and any(q in course["category"].lower() for q in query_lower.split()):
            match = True
        if "level" in criteria and query_lower in course["level"].lower():
            match = True
        if "skills" in criteria and any(q in skill.lower() for q in query_lower.split() for skill in course["skills_gained"]):
            match = True
        if query_lower in course["title"].lower() or query_lower in course["description"].lower():
            match = True

        if match:
            results.append(course)
    return results

def format_course_info(course):
    """Formats a single course dictionary into a readable string."""
    return (
        f"**{course['title']}** ({course['id']})\n"
        f"Category: {course['category']}\n"
        f"Level: {course['level']}\n"
        f"Duration: {course['duration']}\n"
        f"Description: {course['description']}\n"
        f"Skills Gained: {', '.join(course['skills_gained'])}\n"
        f"Prerequisites: {course['prerequisites']}\n"
    )
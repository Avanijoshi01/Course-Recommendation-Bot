from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import csv
from pathlib import Path
from .prompt_api import get_course_recommendation
from .apitotoken import get_iam_token
from django.conf import settings


def load_relevant_courses(user_interest):
    try:
        # Map keywords to course tags
        tag_map = {
            "data": "tech", "ai": "tech", "cloud": "tech", "software": "tech",
            "backend": "tech", "api": "tech", "finance": "finance", "account": "finance",
            "stock": "finance", "business": "business", "startup": "business",
            "entrepreneur": "business", "electrical": "electrical", "circuit": "electrical",
            "signal": "electrical", "mechanical": "mechanical", "thermal": "mechanical", "cad": "mechanical"
        }

        matched_tag = None
        for keyword, tag in tag_map.items():
            if keyword.lower() in user_interest.lower():
                matched_tag = tag
                break

        course_file = Path(__file__).resolve().parent / "course_recommendation_data.csv"
        course_list = []

        with open(course_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if matched_tag is None or row['Tags'].lower() == matched_tag:
                    formatted = (
                        f"Title: {row['Title']}\n"
                        f"Course ID: {row['Course ID']}\n"
                        f"Description: {row['Description']}\n"
                        f"---"
                    )
                    course_list.append(formatted)

        return "\n".join(course_list[:15])

    except Exception as e:
        print("❌ Failed to load or filter CSV:", e)
        return ""


@csrf_exempt
def recommend_course(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_interest = data.get("user_interest", "").strip()

            if not user_interest:
                return JsonResponse({"error": "User interest is required."}, status=400)

            # Get filtered courses
            available_courses = load_relevant_courses(user_interest)

            # Few-shot example + prompt
            prompt_text = f"""
            You are a helpful course recommendation assistant. Based on the user's interests and the following available courses, suggest the **top 5 most relevant courses** in a clean numbered bullet format.

            Each recommendation must include:
            - 🧠 Course Title
            - Course ID in parentheses
            - One-line course description

            ✅ Output must contain exactly 5 numbered courses.
            ✅ Do not repeat.
            ✅ Do not exceed 5 items.

            Example:
            Input:
            Title: Machine Learning Basics
            Course ID: DS101
            Description: Learn the fundamentals of machine learning including regression and classification.

            Title: Python for Data Science
            Course ID: PY102
            Description: A beginner-friendly course to use Python for data analysis and machine learning.

Output:
1. 🧠 Machine Learning Basics (DS101)  
Learn the fundamentals of machine learning including regression and classification.

2. 🧠 Python for Data Science (PY102)  
A beginner-friendly course to use Python for data analysis and machine learning.

Now respond for:

User Interests: {user_interest}
Available Courses:
{available_courses}

            Output:
            """


            # Get access token
            token = get_iam_token(settings.WATSONX_API_KEY)

            # Get recommendation
            raw_response = get_course_recommendation(prompt_text, token)

            # Format output
            formatted = raw_response.strip().replace("\n", "<br>")

            return JsonResponse({"recommendation": formatted})

        except Exception as e:
            print("❌ ERROR in /api/recommend/:", str(e))
            traceback.print_exc()
            return JsonResponse({"error": "Internal Server Error", "detail": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


def index(request):
    return render(request, 'index.html')

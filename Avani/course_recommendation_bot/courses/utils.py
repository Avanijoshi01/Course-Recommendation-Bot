# recommender/utils.py

import pandas as pd

# Load only once
df = pd.read_csv("courses/course_data_300.csv")

def find_relevant_courses(user_interest, max_results=5):
    # Basic filtering based on tags or title/description
    filtered = df[df.apply(
        lambda row: user_interest.lower() in row["Tags"].lower() 
        or user_interest.lower() in row["Title"].lower() 
        or user_interest.lower() in row["Description"].lower(), 
        axis=1
    )]

    if filtered.empty:
        return "No specific matching courses found."

    course_list = ""
    for i, row in filtered.head(max_results).iterrows():
        course_list += f"Course ID: {row['Course ID']}, Title: {row['Title']}, Description: {row['Description']}\n"
    
    return course_list.strip()
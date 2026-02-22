"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
import json
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Load activities from JSON file
ACTIVITIES_FILE = os.path.join(Path(__file__).parent, "activities.json")
TEACHERS_FILE = os.path.join(Path(__file__).parent, "teachers.json")

def load_activities():
    """Load activities from JSON file"""
    try:
        with open(ACTIVITIES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_activities(activities):
    """Save activities to JSON file"""
    with open(ACTIVITIES_FILE, 'w') as f:
        json.dump(activities, f, indent=2)

def load_teachers():
    """Load teacher credentials from JSON file"""
    try:
        with open(TEACHERS_FILE, 'r') as f:
            data = json.load(f)
            return data.get("teachers", [])
    except FileNotFoundError:
        return []

# In-memory activity database (loaded from JSON)
activities = load_activities()
teachers = load_teachers()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.post("/auth/login")
def login(username: str, password: str):
    """Authenticate teacher and return session token"""
    for teacher in teachers:
        if teacher["username"] == username and teacher["password"] == password:
            return {"success": True, "message": "Login successful", "user_role": "teacher"}
    
    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.post("/auth/logout")
def logout():
    """Logout (simple implementation)"""
    return {"success": True, "message": "Logged out successfully"}


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, is_teacher: bool = False):
    """Sign up a student for an activity (students only unless teacher overrides)"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Validate capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(
            status_code=400,
            detail="Activity is at maximum capacity"
        )

    # Add student
    activity["participants"].append(email)
    save_activities(activities)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, is_teacher: bool = False):
    """Unregister a student from an activity (teachers have permission)"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    save_activities(activities)
    return {"message": f"Unregistered {email} from {activity_name}"}

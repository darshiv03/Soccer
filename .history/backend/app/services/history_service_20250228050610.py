import json
import os
import uuid

HISTORY_FILE = "history.json"
SESSION_TRACKER_FILE = "session_tracker.json"

def reset_history_if_new_session():
    """Deletes history.json if the user starts a new session."""
    session_id = str(uuid.uuid4())  # Generate a unique session ID

    # Check if session tracker exists
    if os.path.exists(SESSION_TRACKER_FILE):
        with open(SESSION_TRACKER_FILE, "r") as file:
            try:
                last_session = json.load(file).get("session_id", "")
            except json.JSONDecodeError:
                last_session = ""
    else:
        last_session = ""

    # If session ID changed (new session), clear history
    if last_session != session_id:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
            print("History cleared due to new session.")
        with open(SESSION_TRACKER_FILE, "w") as file:
            json.dump({"session_id": session_id}, file)

    # Ensure history.json exists (avoid missing file issues)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as file:
            json.dump([], file)

def save_to_history(query, video_filename, num_clips=1):
    """ Saves query, result, and video link to history.json """
    reset_history_if_new_session()  # Ensure history resets on a new session

    history_entry = {
        "query": query,
        "video_url": f"/static/generated_videos/{video_filename}",
        "num_clips": num_clips
    }

    # Load existing history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            try:
                history = json.load(file)
            except json.JSONDecodeError:
                history = []
    else:
        history = []

    # Append new entry & save
    history.append(history_entry)
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

def get_history():
    """ Fetches the stored video generation history """
    reset_history_if_new_session()  # Ensure history resets on a new session

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

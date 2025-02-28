import json
import os

HISTORY_FILE = "history.json"

def save_to_history(query, video_filename, num_clips=1):
    """ Saves query, result, and video link to history.json """
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
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

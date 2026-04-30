import json
import os

FILE_NAME = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_score(name, score):
    data = load_leaderboard()
    data.append({"name": name, "score": score})
    # Сортируем: сначала те, у кого больше очков
    data = sorted(data, key=lambda x: x['score'], reverse=True)
    # Оставляем только топ-10
    data = data[:10]
    
    with open(FILE_NAME, 'w') as f:
        json.dump(data, f, indent=4)
SETTINGS_FILE = "settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"sound": True, "difficulty": 1, "car_color": "red"}

def save_settings(data):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(data, f, indent=4)
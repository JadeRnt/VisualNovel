import json
import os

SAVE_PATH = "saves/savegame.json"

class Character:
    def __init__(self, name, color, photo_path):
        self.name = name
        self.friendship = 50
        self.color = color
        self.current_scene = "intro"
        self.photo_path = photo_path

    def to_dict(self):
        return {
            "friendship": self.friendship,
            "current_scene": self.current_scene
        }

    def from_dict(self, data):
        self.friendship = data["friendship"]
        self.current_scene = data["current_scene"]


class VisualNovelGame:
    def __init__(self):
        self.characters = {
            "Alex": Character("Alex", (0.6, 0.8, 1, 1), "assets/photo_alex.png"),
            "Lisa": Character("Lisa", (1, 0.7, 0.9, 1), "assets/photo_lisa.png")
        }
        self.active_character = None
        self.load()

    def save(self):
        data = {
            "active_character": self.active_character,
            "characters": {name: char.to_dict() for name, char in self.characters.items()}
        }
        os.makedirs("saves", exist_ok=True)
        with open(SAVE_PATH, "w") as f:
            json.dump(data, f)

    def load(self):
        if not os.path.exists(SAVE_PATH):
            return
        with open(SAVE_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                return
            data = json.loads(content)
            self.active_character = data.get("active_character")
            for name, char_data in data["characters"].items():
                self.characters[name].from_dict(char_data)

from csv import DictReader
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Could not find songs file: {csv_path}")

    songs: List[Dict] = []
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = DictReader(csv_file)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences.
    Returns (score, explanation).
    """
    score = 0.0
    explanation_parts = []

    if str(user_prefs.get("genre", "")).strip().lower() == str(song.get("genre", "")).strip().lower():
        score += 2.0
        explanation_parts.append("genre match (+2.0)")

    if str(user_prefs.get("mood", "")).strip().lower() == str(song.get("mood", "")).strip().lower():
        score += 1.0
        explanation_parts.append("mood match (+1.0)")

    target_energy = float(user_prefs.get("energy", 0.0))
    song_energy = float(song.get("energy", 0.0))
    energy_points = max(0.0, 1.0 - abs(song_energy - target_energy))
    score += energy_points
    explanation_parts.append(f"energy closeness (+{energy_points:.2f})")

    return score, "; ".join(explanation_parts)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda item: -item[1])
    return scored[:k]

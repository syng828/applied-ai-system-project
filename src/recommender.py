from csv import DictReader
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

MAX_SCORE = 3.0
LOW_CONFIDENCE_THRESHOLD = 0.55
LOW_MARGIN_THRESHOLD = 0.05

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
        scored: List[Tuple[Song, float]] = []
        for song in self.songs:
            score, _ = self._score_song(user, song)
            scored.append((song, score))

        scored.sort(key=lambda item: -item[1])
        diversified = self._apply_artist_diversity(scored, k)

        top_score = scored[0][1] if scored else 0.0
        second_score = scored[1][1] if len(scored) > 1 else 0.0
        confidence = top_score / MAX_SCORE if MAX_SCORE > 0 else 0.0
        margin = top_score - second_score
        low_confidence = confidence < LOW_CONFIDENCE_THRESHOLD or margin < LOW_MARGIN_THRESHOLD

        if low_confidence:
            return self._genre_diverse_fallback(scored, k)
        return [song for song, _ in diversified]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, parts = self._score_song(user, song)
        return f"score={score:.2f}; " + "; ".join(parts)

    def _score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        explanation_parts: List[str] = []

        if user.favorite_genre.strip().lower() == song.genre.strip().lower():
            score += 1.0
            explanation_parts.append("genre match (+1.0)")

        if user.favorite_mood.strip().lower() == song.mood.strip().lower():
            score += 1.0
            explanation_parts.append("mood match (+1.0)")

        energy_points = max(0.0, 1.0 - abs(song.energy - user.target_energy))
        score += energy_points
        explanation_parts.append(f"energy closeness (+{energy_points:.2f})")

        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 0.2
            explanation_parts.append("acoustic bonus (+0.2)")

        return score, explanation_parts

    def _apply_artist_diversity(self, scored: List[Tuple[Song, float]], k: int) -> List[Tuple[Song, float]]:
        selected: List[Tuple[Song, float]] = []
        seen_artists = set()

        for song, score in scored:
            if song.artist not in seen_artists:
                selected.append((song, score))
                seen_artists.add(song.artist)
            if len(selected) == k:
                return selected

        for song, score in scored:
            if len(selected) == k:
                break
            if (song, score) not in selected:
                selected.append((song, score))

        return selected

    def _genre_diverse_fallback(self, scored: List[Tuple[Song, float]], k: int) -> List[Song]:
        by_genre: Dict[str, List[Song]] = {}
        for song, _ in scored:
            by_genre.setdefault(song.genre.lower(), []).append(song)

        fallback: List[Song] = []
        while len(fallback) < k:
            added_in_round = False
            for songs_in_genre in by_genre.values():
                if not songs_in_genre:
                    continue
                fallback.append(songs_in_genre.pop(0))
                added_in_round = True
                if len(fallback) == k:
                    break
            if not added_in_round:
                break

        return fallback

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
        score += 1.0
        explanation_parts.append("genre match (+1.0)")

    if str(user_prefs.get("mood", "")).strip().lower() == str(song.get("mood", "")).strip().lower():
        score += 1.0
        explanation_parts.append("mood match (+1.0)")

    target_energy = float(user_prefs.get("energy", 0.0))
    song_energy = float(song.get("energy", 0.0))
    energy_points = max(0.0, 1.0 - abs(song_energy - target_energy))
    score += energy_points
    explanation_parts.append(f"energy closeness (+{energy_points:.2f})")

    if bool(user_prefs.get("likes_acoustic", False)) and float(song.get("acousticness", 0.0)) >= 0.6:
        score += 0.2
        explanation_parts.append("acoustic bonus (+0.2)")

    return score, "; ".join(explanation_parts)


def _apply_artist_diversity_dict(scored: List[Tuple[Dict, float, str]], k: int) -> List[Tuple[Dict, float, str]]:
    selected: List[Tuple[Dict, float, str]] = []
    seen_artists = set()

    for item in scored:
        song, _, _ = item
        artist = str(song.get("artist", "")).strip().lower()
        if artist not in seen_artists:
            selected.append(item)
            seen_artists.add(artist)
        if len(selected) == k:
            return selected

    for item in scored:
        if len(selected) == k:
            break
        if item not in selected:
            selected.append(item)

    return selected


def _genre_diverse_fallback_dict(scored: List[Tuple[Dict, float, str]], k: int) -> List[Tuple[Dict, float, str]]:
    by_genre: Dict[str, List[Tuple[Dict, float, str]]] = {}
    for item in scored:
        song, _, _ = item
        genre = str(song.get("genre", "unknown")).strip().lower()
        by_genre.setdefault(genre, []).append(item)

    fallback: List[Tuple[Dict, float, str]] = []
    while len(fallback) < k:
        added_in_round = False
        for items_in_genre in by_genre.values():
            if not items_in_genre:
                continue
            fallback.append(items_in_genre.pop(0))
            added_in_round = True
            if len(fallback) == k:
                break
        if not added_in_round:
            break

    return fallback

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda item: -item[1])

    top_score = scored[0][1] if scored else 0.0
    second_score = scored[1][1] if len(scored) > 1 else 0.0
    run_confidence = top_score / MAX_SCORE if MAX_SCORE > 0 else 0.0
    run_margin = top_score - second_score
    low_confidence = run_confidence < LOW_CONFIDENCE_THRESHOLD or run_margin < LOW_MARGIN_THRESHOLD

    selected = _apply_artist_diversity_dict(scored, k)
    fallback_used = False
    if low_confidence:
        selected = _genre_diverse_fallback_dict(scored, k)
        fallback_used = True

    selected_with_reliability: List[Tuple[Dict, float, str]] = []
    for idx, (song, score, explanation) in enumerate(selected):
        next_score = selected[idx + 1][1] if idx + 1 < len(selected) else 0.0
        song_confidence = score / MAX_SCORE if MAX_SCORE > 0 else 0.0
        song_margin = score - next_score
        reliability_tag = (
            f"reliability: confidence={song_confidence:.2f}; "
            f"margin={song_margin:.2f}; fallback={'on' if fallback_used else 'off'}"
        )
        selected_with_reliability.append((song, score, f"{explanation}; {reliability_tag}"))

    return selected_with_reliability

import re
import pytest

from src.recommender import Song, UserProfile, Recommender, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_recommend_prefers_artist_diversity_in_top_k():
    songs = [
        Song(
            id=1,
            title="Pop One",
            artist="Artist A",
            genre="pop",
            mood="happy",
            energy=0.80,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Pop Two",
            artist="Artist A",
            genre="pop",
            mood="happy",
            energy=0.79,
            tempo_bpm=121,
            valence=0.88,
            danceability=0.81,
            acousticness=0.2,
        ),
        Song(
            id=3,
            title="Rock Side",
            artist="Artist B",
            genre="rock",
            mood="sad",
            energy=0.30,
            tempo_bpm=100,
            valence=0.4,
            danceability=0.5,
            acousticness=0.3,
        ),
    ]
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = Recommender(songs)

    results = rec.recommend(user, k=2)
    artists = {song.artist for song in results}

    assert len(results) == 2
    assert len(artists) == 2


def test_functional_recommender_adds_reliability_tag_and_can_fallback():
    songs = [
        {
            "id": 1,
            "title": "Track 1",
            "artist": "A1",
            "genre": "rock",
            "mood": "sad",
            "energy": 0.2,
            "tempo_bpm": 90,
            "valence": 0.2,
            "danceability": 0.3,
            "acousticness": 0.2,
        },
        {
            "id": 2,
            "title": "Track 2",
            "artist": "A2",
            "genre": "jazz",
            "mood": "relaxed",
            "energy": 0.3,
            "tempo_bpm": 95,
            "valence": 0.3,
            "danceability": 0.4,
            "acousticness": 0.7,
        },
    ]
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.95}

    results = recommend_songs(user_prefs, songs, k=2)

    assert len(results) == 2
    assert "reliability: confidence=" in results[0][2]
    assert "fallback=on" in results[0][2]


def test_functional_recommender_uses_per_song_margins():
    songs = [
        {
            "id": 1,
            "title": "Top Song",
            "artist": "A1",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.80,
            "tempo_bpm": 120,
            "valence": 0.8,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 2,
            "title": "Second Song",
            "artist": "A2",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.70,
            "tempo_bpm": 118,
            "valence": 0.7,
            "danceability": 0.7,
            "acousticness": 0.2,
        },
        {
            "id": 3,
            "title": "Third Song",
            "artist": "A3",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.65,
            "tempo_bpm": 116,
            "valence": 0.65,
            "danceability": 0.65,
            "acousticness": 0.2,
        },
    ]
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    results = recommend_songs(user_prefs, songs, k=3)

    margin_values = []
    for _, _, explanation in results:
        match = re.search(r"margin=([-0-9.]+)", explanation)
        assert match is not None
        margin_values.append(float(match.group(1)))

    assert margin_values[0] != margin_values[-1]


def test_recommenders_handle_empty_song_list():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = Recommender([])
    assert rec.recommend(user, k=5) == []

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    assert recommend_songs(user_prefs, [], k=5) == []


def test_functional_recommender_tie_keeps_input_order_and_uses_fallback():
    songs = [
        {
            "id": 1,
            "title": "Tie A",
            "artist": "Artist A",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 120,
            "valence": 0.8,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 2,
            "title": "Tie B",
            "artist": "Artist B",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "tempo_bpm": 121,
            "valence": 0.8,
            "danceability": 0.8,
            "acousticness": 0.2,
        },
        {
            "id": 3,
            "title": "Lower",
            "artist": "Artist C",
            "genre": "rock",
            "mood": "sad",
            "energy": 0.2,
            "tempo_bpm": 95,
            "valence": 0.2,
            "danceability": 0.3,
            "acousticness": 0.2,
        },
    ]
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    results = recommend_songs(user_prefs, songs, k=2)

    assert [song["id"] for song, _, _ in results] == [1, 3]
    assert "fallback=on" in results[0][2]


def test_functional_recommender_raises_on_malformed_numeric_fields():
    songs = [
        {
            "id": 1,
            "title": "Bad Energy",
            "artist": "A1",
            "genre": "pop",
            "mood": "happy",
            "energy": "not-a-number",
            "tempo_bpm": 120,
            "valence": 0.8,
            "danceability": 0.8,
            "acousticness": 0.2,
        }
    ]
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    with pytest.raises(ValueError):
        recommend_songs(user_prefs, songs, k=1)

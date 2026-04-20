"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs

def display_recommendations(recommendations: list) -> None:
    print("\n" + "=" * 40)
    print(f"  Top {len(recommendations)} Recommendations")
    print("=" * 40)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   : {explanation}")

def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print("User Preferences:", user_prefs)
    display_recommendations(recommendations)
    print("\n")

    user_prefs = {"genre": "rock", "mood": "sad", "energy": 0.3}
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print("User Preferences:", user_prefs)
    display_recommendations(recommendations)
    print("\n")

    user_prefs = {"genre": "jazz", "mood": "relaxed", "energy": 0.5}
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print("User Preferences:", user_prefs)
    display_recommendations(recommendations)
    print("\n")

    user_prefs = {"genre": "lofi", "mood": "intense", "energy": 0.9}
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print("User Preferences:", user_prefs)
    display_recommendations(recommendations)
    print("\n")


if __name__ == "__main__":
    main()

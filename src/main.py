"""
Command line runner for the Music Recommender Simulation.

Run: python -m src.main
"""

from src.recommender import load_songs, recommend_songs

PROFILES = [
    {
        "name": "High-energy pop party",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.85},
    },
    {
        "name": "Chill lofi desk session",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.38, "likes_acoustic": True},
    },
    {
        "name": "Deep intense rock",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    },
    {
        "name": "Edge case: moody but hyper-energetic",
        "prefs": {"genre": "synthwave", "mood": "moody", "energy": 0.95},
    },
]

EXPERIMENT_WEIGHTS = {
    "genre_match": 1.0,
    "mood_match": 1.0,
    "energy_scale": 3.0,
}


def print_recommendations(title: str, user_prefs: dict, songs: list, k: int = 5, weights=None) -> None:
    line = "=" * 72
    print(f"\n{line}\n{title}\n{line}")
    print(f"Preferences: {user_prefs}")
    if weights:
        print(f"Custom weights: {weights}")
    recs = recommend_songs(user_prefs, songs, k=k, weights=weights, diversify_by_artist=True)
    print(f"\nTop {k} recommendations:\n")
    for rank, (song, score, explanation) in enumerate(recs, start=1):
        artist = song.get("artist", "?")
        genre = song.get("genre", "?")
        mood = song.get("mood", "?")
        print(f"{rank}. {song['title']} - {artist}")
        print(f"   {genre} / {mood} | score {score:.2f}")
        print(f"   Because: {explanation}\n")


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        print_recommendations(profile["name"], profile["prefs"], songs, k=5)

    baseline = {"genre": "pop", "mood": "happy", "energy": 0.85}
    print_recommendations(
        "Experiment: halve genre weight + stronger energy scale (same profile as first)",
        baseline,
        songs,
        k=5,
        weights=EXPERIMENT_WEIGHTS,
    )


if __name__ == "__main__":
    main()

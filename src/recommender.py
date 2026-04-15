from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple

DEFAULT_SCORING_WEIGHTS: Dict[str, float] = {
    "genre_match": 2.0,
    "mood_match": 1.0,
    "energy_scale": 1.5,
    "acoustic_pref_scale": 0.35,
    "non_acoustic_lean_scale": 0.15,
}


@dataclass
class Song:
    """Represents a song and its attributes."""

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
    """Represents a user's taste preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _merge_weights(overrides: Optional[Dict[str, float]]) -> Dict[str, float]:
    merged = dict(DEFAULT_SCORING_WEIGHTS)
    if overrides:
        merged.update(overrides)
    return merged


def song_as_dict(song: Song) -> Dict:
    """Convert a Song dataclass to the dict shape used by score_song."""
    return asdict(song)


def user_prefs_from_profile(user: UserProfile) -> Dict:
    """Map UserProfile fields to the dict keys expected by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV; coerce numeric columns for scoring."""
    rows: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            row = dict(raw)
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            rows.append(row)
    print(f"Loaded songs: {len(rows)}")
    return rows


def score_song(
    user_prefs: Dict,
    song: Dict,
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[float, List[str]]:
    """Score one song against preferences; returns total score and reason strings."""
    w = _merge_weights(weights)
    reasons: List[str] = []
    total = 0.0

    user_genre = str(user_prefs.get("genre", "")).strip().lower()
    song_genre = str(song.get("genre", "")).strip().lower()
    if user_genre and song_genre and user_genre == song_genre:
        pts = w["genre_match"]
        total += pts
        reasons.append(f"genre match (+{pts:.1f})")

    user_mood = str(user_prefs.get("mood", "")).strip().lower()
    song_mood = str(song.get("mood", "")).strip().lower()
    if user_mood and song_mood and user_mood == song_mood:
        pts = w["mood_match"]
        total += pts
        reasons.append(f"mood match (+{pts:.1f})")

    user_energy = float(user_prefs.get("energy", 0.5))
    song_energy = float(song.get("energy", 0.0))
    gap = abs(song_energy - user_energy)
    energy_pts = w["energy_scale"] * max(0.0, 1.0 - gap)
    total += energy_pts
    reasons.append(f"energy closeness (+{energy_pts:.2f})")

    if "likes_acoustic" in user_prefs:
        ac = float(song.get("acousticness", 0.0))
        if user_prefs["likes_acoustic"]:
            ap = w["acoustic_pref_scale"] * ac
            total += ap
            reasons.append(f"acoustic preference (+{ap:.2f})")
        else:
            lean = w["non_acoustic_lean_scale"] * max(0.0, 1.0 - ac)
            total += lean
            reasons.append(f"non-acoustic lean (+{lean:.2f})")

    return total, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Optional[Dict[str, float]] = None,
    diversify_by_artist: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort descending, return top k with explanations."""
    ranked: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reason_list = score_song(user_prefs, song, weights=weights)
        explanation = "; ".join(reason_list) if reason_list else "no strong matches"
        ranked.append((song, score, explanation))
    ranked.sort(key=lambda item: item[1], reverse=True)

    if not diversify_by_artist:
        return ranked[:k]

    picked: List[Tuple[Dict, float, str]] = []
    seen_artists = set()
    for item in ranked:
        song = item[0]
        artist = str(song.get("artist", "")).strip().lower()
        if artist and artist in seen_artists:
            continue
        seen_artists.add(artist)
        picked.append(item)
        if len(picked) >= k:
            break
    return picked


class Recommender:
    """OOP wrapper that reuses the same scoring rules as score_song."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return up to k songs with highest scores for the given user."""
        prefs = user_prefs_from_profile(user)
        scored: List[Tuple[float, Song]] = []
        for song in self.songs:
            score, _ = score_song(prefs, song_as_dict(song))
            scored.append((score, song))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a single string of score reasons for one user-song pair."""
        prefs = user_prefs_from_profile(user)
        _, reasons = score_song(prefs, song_as_dict(song))
        return "; ".join(reasons) if reasons else "No strong match signals."

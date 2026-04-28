from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from src.recommender import load_songs, recommend_songs


@dataclass
class RetrievalItem:
    source: str
    text: str
    score: float


def _normalize(text: str) -> List[str]:
    return [t for t in "".join([c.lower() if c.isalnum() else " " for c in text]).split() if t]


def retrieve_context(question: str, notes_text: str, songs: List[Dict], top_n: int = 5) -> List[RetrievalItem]:
    q_tokens = set(_normalize(question))
    items: List[RetrievalItem] = []

    notes_tokens = _normalize(notes_text)
    notes_score = sum(1 for t in notes_tokens if t in q_tokens)
    if notes_score:
        items.append(RetrievalItem(source="data/notes.txt", text=notes_text.strip(), score=float(notes_score)))

    for song in songs:
        blob = f"{song.get('title','')} {song.get('artist','')} {song.get('genre','')} {song.get('mood','')}"
        s_tokens = _normalize(blob)
        s_score = sum(1 for t in s_tokens if t in q_tokens)
        if s_score:
            items.append(
                RetrievalItem(
                    source=f"song:{song.get('id','?')}",
                    text=blob.strip(),
                    score=float(s_score),
                )
            )

    items.sort(key=lambda x: x.score, reverse=True)
    return items[:top_n]


def parse_prefs_from_text(text: str) -> Dict:
    t = text.lower()
    prefs: Dict = {}

    for genre in ["pop", "lofi", "rock", "ambient", "jazz", "synthwave", "metal", "blues", "country", "classical", "reggae", "rap", "folk", "electronic", "indie pop"]:
        if genre in t:
            prefs["genre"] = genre
            break

    for mood in ["happy", "chill", "intense", "relaxed", "moody", "focused"]:
        if mood in t:
            prefs["mood"] = mood
            break

    for word, val in [("low energy", 0.3), ("chill", 0.35), ("medium energy", 0.6), ("high energy", 0.85), ("very high energy", 0.95)]:
        if word in t:
            prefs["energy"] = val
            break

    if "energy" not in prefs:
        prefs["energy"] = 0.6

    if "acoustic" in t:
        if "not acoustic" in t or "no acoustic" in t:
            prefs["likes_acoustic"] = False
        else:
            prefs["likes_acoustic"] = True

    return prefs


def _format_recs(recs: List[Tuple[Dict, float, str]]) -> str:
    lines: List[str] = []
    for i, (song, score, explanation) in enumerate(recs, start=1):
        lines.append(f"{i}. {song['title']} - {song.get('artist','?')} (score {score:.2f})")
        lines.append(f"   Because: {explanation}")
    return "\n".join(lines)


def generate_answer_with_openai(question: str, context: List[RetrievalItem], rec_text: str) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except Exception:
        return None

    client = OpenAI(api_key=api_key)
    context_text = "\n\n".join([f"[{c.source}] {c.text}" for c in context])

    prompt = (
        "You are a helpful assistant for a classroom music recommender demo.\n"
        "Use the retrieved context and the ranked list to answer.\n"
        "Be short and clear. No hype.\n\n"
        f"User question: {question}\n\n"
        f"Retrieved context:\n{context_text}\n\n"
        f"Ranked recommendations:\n{rec_text}\n\n"
        "Write: (1) a one paragraph answer, (2) then list the top songs exactly as shown.\n"
    )

    try:
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None


def answer_question(question: str, k: int = 5) -> str:
    songs = load_songs("data/songs.csv")
    try:
        with open("data/notes.txt", "r", encoding="utf-8") as f:
            notes_text = f.read()
    except FileNotFoundError:
        notes_text = ""

    prefs = parse_prefs_from_text(question)

    recs = recommend_songs(prefs, songs, k=k, diversify_by_artist=True)
    rec_text = _format_recs(recs)
    context = retrieve_context(question, notes_text, songs)

    llm_answer = generate_answer_with_openai(question, context, rec_text)
    if llm_answer:
        return llm_answer

    context_line = ", ".join([c.source for c in context]) if context else "none"
    return (
        "Here is what I picked based on your question. "
        f"I used the song sheet plus notes (retrieved sources: {context_line}).\n\n"
        + rec_text
    )


from __future__ import annotations

from src.ai_assistant import answer_question


CASES = [
    "Recommend chill lofi for studying, low energy, acoustic please",
    "I want intense rock for a workout, high energy, not acoustic",
    "Give me something moody and high energy, synthwave vibe",
]


def main() -> None:
    passed = 0
    for i, q in enumerate(CASES, start=1):
        out = answer_question(q, k=5)
        ok = ("Because:" in out) and ("1." in out) and ("score" in out)
        print("=" * 60)
        print(f"Case {i}: {q}")
        print("-" * 60)
        print(out)
        print("-" * 60)
        print("PASS" if ok else "FAIL")
        passed += 1 if ok else 0

    print("=" * 60)
    print(f"Summary: {passed} out of {len(CASES)} passed")


if __name__ == "__main__":
    main()


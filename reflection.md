# Reflection: comparing user profiles

These are quick notes comparing the fake listeners in src/main.py. Each bit is just what I expected to change in the top five and why, given the scoring rules.

---

## High-energy pop party vs Chill lofi desk session

Pop with happy mood lines up with bright pop tracks, so you get a lot of easy matches there. Lofi plus chill pulls toward softer rows and the acoustic nudge, so the loud glossy stuff falls away. Flip the profile and the winners mostly flip too, because genre and mood points are doing most of the steering.

---

## High-energy pop party vs Deep intense rock

Both profiles want a lot of energy, so loud songs can still climb on the energy part of the score. The split is really genre and mood: rock intense should crown different songs than pop happy. If a pop track still sneaks high on the rock list, it is usually energy doing the work without the mood line matching, which is a good reminder to look at the weights.

---

## Chill lofi desk session vs Deep intense rock

These are almost opposite vibes on purpose. Chill lofi wants low energy and softer texture. Rock wants intensity and a lean away from super acoustic tracks. The two lists should look pretty different if the tags in the sheet line up with what you asked for.

---

## Deep intense rock vs Edge case: moody but hyper-energetic

Rock intense is one lane. Moody synthwave at very high energy is a narrow lane and there are not many rows like that in the sheet. If random loud rap or metal still floats up, it is probably energy carrying them, which tells you the catalog is small or the energy weight is loud compared to genre mood.

---

## High-energy pop party vs Edge case: moody but hyper-energetic

Happy high-energy pop is a broad radio shape. Moody synthwave at 0.95 energy is a weird specific ask. Synthwave rows will not get the pop genre bump, so the list should reshuffle around what is actually in the file, plus whatever slips in on energy alone. That gap is a good reminder that missing rows in the sheet looks like bad taste even when the code is doing what you told it.

---

## Chill lofi desk session vs Edge case: moody but hyper-energetic

Lofi chill is low energy with acoustic lean. The edge case wants synthwave, moody, and almost max energy. The lists should barely touch. If Night Drive Loop is in the sheet it should own the top for the edge case. If lofi tracks still hang near the top for the edge profile, I would re-read the weights or double check I ran the right block in the terminal.

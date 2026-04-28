# Model Card: VibeGuide (Applied AI System)

## 1. Model Name

VibeGuide 1.0

---

## 2. Intended Use

This system suggests a small ranked list of songs from a static CSV catalog. It also has an assistant mode that answers natural language requests by retrieving context before writing the response.

It is built for classroom exploration and transparency, not for real listeners or production traffic.

Non-intended use: class demo only. It is not a real product, not advice for anyone’s actual listening, and not a fairness study of a live app.

---

## 3. How the Model Works

The system has two layers. The base layer is content based scoring from song metadata (genre, mood, energy, acousticness). The applied AI layer adds retrieval and a generated answer in assistant mode.

In demo mode, the user supplies a short taste profile as a dictionary. The scorer adds fixed points for genre and mood matches, then adds an energy closeness term, and an acoustic nudge when the profile includes that preference.

In assistant mode, the user supplies a natural language request. The system retrieves relevant context from data/notes.txt and from the song sheet, then uses that plus the ranked list to produce the final answer.

To build a playlist-style list, the model scores every song, sorts by the total score from highest to lowest, and returns the top few results. The same math powers a small object-oriented wrapper used by unit tests.

---

## 4. Data

The catalog lives in data/songs.csv and contains 18 fictional tracks. Assistant mode also uses data/notes.txt.

Represented genres include pop, lofi, rock, ambient, jazz, synthwave, indie pop, metal, blues, country, classical, reggae, rap, folk, and electronic. Moods include happy, chill, intense, relaxed, moody, and focused.

The data is synthetic and small, so it cannot represent real-world diversity, regional scenes, or long-tail taste. There is no listening history, no social signals, and no audio analysis beyond hand-authored numbers.

---

## 5. Strengths

The scoring rules are easy to read and debug, which makes it clear why a song rose or fell in the list. For profiles that align with clear genre and mood tags, such as lofi plus chill plus low energy, the top picks usually feel coherent. The energy closeness term helps separate calm desk music from gym intensity even when genre labels collide.

---

## 6. Limitations and Bias

Because genre equality is a strict string match, nearby ideas like indie pop and pop do not automatically count as the same bucket, so some good fits can lose easy points while still ranking on mood and energy alone. The catalog is tiny, so a single loud anthem can dominate several profiles if energy weights are high.

It can feel like a filter bubble because it only recommends what is already in the CSV. If a style never got added to the sheet, the program acts like it does not exist.

---

## 7. Evaluation

I tested four hand-written profiles in demo mode and three natural language prompts in assistant mode.

For reliability, I kept unit tests (pytest) and added an eval harness script that runs fixed prompts and checks the output includes the expected structure (ranked list with reasons). I also watched for failure cases like the same artist repeating too often, so I added an artist diversity rule in the ranking.

---

## 8. Future Work

If I had more time, I would expand the catalog, loosen genre matching so related labels connect, and add a stronger evaluation harness that checks more properties than basic formatting.

---

## 9. Personal Reflection

What surprised me is how quickly a small system can feel helpful even with a tiny dataset, as long as the output is clear about why it picked something.

I used AI help for some of the structure, but I still ran the program and tests myself because small mistakes can change the ranking and you only notice by checking the output.

One thing I would try next is a fake listening history table so I can compare a collaborative style signal to this content based baseline.

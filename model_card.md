# Model Card: Music Recommender Simulation

## 1. Model Name

VibeRank Classroom 1.0

---

## 2. Intended Use

This recommender suggests a small ranked list of songs from a static CSV catalog. It assumes the user can describe their taste with a favorite genre, favorite mood, a target energy level between zero and one, and optionally whether they prefer acoustic textures.

It is built for classroom exploration and transparency, not for real listeners or production traffic.

Non-intended use: class demo only. It is not a real product, not advice for anyone’s actual listening, and not a fairness study of a live app.

---

## 3. How the Model Works

The system is intentionally simple and content-based. For each song it looks at metadata only: genre, mood, energy, and acousticness, plus other columns in the file that are not scored yet.

The user supplies a short taste profile as a dictionary. The model adds fixed points when the genre matches and when the mood matches. It then adds an energy component that rewards songs whose energy is numerically close to the user target, instead of always preferring higher energy. If the user sets an acoustic preference flag, the score nudges toward higher or lower acousticness.

To build a playlist-style list, the model scores every song, sorts by the total score from highest to lowest, and returns the top few results. The same math powers a small object-oriented wrapper used by unit tests.

---

## 4. Data

The catalog lives in `data/songs.csv` and currently contains 18 fictional tracks after expanding the starter set with additional genres and moods.

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

I tried four hand-written profiles in src/main.py: peppy pop, chill lofi, intense rock, and a weird high-energy moody synthwave case to see if the sheet even has anything that fits.

I stared at the printed top fives and asked if anything felt obviously wrong, like the same winner every time or energy bulldozing genre. I also re-ran the pop profile with softer genre points and stronger energy points to see if the order wiggled. The starter tests in tests/test_recommender.py still pass and they check that explanations are not empty strings.

---

## 8. Future Work

I would try a simple diversity rule so the top five is not all one artist. I would loosen genre matching so indie pop and pop can talk to each other. If I had time for a second toy dataset, I would fake a few other users and compare that ranking to this pure tag score.

---

## 9. Personal Reflection

What surprised me is how fast a handful of rules can feel like a recommender even though there is no real listening data and no lyrics.

I used AI help for some of the typing and layout, but I still ran the program and tests myself because a typo in a weight or a CSV cell can reshuffle the whole list and you would not notice unless you looked.

If I kept going, I would mock a tiny listening history table and see how different the top five looks compared to this tag-only version.

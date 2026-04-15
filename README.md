# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a small python program for class. It reads pretend songs from a spreadsheet, you type a simple taste profile, and it prints a short list of suggestions with short reasons in the terminal. Nothing fancy, just rules you can read in the project files.

---

## How The System Works

Explain your design in plain language.

Big apps guess what you want using what millions of people do, plus lots of signals. Mine only looks at the columns in the song sheet and a few preferences I type in. It never sees skips, likes, or other listeners.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo

  Each song is one row in the sheet. I keep the usual stuff like title and artist, plus genre, mood, and a zero to one energy number. There are a few extra numbers in the file for later, but right now the score mostly cares about genre, mood, energy, and sometimes how acoustic a track feels.

- What information does your `UserProfile` store

  When I run it from the command line I use a tiny profile: favorite genre, mood, target energy, and sometimes whether I want acoustic leaning tracks. The tests use a small profile object with the same idea, just different field names that get lined up before scoring.

- How does your `Recommender` compute a score for each song

  It is basically points. When my genre matches the row I get a chunk of points, same for mood. Then it gives more points when the song energy is close to the energy I asked for, instead of always rewarding the loudest song. If I said I like acoustic sounds it nudges toward warmer tracks, and if I said I do not it nudges the other way a little. At the end I get one total number plus little labels that explain where the points came from.

- How do you choose which songs to recommend

  It scores every song in the sheet, sorts highest score first, and cuts off the top five so I am not staring at the whole list.

You can include a simple diagram or bullet list if helpful.

Simple flow: load the sheet, score each row, sort, show the top few with reasons.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the command line interface:

   ```bash
   python -m src.main
   ```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

I tried a few different fake listeners in the main script, then ran the same pop style listener again but with the genre points turned down and the energy part turned up. That was just to see if the list shuffled toward louder neighbors. I have not folded tempo or valence into the score yet.

Next I need to drop a few terminal screenshots into the repo and link them here like normal markdown images.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

It only knows the songs in the sheet, so if my taste is not really in there I am out of luck. Genre has to match the text exactly, so close cousins like pop and indie pop do not automatically count as the same thing. Loud songs can still float up for more than one mood if energy lines up. I wrote more of this in the model card file.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

I also wrote short comparisons between profiles in reflection.md.

What stuck with me is how plain the whole thing is under the hood. You have rows in a table, a handful of preferences, a few rules, and then a sorted list. That is the whole trick for this assignment sized version, and it still feels a little like a recommender when you run it.

The part that worries me is how fast bias shows up. If the sheet leans one genre, your rules will lean that way too. If two genres are spelled differently even when a human would call them close, the math does not care. A real app has a lot more checks and data. This one is just for learning, but it still makes you think about who gets left out when the catalog is tiny.

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance.

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

```

"""
Lab 4 — Seeing embeddings in vector space (UMAP)
================================================

THE BIG IDEA
------------
When OpenAI's embedding model reads a word, it returns a "vector" — a long list
of numbers (1536 of them for text-embedding-3-small). That vector is a point in a
1536-dimensional space, and the model arranges things so that words with similar
MEANING end up close together in that space.

We can't draw 1536 dimensions. So we use UMAP, an algorithm that shrinks those
1536-D points down to 2-D or 3-D *while trying to keep neighbors as neighbors*.
The result is a picture we can actually look at — and similar words really do
land near each other.

WHAT THIS PROGRAM DOES, STEP BY STEP
------------------------------------
1. Take the SAME sentences Lab 2 measured (from sample_data.py), grouped into
   four topics: pets, finance, food, travel.
2. Ask OpenAI to turn each sentence into a 1536-D embedding vector.
3. Use UMAP to project those vectors down to 3-D (or 2-D with --2d).
4. Plot the result, coloring each point by its topic.
You should see four separate clusters — proof the model grouped the sentences by
meaning on its own, even though it was never told the topics. The paraphrase
pairs that scored "similar" in Lab 2 land right next to each other here.

Run:
    # put OPENAI_API_KEY in a .env file, or export it in your shell
    python lab4_umap_embeddings.py          # interactive, rotatable 3-D, also saves a PNG
    python lab4_umap_embeddings.py --2d     # flat 2-D version
"""

# --- Imports -----------------------------------------------------------------
import sys                          # to read command-line flags like "--2d"

import numpy as np                  # fast array math; embeddings are arrays of floats
import matplotlib.pyplot as plt     # the plotting library that draws the scatter
import umap                         # the dimensionality-reduction algorithm
from dotenv import load_dotenv      # reads key=value pairs from a .env file
from openai import OpenAI           # the official OpenAI client

# The SAME sentences Lab 2 measured for similarity — reused here so the two labs
# line up: the pairs that scored "similar" as numbers in Lab 2 should land in the
# same cluster as a picture here.
from sample_data import SENTENCES, SHORT_LABELS, GROUPS, TOPICS

# --- Setup -------------------------------------------------------------------
# load_dotenv() looks for a ".env" file (here or in a parent folder) and copies
# any variables it finds into the environment. That lets us keep the secret key
# out of the source code.
load_dotenv()

# OpenAI() with no arguments automatically reads the OPENAI_API_KEY environment
# variable (which load_dotenv just populated). `client` is our handle for every
# API call below.
client = OpenAI()

# The embedding model we'll use. "small" is cheap and fast; it returns 1536-D
# vectors. (There is also text-embedding-3-large with 3072 dimensions.)
EMBED_MODEL = "text-embedding-3-small"

# Our input data comes from sample_data.py: a dozen sentences grouped into four
# topics (pets, finance, food, travel). The grouping is ONLY so we can color the
# plot and check UMAP's work afterward — the embedding model never sees the
# topics, it only sees the bare sentences.

# A color per topic, used when drawing the scatter plot.
PALETTE = {"pets": "#1abc9c", "finance": "#e67e22",
           "food": "#9b59b6", "travel": "#3498db"}


def embed(texts: list[str]) -> np.ndarray:
    """Turn a list of strings into a matrix of embedding vectors.

    Returns an array of shape (number_of_texts, 1536): one row per input string,
    each row being that string's 1536-number embedding.
    """
    # One API call embeds the whole list at once (more efficient than looping).
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)

    # resp.data is a list with one entry per input string, IN THE SAME ORDER.
    # Each entry's .embedding is the 1536-float vector. We stack them into a
    # single 2-D NumPy array of 32-bit floats (float32 is plenty of precision
    # and uses half the memory of the default float64).
    return np.array([item.embedding for item in resp.data], dtype=np.float32)


def main() -> None:
    # --- Step 0: decide 2-D vs 3-D from the command line ---------------------
    # If the user did NOT pass "--2d", we default to a 3-D plot.
    three_d = "--2d" not in sys.argv
    dims = 3 if three_d else 2

    print("=" * 64)
    print(f"LAB 4 · UMAP — embeddings in {dims}-D vector space")
    print("=" * 64)

    # --- Step 1: pull the shared, parallel lists from sample_data ------------
    # SENTENCES  = the full sentences we embed.
    # SHORT_LABELS = a short tag per sentence, used to label points on the plot.
    # GROUPS     = the topic of each sentence, in the SAME order.
    # All three stay aligned by index: item i is SENTENCES[i] / SHORT_LABELS[i] /
    # GROUPS[i].
    sentences, labels, groups = SENTENCES, SHORT_LABELS, GROUPS

    # --- Step 2: get the embeddings -----------------------------------------
    print(f"\nEmbedding {len(sentences)} sentences -> {EMBED_MODEL} (1536-dim vectors)...")
    vecs = embed(sentences)     # shape: (12, 1536) — 12 sentences, 1536 numbers each

    # --- Step 3: reduce 1536-D down to 2-D or 3-D with UMAP ------------------
    print(f"Running UMAP (1536-D -> {dims}-D)...")
    reducer = umap.UMAP(
        n_components=dims,      # how many output dimensions (2 or 3 here)
        n_neighbors=4,          # how many nearby points define "local" structure.
                                #   Small because we only have 12 sentences; larger
                                #   values emphasize global shape over local.
        min_dist=0.3,           # how tightly points may pack together (0 = very
                                #   tight clumps, higher = more spread out).
        metric="cosine",        # measure closeness by ANGLE between vectors, which
                                #   is the standard way to compare text embeddings.
        random_state=42,        # fix the randomness so the layout is reproducible
                                #   (rerunning gives the same picture).
    )
    # fit_transform learns the projection AND applies it, returning the new
    # low-dimensional coordinates. Shape: (12, dims).
    coords = reducer.fit_transform(vecs)

    # --- Step 4: draw the scatter plot --------------------------------------
    fig = plt.figure(figsize=(10, 8))   # create a blank canvas (width, height in inches)

    if three_d:
        # add_subplot(111) = "1 row, 1 column, plot #1"; projection="3d" makes
        # it a rotatable 3-D axis.
        ax = fig.add_subplot(111, projection="3d")

        # Plot one topic at a time so each gets its own color and legend entry.
        for g in TOPICS:
            # Pick out the coordinates whose topic matches g.
            pts = np.array([coords[i] for i, gg in enumerate(groups) if gg == g])
            ax.scatter(
                pts[:, 0], pts[:, 1], pts[:, 2],   # the x, y, z columns
                s=90,                  # marker size
                c=PALETTE[g],          # this topic's color
                label=g,               # name shown in the legend
                edgecolors="white",    # white outline so points pop
                linewidths=0.6,
                depthshade=True,       # fade distant points for a depth cue
            )
        # Write each sentence's short label right next to its point.
        for (x, y, z), tag in zip(coords, labels):
            ax.text(x, y, z, tag, fontsize=8)

        ax.set_xlabel("UMAP 1"); ax.set_ylabel("UMAP 2"); ax.set_zlabel("UMAP 3")
    else:
        # The 2-D branch: same idea, just x and y (no z).
        ax = fig.add_subplot(111)
        for g in TOPICS:
            pts = np.array([coords[i] for i, gg in enumerate(groups) if gg == g])
            ax.scatter(pts[:, 0], pts[:, 1], s=120, c=PALETTE[g], label=g,
                       edgecolors="white", linewidths=0.6)
        # annotate() places each label slightly offset (5 px right, 4 px up) from
        # its dot so the text doesn't sit on top of the marker.
        for (x, y), tag in zip(coords, labels):
            ax.annotate(tag, (x, y), fontsize=9, xytext=(5, 4),
                        textcoords="offset points")
        ax.set_xlabel("UMAP 1"); ax.set_ylabel("UMAP 2")

    # Title and legend apply to either branch.
    ax.set_title(f"Sentence embeddings in {dims}-D vector space (UMAP)\n"
                 "same sentences as Lab 2 — they cluster by topic, learned unsupervised")
    ax.legend(loc="best")       # "best" = let matplotlib pick a non-overlapping spot
    plt.tight_layout()          # trim excess whitespace around the figure

    # --- Step 5: save and show ----------------------------------------------
    # Save a static image so you have a copy even on a headless machine.
    out = f"embeddings_umap_{dims}d.png"
    plt.savefig(out, dpi=130)   # dpi controls resolution
    print(f"\nSaved plot to {out}")
    print("Opening an interactive window — drag to rotate the 3-D space, close to exit.")
    print("You should see the pets / finance / food / travel sentences in four")
    print("separate clusters — the same sentences Lab 2 scored for similarity.")

    # plt.show() opens the interactive window and blocks until you close it.
    # In 3-D you can click-and-drag to rotate the vector space.
    plt.show()


# This guard means main() runs only when you execute the file directly
# (python lab4_umap_embeddings.py), not if it's imported by another module.
if __name__ == "__main__":
    main()

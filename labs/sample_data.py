"""
Shared sample sentences for Lab 2 (embeddings) and Lab 4 (UMAP)
==============================================================

Both labs use the SAME sentences so they tell one continuous story:
  * Lab 2 shows, as numbers, that paraphrases are "close" (high cosine similarity).
  * Lab 4 shows, as a picture, those same sentences clustering by topic.

The sentences are grouped into four topics. The embedding model is never told
the topics — they're here only so Lab 4 can color the plot and we can check that
similar meanings really did end up together. Each sentence also carries a short
label for clean plotting (full sentences are too long to print on a chart).

Within a topic, the first two lines are deliberate PARAPHRASES (same meaning,
different words) so Lab 2's similarity matrix has obvious bright spots.
"""

# topic -> list of (full_sentence, short_label_for_plots)
TOPICS = {
    "pets": [
        ("The cat sat on the warm windowsill.",            "cat · windowsill"),
        ("A kitten napped in the sunny window.",           "kitten · window"),
        ("The puppy chased its tail in the yard.",         "puppy · yard"),
    ],
    "finance": [
        ("The stock market fell sharply today.",           "market · fell"),
        ("Shares plunged on the exchange this afternoon.", "shares · plunged"),
        ("Investors sold off bonds amid the downturn.",    "bonds · sold"),
    ],
    "food": [
        ("I love eating fresh pizza on Fridays.",          "pizza · Fridays"),
        ("She baked a warm loaf of sourdough bread.",      "sourdough · bread"),
        ("We grilled vegetables for dinner last night.",   "grilled · veggies"),
    ],
    "travel": [
        ("They booked a flight to Tokyo for the spring.",  "flight · Tokyo"),
        ("Our train wound through the mountain valleys.",  "train · mountains"),
        ("He packed his bags for a weekend road trip.",    "road · trip"),
    ],
}

# Flat, parallel lists derived from TOPICS (all share the same order/index).
SENTENCES = [s for items in TOPICS.values() for (s, _) in items]
SHORT_LABELS = [lbl for items in TOPICS.values() for (_, lbl) in items]
GROUPS = [topic for topic, items in TOPICS.items() for _ in items]

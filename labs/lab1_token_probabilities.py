"""
Lab 1 — Seeing how an LLM "thinks": token probabilities & sampling controls
===========================================================================

An LLM does not "decide" an answer. At every step it produces a *probability
distribution* over its entire vocabulary, then PICKS one token from it, appends
it, and repeats. The OpenAI API can show you that distribution directly via
`logprobs`.

This lab does three things for each prompt:
  1. Prints the model's actual ANSWER (the full generated text).
  2. Prints the probability distribution over its very FIRST token, so you can
     watch the "spiky vs. flat" behavior that drives everything.
Then it demonstrates the knobs that control HOW a token is picked from that
distribution: temperature, top_p, and (conceptually) top_k.

A subtlety worth knowing: chat models are trained to RESPOND, not to continue
your text, so the raw fragment "The capital of France is" makes the model reply
with a full sentence ("The capital of France is Paris.") whose first token is
"The", not "Paris". We add a small system prompt to make it behave like a plain
autocomplete engine, so the next token genuinely IS the answer. (See
COMPLETION_SYSTEM below.)

Run:
    # put OPENAI_API_KEY in a .env file, or export it in your shell
    python lab1_token_probabilities.py
"""

import math
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # load OPENAI_API_KEY from a .env file if present
client = OpenAI()  # reads OPENAI_API_KEY from the environment

CHAT_MODEL = "gpt-4o-mini"  # a small, cheap chat model that supports logprobs

# IMPORTANT — why we use a system prompt here.
# gpt-4o-mini is a CHAT model: it's trained to RESPOND, not to continue your
# text. If you just send the fragment "The capital of France is", it replies with
# a whole sentence that *starts* "The capital of France is Paris." — so its very
# first token is "The" (99%+), NOT "Paris"! That's correct next-token prediction,
# but it hides the point of this lab. To make the next token BE the answer, we
# steer the model with a system prompt to act like a plain autocomplete engine
# that continues the user's text directly.
COMPLETION_SYSTEM = (
    "You are an autocomplete engine. Continue the user's text with the words "
    "that most naturally come next. Do not repeat or rephrase the prompt, do not "
    "add quotation marks, and do not explain — just continue the text."
)


def messages_for(prompt: str) -> list[dict]:
    """Wrap a prompt with the autocomplete system instruction."""
    return [{"role": "system", "content": COMPLETION_SYSTEM},
            {"role": "user", "content": prompt}]


# ---------------------------------------------------------------------------
# Helper 1 — get the model's actual answer (continuation) for a prompt
# ---------------------------------------------------------------------------
def answer(prompt: str, **sampling) -> str:
    """Return the full text the model generates to continue `prompt`.

    Any sampling knob (temperature=..., top_p=...) is passed straight through
    so we can reuse this function in the sampling demos below.
    """
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages_for(prompt),
        max_completion_tokens=60,
        **sampling,
    )
    return resp.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Helper 2 — show the probability distribution over the FIRST token
# ---------------------------------------------------------------------------
def show_distribution(prompt: str, top_n: int = 12) -> None:
    """Print the model's top candidate tokens for the next position."""
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages_for(prompt),  # autocomplete-style, so the next token IS the answer
        max_completion_tokens=1,  # we only want the VERY NEXT token here
        temperature=0,            # the distribution itself is what we inspect
        logprobs=True,            # ask the API for log-probabilities...
        top_logprobs=top_n,       # ...of the top-N candidate tokens (max 20)
    )

    # logprobs.content is one entry per generated token; [0] is the first (only)
    # one. Its .top_logprobs is the ranked list of candidate tokens we want.
    candidates = resp.choices[0].logprobs.content[0].top_logprobs

    print("  Top candidates for the next token:")
    print(f"    {'token':<16}{'probability':>12}   distribution")
    print(f"    {'-'*16}{'-'*12:>12}   {'-'*30}")
    for c in candidates:
        prob = math.exp(c.logprob)      # a logprob converts to a probability via exp()
        bar = "█" * max(1, round(prob * 30))
        print(f"    {repr(c.token):<16}{prob:>11.2%}   {bar}")  # repr() reveals spaces


# ---------------------------------------------------------------------------
# Demo of the sampling knobs
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# The math behind the knobs (computed locally from the model's own logprobs)
# ---------------------------------------------------------------------------
# NOTE: temperature/top_p/top_k are applied INSIDE the model at sampling time,
# so the API won't hand us "the distribution at temperature 2.0" directly.
# But we don't need it to: given the model's base log-probabilities, the effect
# of each knob is a simple, exact transformation we can reproduce here — which is
# the clearest way to SEE the probabilities change.

def softmax(x: np.ndarray) -> np.ndarray:
    """Turn a vector of scores into probabilities that sum to 1."""
    e = np.exp(x - x.max())     # subtract max for numerical stability
    return e / e.sum()


def apply_temperature(logprobs: np.ndarray, t: float) -> np.ndarray:
    """Reshape the distribution by temperature `t`.

    HOW THE SCALING WORKS
    ---------------------
    A model's final layer outputs a raw score per token called a "logit" (z_i).
    It converts those to probabilities with the softmax function:

            p_i = exp(z_i) / sum_j exp(z_j)

    Temperature divides every logit by t *before* softmax:

            p_i(t) = exp(z_i / t) / sum_j exp(z_j / t)

      * t < 1  -> dividing by a small number STRETCHES the gaps between logits,
                  so the leader pulls further ahead -> spikier distribution.
      * t > 1  -> dividing by a big number SQUASHES the gaps -> flatter.
      * t -> 0 -> greedy: all mass on the single largest logit.
      * t -> inf -> uniform: every token equally likely.

    We only have log-probabilities here, not the raw logits, but that's fine:
    logprob_i = z_i - C (a shared constant), and that constant cancels inside
    softmax, so p_i(t) = softmax(logprob_i / t) gives the identical result.
    """
    if t == 0:
        p = np.zeros_like(logprobs)
        p[np.argmax(logprobs)] = 1.0
        return p
    return softmax(logprobs / t)


def apply_top_p(probs: np.ndarray, p: float) -> np.ndarray:
    """Nucleus filter: keep the most likely tokens until their probs reach p,
    zero out the rest, then renormalize the survivors back to sum 1."""
    order = np.argsort(probs)[::-1]          # indices, most→least likely
    kept, cumulative = [], 0.0
    for i in order:
        kept.append(i)
        cumulative += probs[i]
        if cumulative >= p:                  # we've collected enough mass
            break
    out = np.zeros_like(probs)
    out[kept] = probs[kept]
    return out / out.sum()                    # renormalize the kept set


def apply_top_k(probs: np.ndarray, k: int) -> np.ndarray:
    """Top-k filter: keep only the k most likely tokens, renormalize the rest."""
    keep = np.argsort(probs)[::-1][:k]
    out = np.zeros_like(probs)
    out[keep] = probs[keep]
    return out / out.sum()


def print_columns(tokens, columns, headers, top=8) -> None:
    """Print a side-by-side table of probability columns for the top tokens.

    `columns` is a list of probability arrays; `headers` names each column.
    Rows are ordered by the FIRST column so the comparison is easy to read.
    A 0.0% entry means that knob filtered the token out entirely.
    """
    order = np.argsort(columns[0])[::-1][:top]
    head = "  " + f"{'token':<14}" + "".join(f"{h:>10}" for h in headers)
    print(head)
    print("  " + "-" * (14 + 10 * len(headers)))
    for i in order:
        cells = "".join(f"{col[i]:>9.1%}" for col in columns)
        print("  " + f"{repr(tokens[i]):<14}" + cells)


def explain_sampling() -> None:
    """Explain the knobs, then SHOW the same distribution reshaped by each one."""
    print("\n" + "=" * 64)
    print("SAMPLING CONTROLS — how the knobs RESHAPE the probabilities")
    print("=" * 64)
    print("""
The model gives a probability to every possible next token. These knobs decide
how that list is turned into one chosen token. Below we take ONE real
distribution from the model and watch the numbers move.

  TEMPERATURE (OpenAI 0-2): scales the distribution.  low -> sharper (top token
    dominates, deterministic);  high -> flatter (long-shots get a real chance).
  TOP_P  (OpenAI 0-1, "nucleus"): keep the top tokens whose probs ADD UP to p,
    drop the rest, renormalize.  top_p=0.1 = very safe;  top_p=1.0 = no filter.
  TOP_K: keep only the k most likely tokens, drop the rest, renormalize.
    NOTE: OpenAI's API does NOT expose top_k (only temperature & top_p); it IS
    on Anthropic Claude, Google Gemini, and most local/open-source runtimes.
  Tip: tune temperature OR top_p, not both.
""")

    # 1) Grab one real distribution to experiment on. An open-ended prompt gives
    #    a nicely spread distribution so the reshaping is easy to see.
    prompt = "My favorite color is"
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages_for(prompt),  # autocomplete-style continuation
        max_completion_tokens=1,
        temperature=1,        # ask for the model's natural distribution
        logprobs=True,
        top_logprobs=20,      # the top 20 candidates (the API maximum)
    )
    cands = resp.choices[0].logprobs.content[0].top_logprobs
    tokens = [c.token for c in cands]
    logprobs = np.array([c.logprob for c in cands], dtype=float)
    base = softmax(logprobs)  # renormalized over these top-20 candidates

    print(f'Base distribution for prompt: "{prompt}"')
    print("(illustrated on the top-20 candidates the API returns)\n")

    # 2) TEMPERATURE: first show HOW the scaling works on a tiny 2-token example,
    #    then on the real distribution.
    print("HOW TEMPERATURE SCALES")
    print("  The model outputs a raw score per token (a 'logit' z), then")
    print("  softmax turns scores into probabilities:  p_i = exp(z_i)/sum exp(z_j).")
    print("  Temperature divides the logits FIRST:      p_i(T) = softmax(z / T).")
    print("  Worked example with two tokens, logits z = [2.0, 1.0]:")
    z = np.array([2.0, 1.0])
    for tt in (0.5, 1.0, 2.0):
        p = softmax(z / tt)
        gap = "wider gap (spikier)" if tt < 1 else ("baseline" if tt == 1 else "narrower gap (flatter)")
        print(f"    T={tt:<4} z/T = {np.round(z/tt,2)}  ->  p = {np.round(p,3)}   {gap}")
    print()

    # Now the same idea on the model's real distribution: watch the mass shift.
    print("TEMPERATURE on the real distribution — lower = spikier, higher = flatter:")
    print_columns(
        tokens,
        [apply_temperature(logprobs, 0.25),
         apply_temperature(logprobs, 1.0),
         apply_temperature(logprobs, 2.0)],
        ["T=0.25", "T=1.0", "T=2.0"],
    )

    # 3) TOP_P: tokens outside the nucleus drop to 0%, survivors get renormalized.
    print("\nTOP_P — tokens outside the cumulative-p nucleus are removed (0.0%):")
    print_columns(
        tokens,
        [base, apply_top_p(base, 0.9), apply_top_p(base, 0.5)],
        ["base", "p=0.9", "p=0.5"],
    )

    # 4) TOP_K: only the k most likely tokens survive.
    print("\nTOP_K — only the k most likely tokens survive (rest become 0.0%):")
    print_columns(
        tokens,
        [base, apply_top_k(base, 5), apply_top_k(base, 2)],
        ["base", "k=5", "k=2"],
    )

    print("\nSee it: as temperature drops the top token's share climbs toward")
    print("100%; top_p and top_k simply zero out the unlikely tail and rescale")
    print("what remains. That reshaped distribution is what the model samples from.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 64)
    print("LAB 1 · Token probabilities — watching an LLM predict")
    print("=" * 64)

    prompts = [
        "The capital of France is",       # near-certain: distribution spikes
        "My favorite color is",           # open-ended: distribution spreads
        "Once upon a time, there was a",  # creative: very spread out
    ]

    for p in prompts:
        print(f'\nPrompt: "{p}"')
        # 1) the model's actual answer (a normal, full completion)
        print(f"  Answer: {answer(p)}")
        # 2) the distribution over the first token it could have produced
        show_distribution(p)

    print("\nTakeaway: confident facts produce a spiky distribution (one token")
    print("near 100%); open-ended prompts produce a flat one. The sampling knobs")
    print("below decide how adventurously the model picks from that distribution.")

    explain_sampling()

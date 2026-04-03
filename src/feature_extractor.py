import re
from collections import Counter

# ── Lexicons ──────────────────────────────────────────────────────────────────

DEPRESSION_KEYWORDS = [
    'hopeless', 'worthless', 'empty', 'numb', 'tired', 'exhausted',
    'alone', 'lonely', 'sad', 'depressed', 'broken', 'lost', 'dark',
    'hurt', 'pain', 'suffering', 'miserable', 'hate myself', 'no one cares',
    'give up', 'cant go on', "can't go on", 'end it', 'disappear',
    'invisible', 'burden', 'failure', 'pointless', 'meaningless',
    'crying', 'tears', 'sob', 'hollow', 'void', 'dead inside',
    'cant sleep', "can't sleep", 'insomnia', 'nightmare', 'no energy',
    'nothing matters', 'why bother', 'whats the point', "what's the point"
]

ANXIETY_KEYWORDS = [
    'anxious', 'anxiety', 'panic', 'nervous', 'worried', 'overwhelmed',
    'scared', 'fear', 'dread', 'stress', 'stressed', 'tense',
    'cant breathe', "can't breathe", 'heart racing', 'shaking'
]

ISOLATION_KEYWORDS = [
    'alone', 'lonely', 'isolated', 'no friends', 'nobody', 'no one',
    'by myself', 'antisocial', 'withdrawn', 'disconnected', 'invisible'
]

SELF_HARM_KEYWORDS = [
    'hurt myself', 'cut myself', 'self harm', 'self-harm',
    'end my life', 'kill myself', 'suicide', 'not worth living',
    'want to die', 'wanna die', 'better off dead', 'end it all'
]

NEGATIVE_INTENSIFIERS = [
    'always', 'never', 'every day', 'everyday', 'constantly',
    'all the time', 'forever', 'nothing ever', 'nothing works'
]

POSITIVE_INDICATORS = [
    'happy', 'excited', 'grateful', 'thankful', 'blessed', 'joy',
    'love', 'great', 'amazing', 'wonderful', 'hope', 'better',
    'improving', 'proud', 'smile', 'laugh', 'fun', 'celebrate'
]


def extract_features(text: str) -> dict:
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    word_count = len(words)

    # Keyword hits
    dep_hits    = [kw for kw in DEPRESSION_KEYWORDS  if kw in text_lower]
    anx_hits    = [kw for kw in ANXIETY_KEYWORDS     if kw in text_lower]
    iso_hits    = [kw for kw in ISOLATION_KEYWORDS   if kw in text_lower]
    harm_hits   = [kw for kw in SELF_HARM_KEYWORDS   if kw in text_lower]
    intens_hits = [kw for kw in NEGATIVE_INTENSIFIERS if kw in text_lower]
    pos_hits    = [kw for kw in POSITIVE_INDICATORS  if kw in text_lower]

    # Linguistic markers
    first_person_count  = sum(1 for w in words if w in ('i', 'me', 'my', 'myself', 'mine'))
    exclamation_count   = text.count('!')
    question_count      = text.count('?')
    ellipsis_count      = text.count('...')
    caps_ratio          = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    avg_word_length     = sum(len(w) for w in words) / max(word_count, 1)
    unique_ratio        = len(set(words)) / max(word_count, 1)

    # Negative sentiment pattern (simple)
    negation_words = ['not', 'no', 'never', "n't", 'dont', 'cant', 'wont', 'isnt', 'wasnt']
    negation_count = sum(1 for w in words if w in negation_words)

    return {
        'word_count'          : word_count,
        'depression_keywords' : dep_hits,
        'anxiety_keywords'    : anx_hits,
        'isolation_keywords'  : iso_hits,
        'self_harm_keywords'  : harm_hits,
        'intensifiers'        : intens_hits,
        'positive_keywords'   : pos_hits,
        'first_person_count'  : first_person_count,
        'first_person_ratio'  : round(first_person_count / max(word_count, 1), 3),
        'exclamation_count'   : exclamation_count,
        'question_count'      : question_count,
        'ellipsis_count'      : ellipsis_count,
        'caps_ratio'          : round(caps_ratio, 3),
        'avg_word_length'     : round(avg_word_length, 2),
        'unique_word_ratio'   : round(unique_ratio, 3),
        'negation_count'      : negation_count,
    }

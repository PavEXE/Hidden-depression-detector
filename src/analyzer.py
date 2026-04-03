"""
analyzer.py
Core depression-risk scoring engine.
Uses a weighted rule-based system (no external ML model required).
"""

from __future__ import annotations

# ── Weights ───────────────────────────────────────────────────────────────────

W_DEPRESSION  = 0.30   # per unique depression keyword matched
W_ANXIETY     = 0.15
W_ISOLATION   = 0.12
W_SELF_HARM   = 0.80   # high weight — crisis signal
W_INTENSIFIER = 0.10
W_FP_RATIO    = 0.20   # high first-person ratio
W_ELLIPSIS    = 0.05
W_NEGATION    = 0.04
W_POSITIVE    = -0.15  # positive words reduce risk

RISK_THRESHOLDS = {
    'Low'      : 0.35,
    'Moderate' : 0.60,
    'High'     : float('inf'),
}

PLATFORM_MULTIPLIERS = {
    'twitter'   : 1.0,
    'reddit'    : 1.1,   # longer posts, more context
    'instagram' : 0.9,   # tends to be more curated/positive
    'facebook'  : 1.0,
}

CRISIS_PHRASES = [
    'want to die', 'wanna die', 'kill myself', 'end my life',
    'end it all', 'not worth living', 'better off dead',
    'hurt myself', 'self harm', 'self-harm', 'suicide'
]

RECOMMENDATIONS = {
    'Low': [
        "Continue monitoring for changes in posting patterns.",
        "Encourage engagement with supportive communities.",
        "No immediate intervention needed."
    ],
    'Moderate': [
        "Consider reaching out with a check-in message.",
        "Share mental health resources proactively.",
        "Watch for escalation over the next 24-48 hours.",
        "iCall Helpline (India): 9152987821"
    ],
    'High': [
        "🚨 Immediate attention recommended.",
        "Share crisis helpline information directly.",
        "iCall Helpline (India): 9152987821",
        "Vandrevala Foundation 24/7: 1860-2662-345",
        "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/",
        "Encourage the person to speak with a mental health professional urgently."
    ]
}


def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def _risk_level(score: float) -> str:
    for level, threshold in RISK_THRESHOLDS.items():
        if score <= threshold:
            return level
    return 'High'


def analyze_text(text: str, features: dict, platform: str = 'twitter') -> dict:
    multiplier = PLATFORM_MULTIPLIERS.get(platform.lower(), 1.0)

    # ── Raw score ─────────────────────────────────────────────────────────────
    score = 0.0

    score += len(features['depression_keywords']) * W_DEPRESSION
    score += len(features['anxiety_keywords'])    * W_ANXIETY
    score += len(features['isolation_keywords'])  * W_ISOLATION
    score += len(features['self_harm_keywords'])  * W_SELF_HARM
    score += len(features['intensifiers'])        * W_INTENSIFIER
    score += len(features['positive_keywords'])   * W_POSITIVE
    score += features['ellipsis_count']           * W_ELLIPSIS
    score += features['negation_count']           * W_NEGATION

    # High first-person ratio (> 0.20) adds signal
    if features['first_person_ratio'] > 0.20:
        score += (features['first_person_ratio'] - 0.20) * W_FP_RATIO

    # Apply platform multiplier, then clamp
    score = _clamp(score * multiplier)

    # ── Crisis override ───────────────────────────────────────────────────────
    text_lower = text.lower()
    crisis_triggered = any(phrase in text_lower for phrase in CRISIS_PHRASES)
    if crisis_triggered:
        score = max(score, 0.85)   # floor at 0.85 for crisis language

    # ── Build output ──────────────────────────────────────────────────────────
    risk = _risk_level(score)

    # Dominant signals for explanation
    detected_signals = []
    if features['depression_keywords']:
        detected_signals.append(f"Depression language: {', '.join(features['depression_keywords'][:4])}")
    if features['anxiety_keywords']:
        detected_signals.append(f"Anxiety language: {', '.join(features['anxiety_keywords'][:3])}")
    if features['isolation_keywords']:
        detected_signals.append(f"Isolation indicators: {', '.join(features['isolation_keywords'][:3])}")
    if features['self_harm_keywords'] or crisis_triggered:
        detected_signals.append("⚠️ Crisis/self-harm language detected")
    if features['intensifiers']:
        detected_signals.append(f"Negative intensifiers: {', '.join(features['intensifiers'][:3])}")
    if features['first_person_ratio'] > 0.25:
        detected_signals.append(f"High self-referential language ({features['first_person_ratio']*100:.0f}% of words)")
    if features['positive_keywords']:
        detected_signals.append(f"Positive language present (reduces score): {', '.join(features['positive_keywords'][:3])}")

    return {
        'risk_score'       : round(score, 3),
        'risk_level'       : risk,
        'crisis_detected'  : crisis_triggered,
        'detected_signals' : detected_signals,
        'feature_summary'  : {
            'total_depression_keywords' : len(features['depression_keywords']),
            'total_anxiety_keywords'    : len(features['anxiety_keywords']),
            'total_isolation_keywords'  : len(features['isolation_keywords']),
            'positive_balance'          : len(features['positive_keywords']),
            'first_person_ratio'        : features['first_person_ratio'],
        },
        'recommendations'  : RECOMMENDATIONS[risk],
        'platform'         : platform,
    }

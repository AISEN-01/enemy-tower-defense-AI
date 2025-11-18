"""
Enemy wave patterns available to the AI.
These are templates that get slightly modified to avoid repetition.
"""

WAVE_PATTERNS = {
    "balanced": ["grunt", "grunt", "fast", "grunt"],
    "swarm":    ["swarm"] * 10,
    "tank_push":["tank", "grunt", "tank"],
    "fast_rush":["fast", "fast", "fast", "grunt"],
    "mixed":    ["grunt", "fast", "tank", "grunt", "flying"]
}

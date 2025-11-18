"""
Defines all enemy type configs used in the game.
This is a data-driven approach so balancing is easy.
"""

ENEMY_TYPES = {
    "grunt":   {"cost": 5,  "speed": 80,  "hp": 60},
    "fast":    {"cost": 7,  "speed": 150, "hp": 40},
    "tank":    {"cost": 20, "speed": 45,  "hp": 250},
    "flying":  {"cost": 10, "speed": 120, "hp": 45, "flying": True},
    "swarm":   {"cost": 3,  "speed": 95,  "hp": 20},
}

"""
Tower Defense Enemy AI (Normal Difficulty)

Features:
- Finite State Machine: early, mid, late game behavior
- Strategy selection: balanced, swarm, tank push, fast rush, etc.
- Weighted/random monster selection
- Light adaptation depending on player's tower types
"""

import random
import time

from .enemy_types import ENEMY_TYPES
from .wave_patterns import WAVE_PATTERNS


class EnemyAIState:
    EARLY_GAME = 0
    MID_GAME   = 1
    LATE_GAME  = 2


class TowerDefenseEnemyAI:
    def __init__(self):
        self.state = EnemyAIState.EARLY_GAME
        self.wave_number = 1

        self.last_wave_time = 0.0
        self.wave_cooldown = 6.0  # seconds between waves

        random.seed()

    # --------------------------
    # FSM Update
    # --------------------------
    def update_state(self):
        if self.wave_number < 4:
            self.state = EnemyAIState.EARLY_GAME
            self.wave_cooldown = 6.0

        elif self.wave_number < 9:
            self.state = EnemyAIState.MID_GAME
            self.wave_cooldown = 5.0

        else:
            self.state = EnemyAIState.LATE_GAME
            self.wave_cooldown = 4.0

    # --------------------------
    # Strategy selection
    # --------------------------
    def pick_strategy(self):
        if self.state == EnemyAIState.EARLY_GAME:
            return random.choice(["balanced", "swarm"])

        elif self.state == EnemyAIState.MID_GAME:
            return random.choice(["balanced", "fast_rush", "mixed"])

        else:
            return random.choice(["tank_push", "mixed", "swarm"])

    # --------------------------
    # Monster pattern
    # --------------------------
    def pick_monsters(self, strategy):
        pattern = WAVE_PATTERNS.get(strategy, ["grunt"])

        mutated = []
        for monster in pattern:
            # add small randomness so waves don’t feel copy-pasted
            if random.random() < 0.12:
                mutated.append(random.choice(list(ENEMY_TYPES.keys())))
            else:
                mutated.append(monster)

        return mutated

    # --------------------------
    # Light Adaptation (NOT smart)
    # --------------------------
    def maybe_adapt(self, towers):
        """
        Very simple adaptation.
        AI is not meant to be strong — just occasionally responds to your towers.
        """

        if random.random() >= 0.20:  # only 20% chance to adapt
            return None

        has_anti_ground = any(getattr(t, "type", "") == "anti_ground_only" for t in towers)
        has_slow_shoot  = any(getattr(t, "type", "") == "slow_shooter" for t in towers)
        has_short_range = any(getattr(t, "type", "") == "short_range" for t in towers)

        if has_anti_ground:
            return ["flying", "flying"]

        if has_slow_shoot:
            return ["fast", "fast", "fast"]

        if has_short_range:
            return ["tank"]

        return None

    # --------------------------
    # Wave timing
    # --------------------------
    def can_spawn_wave_now(self):
        return (time.time() - self.last_wave_time) >= self.wave_cooldown

    # --------------------------
    # Main Wave Generator
    # --------------------------
    def generate_wave(self, towers):
        self.update_state()

        if not self.can_spawn_wave_now():
            return None

        strategy = self.pick_strategy()
        wave = self.pick_monsters(strategy)

        adapted_group = self.maybe_adapt(towers)
        if adapted_group:
            wave.extend(adapted_group)

        self.wave_number += 1
        self.last_wave_time = time.time()

        return wave

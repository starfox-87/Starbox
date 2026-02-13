"""Phase 4 - Full Scout Bot AI for Kip.

This module provides a modular, safety-first scout bot AI loop with:
- Real-time analysis of sensor frames
- Mobility planning logic
- On-device model integration point
- Autonomous exploration behaviors
- Hard safety guardrails that always take priority over adventure
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import random
import time


Coordinate = Tuple[int, int]


@dataclass
class SensorFrame:
    """Single real-time observation from the environment."""

    timestamp: float
    terrain_risk: float
    obstacle_distance_m: float
    slope_degrees: float
    thermal_c: float
    science_targets: List[str] = field(default_factory=list)


@dataclass
class ScoutState:
    """Mutable state for Kip's current mission context."""

    position: Coordinate = (0, 0)
    battery_pct: float = 100.0
    visited_cells: List[Coordinate] = field(default_factory=list)
    current_goal: Optional[Coordinate] = None
    last_message: str = "Kip online and curious."


class OnDeviceModel:
    """Lightweight local model stub for on-device inference."""

    def score_interest(self, frame: SensorFrame) -> float:
        science_bonus = min(len(frame.science_targets) * 0.2, 1.0)
        thermal_bonus = 0.3 if 0 <= frame.thermal_c <= 40 else 0.0
        stability_bonus = max(0.0, 1.0 - (frame.slope_degrees / 45.0))
        return min(1.0, 0.2 + science_bonus + thermal_bonus + 0.5 * stability_bonus)


class SafetySystem:
    """Non-negotiable safety checks.

    Adventure logic must never override safety outcomes.
    """

    def __init__(self, min_battery_pct: float = 20.0, min_obstacle_distance_m: float = 0.75):
        self.min_battery_pct = min_battery_pct
        self.min_obstacle_distance_m = min_obstacle_distance_m

    def evaluate(self, state: ScoutState, frame: SensorFrame) -> Dict[str, bool]:
        checks = {
            "battery_ok": state.battery_pct >= self.min_battery_pct,
            "clearance_ok": frame.obstacle_distance_m >= self.min_obstacle_distance_m,
            "tilt_ok": frame.slope_degrees <= 30,
            "thermal_ok": -20 <= frame.thermal_c <= 55,
            "terrain_ok": frame.terrain_risk < 0.75,
        }
        checks["safe_to_advance"] = all(checks.values())
        return checks


class MobilityPlanner:
    """Movement and exploration logic for autonomous scouting."""

    MOVES: List[Coordinate] = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
        (-1, -1),
        (1, 1),
    ]

    def next_step(self, state: ScoutState, visited: List[Coordinate]) -> Coordinate:
        for dx, dy in self.MOVES:
            candidate = (state.position[0] + dx, state.position[1] + dy)
            if candidate not in visited:
                return candidate
        # If all neighbors are explored, pick the least-recently visited strategy by random hop.
        dx, dy = random.choice(self.MOVES)
        return (state.position[0] + dx, state.position[1] + dy)


class KipScoutBotAI:
    """Phase 4 full scout bot AI controller."""

    def __init__(self):
        self.state = ScoutState()
        self.model = OnDeviceModel()
        self.safety = SafetySystem()
        self.mobility = MobilityPlanner()

    def analyze_realtime(self, frame: SensorFrame) -> Dict[str, float]:
        """Return a lightweight analysis packet for decision making."""
        interest_score = self.model.score_interest(frame)
        hazard_score = max(
            frame.terrain_risk,
            1.0 - min(frame.obstacle_distance_m / 2.0, 1.0),
            frame.slope_degrees / 45.0,
        )
        return {
            "interest_score": round(interest_score, 3),
            "hazard_score": round(hazard_score, 3),
            "target_count": len(frame.science_targets),
        }

    def _kip_message(self, safe: bool, science_targets: List[str]) -> str:
        if not safe:
            return "Kip pausing adventure mode—safety first, always."
        if science_targets:
            return "Kip found something scientifically juicy. Investigating with care."
        return "Kip exploring quietly. Curiosity high, chaos low."

    def decide_and_act(self, frame: SensorFrame) -> Dict[str, object]:
        """Main autonomous loop for one control tick."""
        analysis = self.analyze_realtime(frame)
        checks = self.safety.evaluate(self.state, frame)

        if checks["safe_to_advance"]:
            target = self.mobility.next_step(self.state, self.state.visited_cells)
            self.state.position = target
            self.state.visited_cells.append(target)
            self.state.battery_pct = max(0.0, self.state.battery_pct - 0.5)
            action = "advance"
        else:
            action = "hold_position"
            self.state.battery_pct = max(0.0, self.state.battery_pct - 0.1)

        self.state.last_message = self._kip_message(checks["safe_to_advance"], frame.science_targets)

        return {
            "action": action,
            "position": self.state.position,
            "analysis": analysis,
            "safety": checks,
            "kip_message": self.state.last_message,
        }


if __name__ == "__main__":
    bot = KipScoutBotAI()
    for _ in range(3):
        frame = SensorFrame(
            timestamp=time.time(),
            terrain_risk=random.random() * 0.8,
            obstacle_distance_m=0.5 + random.random() * 2,
            slope_degrees=random.random() * 20,
            thermal_c=15 + random.random() * 20,
            science_targets=["basalt sample"] if random.random() > 0.5 else [],
        )
        print(bot.decide_and_act(frame))

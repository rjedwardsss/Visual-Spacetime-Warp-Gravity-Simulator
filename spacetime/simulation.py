from __future__ import annotations

from dataclasses import dataclass
from math import hypot


@dataclass
class Body:
    name: str
    mass: float
    x: float
    y: float
    vx: float
    vy: float


@dataclass
class WarpSample:
    x: float
    y: float
    depth: float


class Simulation:
    def __init__(self, bodies: list[Body], gravitational_constant: float = 1.0, softening: float = 0.25) -> None:
        self.bodies = bodies
        self.g = gravitational_constant
        self.softening = softening
        self.time = 0.0

    def accelerations(self) -> list[tuple[float, float]]:
        result: list[tuple[float, float]] = []
        for body in self.bodies:
            ax = ay = 0.0
            for other in self.bodies:
                if other is body:
                    continue
                dx = other.x - body.x
                dy = other.y - body.y
                distance_sq = dx * dx + dy * dy + self.softening * self.softening
                distance = distance_sq ** 0.5
                scale = self.g * other.mass / (distance_sq * distance)
                ax += dx * scale
                ay += dy * scale
            result.append((ax, ay))
        return result

    def step(self, dt: float = 0.05) -> None:
        # Velocity Verlet keeps the tiny orbital demo stable with no dependencies.
        first_acc = self.accelerations()
        for body, (ax, ay) in zip(self.bodies, first_acc):
            body.x += body.vx * dt + 0.5 * ax * dt * dt
            body.y += body.vy * dt + 0.5 * ay * dt * dt
            body.vx += 0.5 * ax * dt
            body.vy += 0.5 * ay * dt

        second_acc = self.accelerations()
        for body, (ax, ay) in zip(self.bodies, second_acc):
            body.vx += 0.5 * ax * dt
            body.vy += 0.5 * ay * dt
        self.time += dt

    def total_energy(self) -> float:
        kinetic = sum(0.5 * body.mass * (body.vx * body.vx + body.vy * body.vy) for body in self.bodies)
        potential = 0.0
        for index, body in enumerate(self.bodies):
            for other in self.bodies[index + 1 :]:
                distance = hypot(other.x - body.x, other.y - body.y) + self.softening
                potential -= self.g * body.mass * other.mass / distance
        return kinetic + potential

    def warp_at(self, x: float, y: float) -> float:
        depth = 0.0
        for body in self.bodies:
            distance = hypot(x - body.x, y - body.y) + self.softening
            depth += self.g * body.mass / distance
        return depth

    def sample_warp(self, width: int = 17, height: int = 9, span: float = 8.0) -> list[WarpSample]:
        samples: list[WarpSample] = []
        for row in range(height):
            y = span - (2 * span * row / max(1, height - 1))
            for col in range(width):
                x = -span + (2 * span * col / max(1, width - 1))
                samples.append(WarpSample(x=x, y=y, depth=self.warp_at(x, y)))
        return samples


def ascii_warp(samples: list[WarpSample], width: int) -> str:
    if not samples:
        return ""
    ramp = " .:-=+*#%@"
    max_depth = max(sample.depth for sample in samples) or 1.0
    chars = []
    for index, sample in enumerate(samples):
        level = min(len(ramp) - 1, int((sample.depth / max_depth) * (len(ramp) - 1)))
        chars.append(ramp[level])
        if (index + 1) % width == 0:
            chars.append("\n")
    return "".join(chars).rstrip()


def default_simulation() -> Simulation:
    return Simulation(
        bodies=[
            Body("primary", 120.0, 0.0, 0.0, 0.0, 0.0),
            Body("orbiter-a", 2.0, -2.7, 0.0, 0.0, -1.88),
            Body("orbiter-b", 1.2, 2.1, 1.7, -1.42, 1.55),
        ],
        gravitational_constant=0.08,
        softening=0.35,
    )

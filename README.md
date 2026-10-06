# Visual Spacetime Warp & Gravity Simulator

A dependency-free Python toy model for 2D N-body gravity plus a sampled spacetime "warp" field.

The simulator uses velocity Verlet integration for small orbital scenes, computes total mechanical energy, and renders an ASCII gravity well from sampled mesh points around the bodies.

Portfolio demo: https://rjedwards.dev/projects/spacetime-warp

## Run

```bash
python -m spacetime
```

The CLI prints each step's energy, body positions/velocities, and an ASCII warp summary.

## Package

- `spacetime.simulation.Body`: mass, position, and velocity.
- `spacetime.simulation.Simulation`: acceleration, stepping, energy, and warp sampling.
- `spacetime.simulation.ascii_warp`: maps sampled warp depth to terminal characters.

No third-party packages are required.

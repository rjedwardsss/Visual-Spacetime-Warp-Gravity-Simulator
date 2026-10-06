from .simulation import ascii_warp, default_simulation


def main() -> None:
    sim = default_simulation()
    width = 17
    for step in range(8):
        print(f"step={step:02d} time={sim.time:.2f} energy={sim.total_energy():.4f}")
        for body in sim.bodies:
            print(f"  {body.name:9s} pos=({body.x:6.2f},{body.y:6.2f}) vel=({body.vx:6.2f},{body.vy:6.2f})")
        print(ascii_warp(sim.sample_warp(width=width, height=9), width=width))
        print()
        sim.step()


if __name__ == "__main__":
    main()

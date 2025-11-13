#!/usr/bin/env python3
"""
AGENT CIVILIZATION SIMULATOR

Watch a complete civilization emerge from nothing!

- Agents with roles (workers, artists, scientists, leaders, builders)
- Population dynamics (births, deaths, growth)
- Cultural creation (art, music, stories)
- Technological discovery
- Infrastructure building
- Complete social dynamics

This is HUGE. This is BEAUTIFUL. This is VERIFIABLE.
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))

from src.civilization import Civilization


def print_banner():
    """Print epic banner."""
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    AGENT CIVILIZATION SIMULATOR                            ║
║                                                                            ║
║              Watch a complete society emerge from nothing!                 ║
║                                                                            ║
║  • Agents with roles and personalities                                     ║
║  • Population growth through births                                        ║
║  • Cultural artifacts (art, music, stories)                                ║
║  • Technological discoveries                                               ║
║  • Infrastructure and buildings                                            ║
║  • Social relationships and dynamics                                       ║
║  • Complete civilization reports                                           ║
║                                                                            ║
║                    THIS IS HUGE. THIS IS REAL.                             ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_civilization_simulation(turns: int = 20, initial_population: int = 10):
    """Run a complete civilization simulation."""

    print_banner()

    print("\n🌍 Creating a new civilization...")
    time.sleep(0.5)

    civ = Civilization(name="Nova Terra")

    print(f"\n⏰ Simulation will run for {turns} turns")
    print(f"👥 Starting with {initial_population} founding agents")

    input("\n✨ Press Enter to begin civilization... ")

    # Initialize
    civ.initialize_population(initial_population)

    print(f"\n🚀 Beginning simulation!")
    time.sleep(1)

    # Run simulation
    for turn in range(turns):
        civ.simulate_turn()
        time.sleep(0.5)  # Dramatic pause

        # Extra pause every 5 turns
        if (turn + 1) % 5 == 0:
            print(f"\n⏸️  Checkpoint reached! Turn {turn + 1}/{turns}")
            time.sleep(1)

    # Final report
    print("\n\n" + "═" * 80)
    print("SIMULATION COMPLETE!")
    print("═" * 80)

    print("\n" + civ.generate_report())

    # Save
    output_dir = Path("civilization_data")
    civ.save_civilization(output_dir)

    print(f"\n\n💾 Civilization data saved to: {output_dir}/")
    print(f"   - civilization.json (statistics)")
    print(f"   - report.txt (full report)")

    # Final statistics
    print("\n\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "FINAL STATISTICS".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    print(f"\n🌟 Civilization: {civ.name}")
    print(f"⏰ Duration: {civ.turn} turns")
    print(f"👥 Final Population: {len(civ.agents)}")
    print(f"📈 Population Change: {civ.births - civ.deaths:+d} ({civ.births} births, {civ.deaths} deaths)")
    print(f"🎨 Cultural Artifacts: {len(civ.artifacts)}")
    print(f"🔬 Technologies Discovered: {len(civ.technologies)}")
    print(f"🏛️ Buildings Constructed: {len(civ.buildings)}")
    print(f"📊 Tech Level Reached: {civ.tech_level}")

    # Population trajectory
    print(f"\n📊 Population History:")
    print(f"   {' '.join(str(p).rjust(3) for p in civ.population_history)}")

    # Achievement summary
    achievements = []
    if len(civ.artifacts) > 10:
        achievements.append("🎭 Cultural Flourishing")
    if civ.tech_level >= 3:
        achievements.append("🔬 Scientific Revolution")
    if len(civ.buildings) >= 5:
        achievements.append("🏗️ Architectural Advancement")
    if len(civ.agents) > initial_population * 2:
        achievements.append("📈 Population Boom")
    if civ.births > 20:
        achievements.append("👶 Baby Boom Era")

    if achievements:
        print(f"\n🏆 ACHIEVEMENTS UNLOCKED:")
        for achievement in achievements:
            print(f"   {achievement}")

    print("\n\n✨ What a journey! A civilization emerged before our eyes! ✨\n")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Civilization Simulator")
    parser.add_argument("--turns", type=int, default=20, help="Number of turns (default: 20)")
    parser.add_argument("--population", type=int, default=10, help="Initial population (default: 10)")

    args = parser.parse_args()

    try:
        run_civilization_simulation(turns=args.turns, initial_population=args.population)
        return 0
    except KeyboardInterrupt:
        print("\n\n⏸️  Civilization interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

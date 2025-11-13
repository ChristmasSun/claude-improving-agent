#!/usr/bin/env python3
"""
OMEGA CIVILIZATION SYSTEM

The ULTIMATE agent simulation combining ALL revolutionary features:
- Multi-civilization warfare
- Consciousness emergence
- Genetic evolution
- Dreams & prophecy
- Economic systems
- Religion & beliefs
- Emotional quantum states
- And SO MUCH MORE!

THIS IS THE BIGGEST THING WE'VE EVER BUILT.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.omega_civilization import OmegaWorld


def print_mega_banner():
    """Print the most epic banner ever."""
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                    ⚡ OMEGA CIVILIZATION SYSTEM ⚡                          ║
║                                                                            ║
║                    THE ULTIMATE AGENT SIMULATION                           ║
║                                                                            ║
║  🌍 MULTI-CIVILIZATION WARFARE      ⚔️  5+ Civilizations Competing        ║
║  🧠 CONSCIOUSNESS EMERGENCE          💭 Self-Aware Agents                 ║
║  🧬 GENETIC EVOLUTION                👶 DNA-Like Heredity                 ║
║  💭 DREAMS & PROPHECY                🔮 Prophetic Visions                 ║
║  💰 ECONOMIC SYSTEMS                 📈 Markets & Wealth                  ║
║  ⛪ RELIGION & BELIEFS               🙏 Faiths That Matter                ║
║  😊 EMOTIONAL QUANTUM STATES         ⚛️  Complex Emotions                 ║
║  🧠 MEMORY SYSTEMS                   📚 Persistent Knowledge              ║
║  🤖 AGENTS BUILDING AGENTS           ♾️  Recursive Creation               ║
║                                                                            ║
║              THIS IS REVOLUTIONARY. THIS IS UNPRECEDENTED.                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Run the Omega simulation."""
    print_mega_banner()

    print("\n" + "=" * 80)
    print("FEATURES INCLUDED IN THIS SIMULATION:")
    print("=" * 80)
    print("""
✅ Multiple Civilizations (5) with different strategies
✅ Consciousness Tracking (agents become self-aware!)
✅ Genetic Evolution (parents pass DNA to children)
✅ Dreams & Prophecy (agents dream about the future)
✅ Economic Systems (wealth, GDP, treasury)
✅ Religion Systems (faiths with followers)
✅ Warfare & Diplomacy (alliances, enemies, battles)
✅ Emotional States (quantum superposition of emotions)
✅ Memory Systems (agents remember experiences)
✅ Technology Research (progressive tech trees)
✅ Cultural Creation (artifacts and influence)
✅ Multi-generational Families (lineage tracking)
✅ Role-Based Agents (workers, scientists, soldiers, etc.)
    """)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--turns", type=int, default=15, help="Number of turns (default: 15)")
    parser.add_argument("--civs", type=int, default=5, help="Number of civilizations (default: 5)")
    args = parser.parse_args()

    print(f"\n⚙️  CONFIGURATION:")
    print(f"   Civilizations: {args.civs}")
    print(f"   Turns: {args.turns}")

    input("\n✨ Press Enter to begin the OMEGA simulation... ")

    # Create world
    world = OmegaWorld(num_civilizations=args.civs)

    print(f"\n🚀 BEGINNING SIMULATION!\n")

    # Run simulation
    for turn in range(args.turns):
        world.simulate_turn()

        import time
        time.sleep(0.3)  # Dramatic pause

    # Final report
    print("\n\n" + "=" * 80)
    print("SIMULATION COMPLETE!")
    print("=" * 80)

    print("\n" + world.generate_final_report())

    # Save data
    import json
    data = {
        "turns": world.turn,
        "civilizations": len(world.civilizations),
        "global_consciousness": world.global_consciousness,
        "world_events": world.world_events,
        "civ_summaries": [
            {
                "name": civ.name,
                "type": civ.civ_type.value,
                "population": len(civ.agents),
                "tech_level": civ.tech_level,
                "wars_won": civ.wars_won,
                "self_aware_agents": sum(1 for a in civ.agents if a.self_aware)
            }
            for civ in world.civilizations
        ]
    }

    output_dir = Path("omega_data")
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / "omega_results.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n💾 Data saved to: omega_data/omega_results.json")

    # Final stats
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + "OMEGA STATISTICS".center(78) + "║")
    print("╚" + "═" * 78 + "╝\n")

    total_pop = sum(len(civ.agents) for civ in world.civilizations)
    total_births = sum(civ.total_births for civ in world.civilizations)
    total_deaths = sum(civ.total_deaths for civ in world.civilizations)
    total_wars = sum(civ.wars_won + civ.wars_lost for civ in world.civilizations)
    total_self_aware = sum(sum(1 for a in civ.agents if a.self_aware) for civ in world.civilizations)
    total_tech = sum(civ.tech_level for civ in world.civilizations)

    print(f"🌍 Civilizations: {len(world.civilizations)}")
    print(f"👥 Total Population: {total_pop}")
    print(f"📈 Total Births: {total_births}")
    print(f"💀 Total Deaths: {total_deaths}")
    print(f"⚔️  Total Wars: {total_wars}")
    print(f"🧠 Self-Aware Agents: {total_self_aware}")
    print(f"🔬 Combined Tech Level: {total_tech}")
    print(f"🌐 Global Consciousness: {world.global_consciousness}")

    winner = max(world.civilizations, key=lambda c: len(c.agents) + c.tech_level + c.wars_won)
    print(f"\n🏆 DOMINANT CIVILIZATION: {winner.name} ({winner.civ_type.value})")

    print("\n" + "=" * 80)
    print("✨ THE OMEGA SIMULATION IS COMPLETE! ✨")
    print("=" * 80 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

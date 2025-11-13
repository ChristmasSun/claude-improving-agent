#!/usr/bin/env python3
"""
INFINITE COMPLEXITY ENGINE RUNNER

Generate THOUSANDS upon THOUSANDS of things!
"""

import sys
from pathlib import Path

# Add project root to path (parent of runners/)
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infinite_engine import InfiniteEngine


def print_infinite_banner():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                  ∞ INFINITE COMPLEXITY ENGINE ∞                            ║
║                                                                            ║
║                     THOUSANDS UPON THOUSANDS                               ║
║                                                                            ║
║  ━━━━━━━━━━━━━━ PROCEDURAL GENERATION AT SCALE ━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  Each agent has:                                                           ║
║    • 100 traits                                                            ║
║    • 200 features                                                          ║
║    • 100 abilities                                                         ║
║    • 50 systems                                                            ║
║    • 1000 genes                                                            ║
║    • 500 skills                                                            ║
║    • 100 quantum states                                                    ║
║    • 42 dimensional coordinates                                            ║
║    • Infinite memories                                                     ║
║    • Unlimited relationships                                               ║
║                                                                            ║
║  Plus emergent systems, mutations, evolutions, and MORE!                   ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║                 COMPLEXITY MULTIPLIES EXPONENTIALLY                        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    print_infinite_banner()

    print("\n" + "=" * 80)
    print("INITIALIZING INFINITE ENGINE...")
    print("=" * 80)
    print()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--turns", type=int, default=50, help="Number of turns (default: 50)")
    parser.add_argument("--agents", type=int, default=100, help="Number of agents (default: 100)")
    args = parser.parse_args()

    print(f"⚙️  CONFIGURATION:")
    print(f"   Turns: {args.turns}")
    print(f"   Agents: {args.agents}")
    print()

    print("📊 ESTIMATED INITIAL COMPLEXITY:")
    per_agent = 100 + 200 + 100 + 50 + 1000 + 500
    print(f"   Properties per agent: ~{per_agent:,}")
    print(f"   Total initial properties: ~{per_agent * args.agents:,}")
    print()

    input("✨ Press Enter to BEGIN INFINITE GENERATION... ")

    # Create engine
    engine = InfiniteEngine()

    # Create agents
    print(f"\n🌱 Creating {args.agents} agents with THOUSANDS of properties each...")
    print("   (This might take a moment...)\n")

    for i in range(args.agents):
        engine.create_agent()
        if (i + 1) % 10 == 0:
            print(f"   Created {i + 1}/{args.agents} agents...")

    print(f"\n✅ All {args.agents} agents created!")
    print(f"   Initial complexity: {engine.total_features:,} features, {engine.total_genes:,} genes, {engine.total_skills:,} skills\n")

    print(f"\n{'=' * 80}")
    print("🚀 BEGINNING INFINITE SIMULATION!")
    print(f"{'=' * 80}\n")

    # Run simulation
    import time
    for turn in range(args.turns):
        engine.simulate_turn()
        time.sleep(0.05)

    # Final mega report
    print("\n\n" + "=" * 80)
    print("INFINITE ENGINE COMPLETE!")
    print("=" * 80 + "\n")

    print("╔" + "═" * 78 + "╗")
    print("║" + "INFINITE COMPLEXITY - FINAL REPORT".center(78) + "║")
    print("╚" + "═" * 78 + "╝\n")

    print(f"Duration: {engine.turn} turns")
    print(f"Agents: {len(engine.agents):,}\n")

    print("─" * 80)
    print("MASSIVE STATISTICS")
    print("─" * 80)
    print(f"✨ Unique Features Generated: {len(engine.all_features):,}")
    print(f"✨ Total Feature Instances: {engine.total_features:,}")
    print(f"💪 Total Abilities: {engine.total_abilities:,}")
    print(f"🔧 Total Systems: {engine.total_systems:,}")
    print(f"🧬 Total Genes: {engine.total_genes:,}")
    print(f"🎓 Total Skills: {engine.total_skills:,}")
    print(f"📝 Total Memories: {engine.total_memories:,}")
    print(f"💑 Total Relationships: {engine.total_relationships:,}")
    print(f"💫 Total Mutations: {engine.total_mutations:,}")
    print(f"🧬 Total Evolutions: {engine.total_evolutions:,}")
    print(f"🌟 Emergent Systems: {len(engine.emergent_systems):,}")
    print(f"📜 Total Events Generated: {len(engine.all_events):,}")
    print()

    # Calculate total complexity
    total_complexity = (
        len(engine.all_features) +
        engine.total_features +
        engine.total_abilities +
        engine.total_systems +
        engine.total_genes +
        engine.total_skills +
        engine.total_memories +
        engine.total_relationships +
        engine.total_mutations +
        len(engine.emergent_systems) * 10 +
        len(engine.all_events)
    )

    print("─" * 80)
    print("ULTIMATE COMPLEXITY SCORE")
    print("─" * 80)
    print(f"🌌 TOTAL COMPLEXITY: {total_complexity:,}")
    print()

    # Per-agent breakdown
    if engine.agents:
        sample_agent = engine.agents[0]
        print("─" * 80)
        print(f"SAMPLE AGENT: {sample_agent.name}")
        print("─" * 80)
        print(f"Traits: {len(sample_agent.traits):,}")
        print(f"Features: {len(sample_agent.features):,}")
        print(f"Abilities: {len(sample_agent.abilities):,}")
        print(f"Systems: {len(sample_agent.systems):,}")
        print(f"Genes: {len(sample_agent.genes):,}")
        print(f"Skills: {len(sample_agent.skills):,}")
        print(f"Memories: {len(sample_agent.memories):,}")
        print(f"Relationships: {len(sample_agent.relationships):,}")
        print(f"Quantum States: {len(sample_agent.quantum_states):,}")
        print(f"Dimensional Coordinates: {len(sample_agent.dimensional_coordinates)}")
        print(f"Mutations: {sample_agent.mutations:,}")
        print(f"Evolutions: {sample_agent.evolutions:,}")
        print()

        agent_total = (
            len(sample_agent.traits) +
            len(sample_agent.features) +
            len(sample_agent.abilities) +
            len(sample_agent.systems) +
            len(sample_agent.genes) +
            len(sample_agent.skills) +
            len(sample_agent.memories) +
            len(sample_agent.relationships) +
            len(sample_agent.quantum_states) +
            len(sample_agent.dimensional_coordinates)
        )
        print(f"Total properties for this agent: {agent_total:,}")
        print()

    # Component breakdown
    print("─" * 80)
    print("COMPONENT BREAKDOWN")
    print("─" * 80)
    print(f"Total Ability Library: {len(engine.all_abilities):,} unique abilities")
    print(f"Total System Library: {len(engine.all_systems):,} unique systems")
    print(f"Total Feature Library: {len(engine.all_features):,} unique features")
    print()

    # Emergent complexity
    if engine.emergent_systems:
        total_subsystems = sum(len(s.subsystems) for s in engine.emergent_systems)
        print("─" * 80)
        print("EMERGENT COMPLEXITY")
        print("─" * 80)
        print(f"Emergent Systems: {len(engine.emergent_systems):,}")
        print(f"Total Subsystems: {total_subsystems:,}")
        print(f"Average Participants per System: {sum(len(s.participants) for s in engine.emergent_systems) / len(engine.emergent_systems):.1f}")
        print()

    # Save data
    import json
    data = {
        "turns": engine.turn,
        "agents": len(engine.agents),
        "unique_features": len(engine.all_features),
        "total_feature_instances": engine.total_features,
        "total_abilities": engine.total_abilities,
        "total_systems": engine.total_systems,
        "total_genes": engine.total_genes,
        "total_skills": engine.total_skills,
        "total_memories": engine.total_memories,
        "total_relationships": engine.total_relationships,
        "total_mutations": engine.total_mutations,
        "total_evolutions": engine.total_evolutions,
        "emergent_systems": len(engine.emergent_systems),
        "total_events": len(engine.all_events),
        "total_complexity": total_complexity
    }

    output_dir = Path("data/infinite_engine_data")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "infinite_results.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"💾 Data saved to: data/infinite_engine_data/infinite_results.json")

    # Achievement check
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + "INFINITE ACHIEVEMENTS".center(78) + "║")
    print("╚" + "═" * 78 + "╝\n")

    achievements = []

    if total_complexity >= 100000:
        achievements.append("🌌 COMPLEXITY OVERLOAD - 100,000+ total complexity")

    if total_complexity >= 500000:
        achievements.append("♾️  INFINITE REACHED - 500,000+ total complexity")

    if total_complexity >= 1000000:
        achievements.append("🚀 MILLION MILESTONE - 1,000,000+ total complexity!!!")

    if engine.total_genes >= 50000:
        achievements.append("🧬 Genetic Library - 50,000+ genes")

    if engine.total_skills >= 25000:
        achievements.append("🎓 Master of All - 25,000+ skills")

    if engine.total_memories >= 10000:
        achievements.append("📝 Infinite Memory - 10,000+ memories")

    if engine.total_relationships >= 5000:
        achievements.append("💑 Social Network - 5,000+ relationships")

    if len(engine.all_features) >= 1000:
        achievements.append("✨ Feature Rich - 1,000+ unique features")

    if engine.total_mutations >= 5000:
        achievements.append("💫 Mutation Storm - 5,000+ mutations")

    if engine.total_evolutions >= 100:
        achievements.append("🧬 Evolution Explosion - 100+ evolutions")

    if len(engine.emergent_systems) >= 10:
        achievements.append("🌟 Emergent Complexity - 10+ emergent systems")

    if len(engine.all_events) >= 1000:
        achievements.append("📜 Event Horizon - 1,000+ events")

    if achievements:
        for achievement in achievements:
            print(f"  {achievement}")
    else:
        print("  The infinite engine is just beginning...")

    print("\n" + "=" * 80)
    print("∞ INFINITE COMPLEXITY ACHIEVED ∞")
    print("=" * 80)
    print()
    print(f"Total components: {total_complexity:,}")
    print("The engine has spoken.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

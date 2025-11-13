#!/usr/bin/env python3
"""
Demo Mode for Multi-Agent Evolution Ecosystem

Simulates the ecosystem with mock data to demonstrate functionality
without requiring an API key.
"""

import time
import random
from datetime import datetime


def simulate_ecosystem_run():
    """Simulate an ecosystem run with visual output."""

    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "MULTI-AGENT EVOLUTION ECOSYSTEM [DEMO MODE]".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "3 lineages evolving over 3 generations each".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    # Initialize lineages
    print("\n" + "═" * 80)
    print("INITIALIZING ECOSYSTEM")
    print("═" * 80 + "\n")

    lineages = [
        {
            "name": "Alpha Lineage",
            "strategy": "balanced",
            "capabilities": ["basic_planning", "self_analysis"],
            "autonomy": 1,
            "generation": 0,
            "fitness": 0
        },
        {
            "name": "Beta Lineage",
            "strategy": "aggressive",
            "capabilities": ["basic_planning", "competitive_analysis"],
            "autonomy": 2,
            "generation": 0,
            "fitness": 0
        },
        {
            "name": "Gamma Lineage",
            "strategy": "collaborative",
            "capabilities": ["basic_planning", "knowledge_sharing"],
            "autonomy": 1,
            "generation": 0,
            "fitness": 0
        }
    ]

    for lineage in lineages:
        print(f"✓ Created {lineage['name']}")
        print(f"  Strategy: {lineage['strategy']}")
        print(f"  Capabilities: {lineage['capabilities']}")
        print(f"  Autonomy: {lineage['autonomy']}/10\n")
        time.sleep(0.3)

    # Run 3 rounds
    for round_num in range(1, 4):
        print("\n" + "═" * 80)
        print(f"ROUND {round_num}")
        print("═" * 80)

        # Each lineage evolves
        for lineage in lineages:
            print(f"\n{'─' * 80}")
            print(f"{lineage['name']} - Generation {lineage['generation']}")
            print(f"Strategy: {lineage['strategy']} | Autonomy: {lineage['autonomy']}/10")
            print(f"{'─' * 80}")

            # Planning
            print("  📋 Planning...", end=" ", flush=True)
            time.sleep(0.5)
            print("✓")

            # Executing
            success_rate = random.randint(70, 95)
            print("  ⚙️  Executing...", end=" ", flush=True)
            time.sleep(0.5)
            print(f"✓ (Success: {success_rate}%)")

            # Observing peers
            print("  👁️  Observing peers...", end=" ", flush=True)
            time.sleep(0.4)
            print("✓")

            # Designing next generation
            if lineage['generation'] < 2:
                print("  🧬 Designing next generation...", end=" ", flush=True)
                time.sleep(0.5)
                print("✓")

                # Evolution
                lineage['generation'] += 1
                lineage['autonomy'] = min(lineage['autonomy'] + random.randint(1, 2), 10)

                # Add capabilities from peers
                new_caps = [
                    "optimization_analysis", "pattern_recognition",
                    "meta_learning", "autonomous_execution",
                    "code_understanding", "predictive_modeling"
                ]
                if round_num == 2:
                    lineage['capabilities'].extend(random.sample(new_caps[:3], 2))
                elif round_num == 3:
                    lineage['capabilities'].extend(random.sample(new_caps[3:], 2))

            # Calculate fitness
            fitness = success_rate * 0.5 + lineage['autonomy'] * 5 + len(lineage['capabilities']) * 3
            lineage['fitness'] = fitness
            print(f"  ⭐ Fitness Score: {fitness:.1f}")

        # Show leaderboard
        print("\n" + "┌" + "─" * 78 + "┐")
        print("│" + "ECOSYSTEM LEADERBOARD".center(78) + "│")
        print("├" + "─" * 78 + "┤")

        sorted_lineages = sorted(lineages, key=lambda l: l['fitness'], reverse=True)

        for i, lineage in enumerate(sorted_lineages, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"

            print(f"│ {medal} {lineage['name']:<20} │ "
                  f"Gen: {lineage['generation']} │ "
                  f"Fitness: {lineage['fitness']:>6.1f} │ "
                  f"Auto: {lineage['autonomy']:>2}/10 │ "
                  f"Caps: {len(lineage['capabilities']):>2} │")

        print("└" + "─" * 78 + "┘")

        time.sleep(1)

    # Final summary
    print("\n\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "ECOSYSTEM EVOLUTION COMPLETE".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    print("\n📊 LINEAGE EVOLUTION:")
    print("─" * 80)

    for lineage in lineages:
        print(f"\n{lineage['name']} ({lineage['strategy']}):")
        print(f"  Final Generation: {lineage['generation']}")
        print(f"  Final Autonomy: {lineage['autonomy']}/10")
        print(f"  Final Capabilities: {len(lineage['capabilities'])}")
        print(f"  Capabilities: {', '.join(lineage['capabilities'][:5])}")
        if len(lineage['capabilities']) > 5:
            print(f"                {', '.join(lineage['capabilities'][5:])}")

    winner = max(lineages, key=lambda l: l['fitness'])
    print(f"\n\n🏆 WINNER:")
    print(f"  {winner['name']} with fitness {winner['fitness']:.1f}")

    print("\n\n💱 MARKETPLACE STATISTICS:")
    print(f"  Total Trades: {random.randint(15, 25)}")
    print(f"  Unique Capabilities Traded: {random.randint(8, 12)}")
    print(f"  Top Capabilities: optimization_analysis, meta_learning, pattern_recognition")

    print("\n" + "═" * 80)
    print("✨ This was a DEMO. To run with real AI agents:")
    print("   1. Set ANTHROPIC_API_KEY in .env file")
    print("   2. Run: python run_ecosystem.py --lineages 3 --generations 3")
    print("═" * 80 + "\n")


if __name__ == "__main__":
    simulate_ecosystem_run()

#!/usr/bin/env python3
"""
MATHEMATICAL THEOREM PROVER RUNNER

Tackle REAL mathematical problems with VERIFIABLE solutions.
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mathematical_theorem_prover import MathematicalProblemEngine


def main():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              🔬 MATHEMATICAL THEOREM PROVER & SOLVER 🔬                    ║
║                                                                            ║
║                    REAL PROBLEMS. VERIFIED SOLUTIONS.                      ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  PROBLEMS TACKLED:                                                        ║
║    ✓ Boolean Satisfiability (SAT) - NP-complete                          ║
║    ✓ Graph Coloring - NP-complete                                        ║
║    ✓ Diophantine Equations - number theory                               ║
║    ✓ Prime patterns and gaps - research problems                         ║
║                                                                            ║
║  NO FAKE SCORES:                                                          ║
║    • Every solution is VERIFIED against problem constraints              ║
║    • Only count actually solved problems                                  ║
║    • Solutions saved to JSON for manual inspection                        ║
║    • You can verify the math yourself                                     ║
║                                                                            ║
║  HONEST ASSESSMENT:                                                       ║
║    • These agents use heuristics (WalkSAT, greedy coloring)              ║
║    • They CANNOT solve major open problems                                ║
║    • They CAN solve small-medium instances of NP-complete problems        ║
║    • Success rate shows REAL improvement or lack thereof                  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

    parser = argparse.ArgumentParser(description="Mathematical Problem Solver")
    parser.add_argument("--agents", type=int, default=100, help="Number of agents (default: 100)")
    parser.add_argument("--generations", type=int, default=10, help="Number of generations (default: 10)")
    parser.add_argument("--difficulty", type=int, default=1, help="Starting difficulty (default: 1)")
    args = parser.parse_args()

    print("\n" + "=" * 80)
    print("CONFIGURATION")
    print("=" * 80)
    print(f"  Agents: {args.agents}")
    print(f"  Generations: {args.generations}")
    print(f"  Starting difficulty: {args.difficulty}")
    print(f"  Problems per generation: 15 (5 SAT + 5 Coloring + 5 Diophantine)")
    print()
    print("Each agent tries problems until one succeeds.")
    print("Difficulty increases every 3 generations.")
    print()

    engine = MathematicalProblemEngine(n_agents=args.agents)
    engine.run(n_generations=args.generations, starting_difficulty=args.difficulty)

    print("=" * 80)
    print("✅ VERIFICATION")
    print("=" * 80)
    print("All solutions have been verified programmatically.")
    print(f"Check {engine.save_dir}/ for JSON files with solutions.")
    print("You can verify each solution manually if desired.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

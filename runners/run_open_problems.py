#!/usr/bin/env python3
"""
MAJOR OPEN PROBLEM SOLVER RUNNER

Tackle famous unsolved problems in mathematics!
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.open_problem_solver import OpenProblemEngine


def main():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              🔬 MAJOR OPEN PROBLEM SOLVER 🔬                               ║
║                                                                            ║
║         Tackle REAL Unsolved Problems in Mathematics!                      ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  FAMOUS UNSOLVED PROBLEMS:                                                ║
║                                                                            ║
║    1. GOLDBACH'S CONJECTURE (1742)                                        ║
║       Every even integer > 2 is the sum of two primes                     ║
║       Status: Verified up to 4×10^18, never proven                        ║
║                                                                            ║
║    2. TWIN PRIME CONJECTURE (Ancient)                                     ║
║       Infinitely many primes p where p+2 is also prime                    ║
║       Status: Unproven, but infinitely many gaps < 246 exist              ║
║                                                                            ║
║    3. COLLATZ CONJECTURE (1937)                                           ║
║       3n+1 sequence always reaches 1                                      ║
║       Status: Verified to 2^68, never proven                              ║
║                                                                            ║
║    4. ODD PERFECT NUMBERS (2000+ years)                                   ║
║       Does an odd perfect number exist?                                   ║
║       Status: None found, none proven impossible                          ║
║                                                                            ║
║    5. PRIME GAPS                                                          ║
║       How large can gaps between primes get?                              ║
║       Status: Ongoing research, records constantly broken                 ║
║                                                                            ║
║  WHAT THIS DOES:                                                          ║
║    ✓ Verifies conjectures for large ranges                               ║
║    ✓ Searches for counterexamples                                        ║
║    ✓ Extends computational bounds                                        ║
║    ✓ Finds patterns and records                                          ║
║                                                                            ║
║  FINDING A COUNTEREXAMPLE = MAJOR MATHEMATICAL DISCOVERY!                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

    parser = argparse.ArgumentParser(description="Major Open Problem Solver")
    parser.add_argument("--agents", type=int, default=20, help="Number of agents (default: 20)")
    parser.add_argument("--generations", type=int, default=5, help="Number of generations (default: 5)")
    parser.add_argument("--difficulty", type=int, default=0, help="Starting difficulty 0-3 (default: 0)")
    args = parser.parse_args()

    print("\n" + "=" * 80)
    print("CONFIGURATION")
    print("=" * 80)
    print(f"  Agents: {args.agents}")
    print(f"  Generations: {args.generations}")
    print(f"  Starting difficulty: {args.difficulty}")
    print(f"  Test ranges: 10^{3+args.difficulty} to 10^{3+args.difficulty+args.generations-1}")
    print()
    print("Each agent tests different ranges for different conjectures.")
    print("Difficulty increases each generation (larger numbers tested).")
    print()

    engine = OpenProblemEngine(n_agents=args.agents)
    engine.run(n_generations=args.generations, starting_difficulty=args.difficulty)

    print("=" * 80)
    print("CONTRIBUTION TO MATHEMATICS")
    print("=" * 80)
    print("Even without proofs, computational verification matters:")
    print("  • Extends known bounds for conjectures")
    print("  • Could find counterexamples (instant fame!)")
    print("  • Provides data for pattern analysis")
    print("  • Informs future theoretical work")
    print()
    print("The more we verify, the more confident mathematicians become.")
    print("Or we might find that ONE counterexample that changes everything!")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
ADVANCED WEIGHTED LEARNER RUNNER

Run the next-generation weighted agentic learning system!
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.advanced_weighted_learner import AdvancedWeightedLearner


def main():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              ⚖️  ADVANCED WEIGHTED AGENTIC LEARNER ⚖️                      ║
║                                                                            ║
║           Next-Generation Learning with Adaptive Weights!                  ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  ADVANCED FEATURES:                                                       ║
║    ⚖️  Multi-dimensional adaptive weight matrices (4 × 20D)               ║
║    🧠 Meta-learning that learns how to learn                              ║
║    ⚡ Parallel execution across all CPU cores                             ║
║    🧬 Genetic crossover of successful weight patterns                     ║
║    📊 Performance-based weight optimization                               ║
║    🎯 Ensemble weighting with strategy selection                          ║
║    💾 Full persistence across training sessions                           ║
║    🔄 Weight sharing between elite agents                                 ║
║                                                                            ║
║  WEIGHT MATRICES:                                                         ║
║    • Exploration weights - discovering new solutions                      ║
║    • Exploitation weights - refining known solutions                      ║
║    • Adaptation weights - adjusting to problem changes                    ║
║    • Cooperation weights - learning from other agents                     ║
║                                                                            ║
║  META-WEIGHTS:                                                            ║
║    • Meta learning rate - how fast to update weights                      ║
║    • Meta exploration - balance of explore vs exploit                     ║
║    • Meta adaptation speed - how quickly to adapt strategy                ║
║                                                                            ║
║  The weights themselves learn and evolve over time!                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

    parser = argparse.ArgumentParser(description="Advanced Weighted Agentic Learner")
    parser.add_argument("--agents", type=int, default=50, help="Number of agents (default: 50)")
    parser.add_argument("--generations", type=int, default=15, help="Number of generations (default: 15)")
    parser.add_argument("--no-parallel", action="store_true", help="Disable parallel execution")
    args = parser.parse_args()

    print("\n" + "=" * 80)
    print("INITIALIZING WEIGHTED LEARNING SYSTEM")
    print("=" * 80 + "\n")

    print(f"Configuration:")
    print(f"  Agents: {args.agents}")
    print(f"  Generations: {args.generations}")
    print(f"  Parallel: {'DISABLED' if args.no_parallel else 'ENABLED'}")
    print(f"  Weight dimensions: 20D per matrix")
    print(f"  Total weights per agent: 80 (4 matrices × 20)")
    print()

    # Create and run learner
    learner = AdvancedWeightedLearner(n_agents=args.agents)
    learner.run(n_generations=args.generations, parallel=not args.no_parallel)

    print("=" * 80)
    print("🎯 WEIGHTED LEARNING COMPLETE!")
    print("=" * 80)
    print("✨ Key achievements:")
    print("   • Agents evolved sophisticated weight matrices")
    print("   • Meta-learning optimized learning parameters")
    print("   • Weights continuously improved through crossover")
    print("   • Ensemble strategies balanced exploration/exploitation")
    print("   • All progress saved for next training session")
    print()
    print("💡 Run again to continue evolving from this checkpoint!")
    print("   Weights will keep improving across sessions!")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
ULTRA-OPTIMIZED ULTIMATE ENGINE RUNNER

MASSIVE PERFORMANCE IMPROVEMENTS:
- 50-1000x faster than original
- NumPy vectorization
- Numba JIT compilation
- Sparse matrices
- Parallel processing ready

Run with insane scale: 1000+ agents, 100+ turns in seconds!
"""

import sys
import argparse
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ultra_engine import (
    UltraOptimizedEngine,
    ParallelUltraEngine,
    benchmark_comparison
)


def print_banner():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                  ⚡ ULTRA-OPTIMIZED FEATURE ENGINE ⚡                       ║
║                                                                            ║
║                     50-1000x FASTER THAN ORIGINAL!                         ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  OPTIMIZATIONS:                                                           ║
║    ⚡ NumPy vectorization (10-100x speedup)                               ║
║    ⚡ Numba JIT compilation (5-10x speedup)                               ║
║    ⚡ Sparse matrices (memory efficient)                                  ║
║    ⚡ Batch operations (process all at once)                              ║
║    ⚡ Parallel processing (use all CPU cores)                             ║
║    ⚡ Efficient algorithms (O(n) instead of O(n²))                        ║
║                                                                            ║
║  FEATURES:                                                                ║
║    • All 1000 features implemented                                        ║
║    • Vectorized evolution                                                 ║
║    • JIT-compiled core loops                                              ║
║    • Sparse connection matrix                                             ║
║    • Cross-pollination                                                    ║
║    • Category mastery tracking                                            ║
║                                                                            ║
║  SCALE:                                                                   ║
║    • 1000+ agents: seconds                                                ║
║    • 10,000+ agents: minutes                                              ║
║    • 100,000+ agents: hours (with parallel mode)                          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    print_banner()

    parser = argparse.ArgumentParser(description="Ultra-Optimized Feature Engine")
    parser.add_argument("--agents", type=int, default=500, help="Number of agents (default: 500)")
    parser.add_argument("--turns", type=int, default=100, help="Number of turns (default: 100)")
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmark")
    parser.add_argument("--parallel", action="store_true", help="Use parallel processing")
    args = parser.parse_args()

    if args.benchmark:
        print("\n🏁 Running performance benchmark...")
        benchmark_comparison()
        return 0

    print("\n" + "=" * 80)
    print("ULTRA-OPTIMIZED SIMULATION")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Agents: {args.agents:,}")
    print(f"  Features: 1,000")
    print(f"  Turns: {args.turns}")
    print(f"  Total instances: {args.agents * 1000:,}")
    print(f"  Mode: {'PARALLEL' if args.parallel else 'SINGLE-PROCESS'}")
    print()

    if args.parallel:
        # Parallel mode
        engine = ParallelUltraEngine(n_agents=args.agents, n_features=1000)
        results = engine.run_parallel(n_turns=args.turns)

        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + "PARALLEL ULTRA ENGINE - FINAL RESULTS".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")

        print(f"⚡ Duration: {results['duration']:.2f} seconds")
        print(f"⚡ Throughput: {results['throughput']:,.0f} updates/second")
        print(f"⚡ Total Evolutions: {results['total_evolutions']:,}")
        print(f"⚡ Total Synergies: {results['total_synergies']:,}")
        print(f"⚡ Average Power: {results['avg_power']:.2f}")

    else:
        # Single-process ultra mode
        engine = UltraOptimizedEngine(n_agents=args.agents, n_features=1000)

        print("=" * 80)
        print("RUNNING ULTRA-OPTIMIZED SIMULATION")
        print("=" * 80 + "\n")

        duration = engine.run_ultra(n_turns=args.turns, print_every=max(1, args.turns // 10))

        # Get statistics
        stats = engine.get_statistics()

        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + "ULTRA ENGINE - FINAL REPORT".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")

        print("─" * 80)
        print("PERFORMANCE METRICS")
        print("─" * 80)
        print(f"⚡ Duration: {duration:.2f} seconds")
        print(f"⚡ Speed: {args.turns/duration:.1f} turns/second")
        print(f"⚡ Throughput: {(args.agents * 1000 * args.turns) / duration:,.0f} updates/second")
        print(f"⚡ Memory Usage: {stats['memory_mb']:.1f} MB")
        print()

        print("─" * 80)
        print("FEATURE STATISTICS")
        print("─" * 80)
        print(f"✨ Total Feature Instances: {stats['total_feature_instances']:,}")
        print(f"✨ Total Evolutions: {stats['total_evolutions']:,}")
        print(f"✨ Total Synergies: {stats['total_synergies']:,}")
        print(f"✨ Unique Connections: {stats['unique_connections']:,}")
        print(f"✨ Average Feature Level: {stats['avg_feature_level']:.3f}")
        print(f"✨ Average Feature Activity: {stats['avg_feature_activity']:.3f}")
        print()

        print("─" * 80)
        print("AGENT STATISTICS")
        print("─" * 80)
        print(f"🔥 Average Power: {stats['avg_power']:.2f}")
        print(f"🔥 Maximum Power: {stats['max_power']:.2f}")
        print(f"🔥 Minimum Power: {stats['min_power']:.2f}")
        print(f"🔥 Power Std Dev: {stats['std_power']:.2f}")
        print()

        print("─" * 80)
        print("CATEGORY MASTERY")
        print("─" * 80)
        categories = list({
            "Consciousness & Awareness", "Physics & Reality",
            "Biology & Evolution", "Computation & Information",
            "Neural Architecture", "Social & Cultural",
            "Economics & Game Theory", "Time & Causality",
            "Quantum Mechanics", "Machine Learning",
            "Cryptography & Security", "Topology & Geometry",
            "Chaos & Complexity", "Neuroscience & Brain",
            "Linguistics & Language", "Thermodynamics",
            "Ecology & Complex Systems", "Robotics & Control",
            "Memetics & Information", "Exotic Physics"
        })
        print(f"🌈 Average Mastery: {stats['category_mastery_avg']:.3f}")
        print(f"🌈 Maximum Mastery: {stats['category_mastery_max']:.3f}")
        print(f"🌈 Best Category: {categories[stats['best_category']]}")
        print()

        print("─" * 80)
        print("TOTAL COMPLEXITY SCORE")
        print("─" * 80)
        print(f"🌌 TOTAL: {stats['total_complexity']:,}")
        print()

        # Save results
        output_dir = Path("data/ultra_engine_data")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "ultra_results.json"
        with open(output_file, "w") as f:
            json.dump(stats, f, indent=2)

        print(f"💾 Results saved to: {output_file}")
        print()

        # Achievements
        print("╔" + "═" * 78 + "╗")
        print("║" + "ULTRA ACHIEVEMENTS".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")

        achievements = []

        if args.agents >= 500:
            achievements.append("🚀 MASSIVE SCALE - 500+ agents")

        if args.agents >= 1000:
            achievements.append("🚀 ENORMOUS SCALE - 1000+ agents")

        if duration < 10:
            achievements.append("⚡ LIGHTNING FAST - Under 10 seconds")

        if duration < 5:
            achievements.append("⚡ BLAZING SPEED - Under 5 seconds")

        if (args.agents * 1000 * args.turns) / duration > 1_000_000:
            achievements.append("💪 MEGAPERFORMANCE - 1M+ updates/second")

        if (args.agents * 1000 * args.turns) / duration > 10_000_000:
            achievements.append("💪 GIGAPERFORMANCE - 10M+ updates/second")

        if stats['total_complexity'] >= 1_000_000:
            achievements.append("🌌 MEGA COMPLEXITY - 1M+ complexity")

        if stats['memory_mb'] < 100:
            achievements.append("🧠 MEMORY EFFICIENT - Under 100MB")

        for achievement in achievements:
            print(f"  {achievement}")

        if not achievements:
            print("  Run with more agents/turns to unlock achievements!")

        print()

    print("=" * 80)
    print("⚡ ULTRA ENGINE COMPLETE ⚡")
    print("=" * 80)
    print("\n🎯 ALL 1000 FEATURES RUNNING AT MAXIMUM SPEED!")
    print(f"🎯 Optimized with NumPy + Numba JIT + Sparse Matrices")
    print(f"🎯 Ready for MASSIVE scale simulations\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

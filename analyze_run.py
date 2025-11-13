#!/usr/bin/env python3
"""
Analyze and visualize the results of a recursive agent run.

This script reads the generation logs and provides insights into
how the agents evolved over time.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_run_summary(generations_dir: str = "generations"):
    """Load the run summary."""
    summary_path = Path(generations_dir) / "run_summary.json"

    if not summary_path.exists():
        print(f"Error: No run summary found at {summary_path}")
        print("Run main.py first to generate data.")
        sys.exit(1)

    with open(summary_path) as f:
        return json.load(f)


def analyze_evolution(summary: dict):
    """Analyze how agents evolved over generations."""
    print("\n" + "=" * 80)
    print("AGENT EVOLUTION ANALYSIS")
    print("=" * 80 + "\n")

    generations = summary.get("generations", [])

    # Track metrics over time
    autonomy_progression = []
    capability_growth = []

    print("Generation-by-Generation Progression:\n")

    for i, gen in enumerate(generations):
        print(f"{'─' * 80}")
        print(f"GENERATION {i}")
        print(f"{'─' * 80}")

        # Get design info (from improvement_design of previous gen or initial)
        if i == 0:
            # Initial generation
            capabilities = ["basic_planning", "self_analysis"]
            autonomy = 1
        else:
            prev_design = generations[i-1].get("improvement_design", {})
            capabilities = prev_design.get("new_capabilities", [])
            autonomy = prev_design.get("autonomy_level", 1)

        print(f"\nAutonomy Level: {autonomy}/10")
        print(f"Capabilities ({len(capabilities)}):")
        for cap in capabilities:
            print(f"  • {cap}")

        if gen.get("improvement_design"):
            print(f"\nImprovements Designed:")
            for imp in gen["improvement_design"].get("improvements", []):
                print(f"  → {imp}")

        autonomy_progression.append(autonomy)
        capability_growth.append(len(capabilities))

    # Summary statistics
    print(f"\n{'=' * 80}")
    print("SUMMARY STATISTICS")
    print(f"{'=' * 80}\n")

    print(f"Total Generations: {len(generations)}")
    print(f"\nAutonomy Progression: {autonomy_progression}")
    print(f"  Starting Autonomy: {autonomy_progression[0]}/10")
    if len(autonomy_progression) > 1:
        print(f"  Final Autonomy: {autonomy_progression[-1]}/10")
        print(f"  Total Growth: +{autonomy_progression[-1] - autonomy_progression[0]} levels")

    print(f"\nCapability Growth: {capability_growth}")
    print(f"  Starting Capabilities: {capability_growth[0]}")
    if len(capability_growth) > 1:
        print(f"  Final Capabilities: {capability_growth[-1]}")
        print(f"  Total Growth: +{capability_growth[-1] - capability_growth[0]} capabilities")


def analyze_thought_patterns(generations_dir: str = "generations"):
    """Analyze thought patterns across generations."""
    print(f"\n{'=' * 80}")
    print("THOUGHT PATTERN ANALYSIS")
    print(f"{'=' * 80}\n")

    gen_dir = Path(generations_dir)
    log_files = sorted(gen_dir.glob("generation_*_log.json"))

    thought_types_by_gen = []

    for log_file in log_files:
        with open(log_file) as f:
            data = json.load(f)

        gen = data["generation"]
        thoughts = data["thought_log"]

        # Count thought types
        thought_types = {}
        for thought in thoughts:
            t_type = thought.get("thought_type", "unknown")
            thought_types[t_type] = thought_types.get(t_type, 0) + 1

        print(f"Generation {gen}:")
        print(f"  Total Thoughts: {len(thoughts)}")
        print(f"  Thought Types:")
        for t_type, count in sorted(thought_types.items()):
            print(f"    {t_type}: {count}")
        print()

        thought_types_by_gen.append(len(thoughts))

    if thought_types_by_gen:
        print(f"Thought Volume Progression: {thought_types_by_gen}")
        avg = sum(thought_types_by_gen) / len(thought_types_by_gen)
        print(f"Average Thoughts per Generation: {avg:.1f}")


def show_key_insights(summary: dict):
    """Extract and display key insights."""
    print(f"\n{'=' * 80}")
    print("KEY INSIGHTS")
    print(f"{'=' * 80}\n")

    generations = summary.get("generations", [])

    # Find most significant improvements
    print("Most Significant Improvements:\n")

    for i, gen in enumerate(generations):
        design = gen.get("improvement_design")
        if design:
            print(f"Generation {i} → {i+1}:")
            print(f"  Rationale: {design.get('rationale', 'N/A')}")
            print()

    # Execution quality
    print("\nExecution Quality Over Time:\n")

    for i, gen in enumerate(generations):
        execution = gen.get("execution")
        if execution and "success_rate" in execution:
            success_rate = execution["success_rate"]
            bar_length = int(success_rate / 5)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"Generation {i}: {bar} {success_rate}%")


def export_markdown_report(summary: dict, output_file: str = "analysis_report.md"):
    """Export analysis as a markdown report."""
    with open(output_file, "w") as f:
        f.write("# Recursive Agent Run Analysis\n\n")
        f.write(f"**Run Date:** {summary.get('run_timestamp', 'Unknown')}\n\n")
        f.write(f"**Total Generations:** {len(summary.get('generations', []))}\n\n")

        f.write("## Evolution Timeline\n\n")

        generations = summary.get("generations", [])
        for i, gen in enumerate(generations):
            f.write(f"### Generation {i}\n\n")

            if i == 0:
                capabilities = ["basic_planning", "self_analysis"]
                autonomy = 1
            else:
                prev_design = generations[i-1].get("improvement_design", {})
                capabilities = prev_design.get("new_capabilities", [])
                autonomy = prev_design.get("autonomy_level", 1)

            f.write(f"**Autonomy:** {autonomy}/10\n\n")
            f.write(f"**Capabilities:**\n")
            for cap in capabilities:
                f.write(f"- {cap}\n")
            f.write("\n")

            if gen.get("plan"):
                f.write("**Plan:**\n\n")
                f.write(f"```\n{gen['plan']}\n```\n\n")

            if gen.get("improvement_design"):
                design = gen["improvement_design"]
                f.write(f"**Next Generation Design:**\n\n")
                f.write(f"{design.get('rationale', '')}\n\n")

    print(f"\nMarkdown report exported to: {output_file}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze recursive agent run results"
    )
    parser.add_argument(
        "--dir",
        default="generations",
        help="Generations directory (default: generations/)"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export markdown report"
    )

    args = parser.parse_args()

    # Load data
    summary = load_run_summary(args.dir)

    # Run analyses
    analyze_evolution(summary)
    analyze_thought_patterns(args.dir)
    show_key_insights(summary)

    # Export if requested
    if args.export:
        export_markdown_report(summary)

    print(f"\n{'=' * 80}\n")


if __name__ == "__main__":
    main()

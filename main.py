#!/usr/bin/env python3
"""
Recursive Self-Improving AI Agent System - Main Entry Point

This script runs a recursive self-improvement loop where each generation
of AI agent designs a better version of itself.

Usage:
    python main.py [--generations N] [--task "Your task"] [--model MODEL]

Example:
    python main.py --generations 5 --task "Analyze and optimize a codebase"
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.runner import AgentRunner


def load_environment():
    """Load environment variables from .env file."""
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found!")
        print("\nPlease set your API key in one of these ways:")
        print("1. Create a .env file with: ANTHROPIC_API_KEY=your_key_here")
        print("2. Set environment variable: export ANTHROPIC_API_KEY=your_key_here")
        print("\nGet your API key from: https://console.anthropic.com/")
        sys.exit(1)

    return api_key


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run a recursive self-improving AI agent system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run 5 generations with default task
  python main.py --generations 5

  # Run with a specific task
  python main.py --task "Build a web scraper for news articles"

  # Run with custom model
  python main.py --model claude-sonnet-4-5-20250929 --generations 3

  # Run with all options
  python main.py --generations 7 --task "Optimize database queries" --output results/
        """
    )

    parser.add_argument(
        "--generations",
        type=int,
        default=5,
        help="Number of generations to run (default: 5)"
    )

    parser.add_argument(
        "--task",
        type=str,
        default=None,
        help="Specific task for the agents to work on (optional)"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="claude-sonnet-4-5-20250929",
        help="Claude model to use (default: claude-sonnet-4-5-20250929)"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="generations",
        help="Output directory for generation data (default: generations/)"
    )

    return parser.parse_args()


def print_banner():
    """Print a welcome banner."""
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           RECURSIVE SELF-IMPROVING AI AGENT SYSTEM                         ║
║                                                                            ║
║  Each generation designs a better, more autonomous version of itself      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_final_summary(runner):
    """Print a final summary of the run."""
    print("\n\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "FINAL SUMMARY".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    print("\nEvolution of Capabilities:")
    print("-" * 80)

    for i, agent in enumerate(runner.generations):
        print(f"\n  Generation {i}:")
        print(f"    Autonomy Level: {agent.autonomy_level}/10")
        print(f"    Capabilities: {', '.join(agent.capabilities[:5])}")
        if len(agent.capabilities) > 5:
            print(f"                  {', '.join(agent.capabilities[5:])}")
        print(f"    Decisions Made: {len(agent.thought_log)}")

    print("\n" + "=" * 80)
    print("\nGeneration data saved to:", runner.output_dir)
    print("View detailed logs in: {}/run_summary.json".format(runner.output_dir))
    print("\n" + "=" * 80 + "\n")


def main():
    """Main entry point."""
    # Print banner
    print_banner()

    # Parse arguments
    args = parse_arguments()

    # Load environment
    api_key = load_environment()

    # Print configuration
    print("\nConfiguration:")
    print(f"  Generations: {args.generations}")
    print(f"  Model: {args.model}")
    print(f"  Task: {args.task or 'General self-improvement'}")
    print(f"  Output: {args.output}")
    print()

    # Confirm with user
    try:
        response = input("Press Enter to start, or Ctrl+C to cancel... ")
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)

    # Create and run the agent system
    try:
        runner = AgentRunner(
            max_generations=args.generations,
            output_dir=args.output,
            api_key=api_key,
            model=args.model
        )

        # Run the recursive improvement loop
        results = runner.run(task=args.task)

        # Print final summary
        print_final_summary(runner)

        return 0

    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        return 1

    except Exception as e:
        print(f"\n\nERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Run the Multi-Agent Evolution Ecosystem

Watch multiple AI agent lineages evolve simultaneously, competing and
learning from each other in real-time!
"""

import argparse
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent))

from src.ecosystem import Ecosystem


def main():
    """Run the ecosystem."""
    parser = argparse.ArgumentParser(
        description="Run Multi-Agent Evolution Ecosystem"
    )

    parser.add_argument(
        "--lineages",
        type=int,
        default=3,
        help="Number of agent lineages (default: 3)"
    )

    parser.add_argument(
        "--generations",
        type=int,
        default=3,
        help="Generations per lineage (default: 3)"
    )

    parser.add_argument(
        "--task",
        type=str,
        default=None,
        help="Task for agents to work on"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="ecosystem",
        help="Output directory"
    )

    args = parser.parse_args()

    # Load API key
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("❌ ERROR: ANTHROPIC_API_KEY not found!")
        print("Set it in .env file or environment variable")
        sys.exit(1)

    # Create and run ecosystem
    ecosystem = Ecosystem(
        num_lineages=args.lineages,
        generations_per_lineage=args.generations,
        output_dir=args.output,
        api_key=api_key
    )

    try:
        ecosystem.run(task=args.task)
        return 0
    except KeyboardInterrupt:
        print("\n\nEcosystem interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

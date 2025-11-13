#!/usr/bin/env python3
"""
Runner for progressive proof difficulty system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from progressive_proof_system import run_progressive_proof_challenge


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate proofs of progressive difficulty")
    parser.add_argument("--agents", type=int, default=5, help="Number of proof agents")
    parser.add_argument("--max-level", type=int, default=6,
                       help="Maximum difficulty level (1-6, 6 includes novel conjectures)")
    args = parser.parse_args()

    run_progressive_proof_challenge(n_agents=args.agents, max_level=args.max_level)

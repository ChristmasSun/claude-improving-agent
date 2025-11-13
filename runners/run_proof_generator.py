#!/usr/bin/env python3
"""
Runner for automated proof generator
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from proof_generator import run_proof_generation


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate formal proofs using logical reasoning")
    parser.add_argument("--agents", type=int, default=5, help="Number of proof agents")
    args = parser.parse_args()

    run_proof_generation(n_agents=args.agents)

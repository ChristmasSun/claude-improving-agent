#!/usr/bin/env python3
"""
Run LIVE Ecosystem with REAL AI agents!

Uses built-in API access - no API key needed!
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.live_ecosystem import LiveEcosystem


def main():
    """Run the live ecosystem with real AI!"""

    task = "Design an advanced AI-powered code optimization and refactoring system"

    ecosystem = LiveEcosystem(
        num_lineages=3,
        generations=3
    )

    try:
        ecosystem.run(task)
        print("\n✨ SUCCESS! Real AI agents evolved together!\n")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

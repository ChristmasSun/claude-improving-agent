#!/usr/bin/env python3
"""
Run the CODE-EVOLVING Multi-Agent Ecosystem!

Watch AI agents write and evolve ACTUAL CODE that gets better each generation!
This is REVOLUTIONARY - not just plans, but real executable code!
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.code_evolution import CodeEvolutionEcosystem


def main():
    """Run code evolution ecosystem."""

    print("""
🚀 CODE-EVOLVING AGENT ECOSYSTEM 🚀

This is something that doesn't exist anywhere else:
- Agents that WRITE actual code
- Code that EVOLVES and improves each generation
- Multiple lineages competing with different strategies
- Real performance testing and scoring
- Best code automatically saved

Let's watch code evolve!
""")

    input("Press Enter to begin the evolution... ")

    ecosystem = CodeEvolutionEcosystem(
        num_lineages=3,
        generations=3
    )

    try:
        ecosystem.run()
        print("\n✨ CODE EVOLUTION SUCCESSFUL! Check evolved_code/ for results!\n")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

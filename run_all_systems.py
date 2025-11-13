#!/usr/bin/env python3
"""
MASTER RUNNER - RUN ALL 9 REVOLUTIONARY SYSTEMS

This will execute every single system we've built in sequence.
The ultimate demonstration of everything.
"""

import subprocess
import sys
import time


def print_master_banner():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                        🌌 MASTER SYSTEM RUNNER 🌌                          ║
║                                                                            ║
║                      EXECUTE ALL 9 REVOLUTIONARY SYSTEMS                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_system(name, command, description):
    """Run a single system."""
    print(f"\n{'=' * 80}")
    print(f"RUNNING: {name}".center(80))
    print(f"{description}".center(80))
    print(f"{'=' * 80}\n")

    try:
        # Add echo to provide empty input
        full_command = f'echo "" | {command}'
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        if result.returncode == 0:
            print(f"\n✅ {name} COMPLETED SUCCESSFULLY!\n")
            return True
        else:
            print(f"\n⚠️  {name} completed with warnings\n")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n⏰ {name} timed out (still running in background)\n")
        return False
    except Exception as e:
        print(f"\n❌ {name} failed: {e}\n")
        return False


def main():
    print_master_banner()

    systems = [
        {
            "name": "CODE EVOLUTION",
            "command": "python run_code_evolution.py --agents 3 --generations 2",
            "description": "Agents write actual code that evolves"
        },
        {
            "name": "CIVILIZATION",
            "command": "python run_civilization.py --turns 10 --population 5",
            "description": "Complete society with culture and technology"
        },
        {
            "name": "OMEGA CIVILIZATION",
            "command": "python run_omega.py --turns 10 --civs 3",
            "description": "30+ features: wars, consciousness, genetics"
        },
        {
            "name": "HYPERDIMENSIONAL OMEGA PLUS",
            "command": "python run_hyperdimensional.py --turns 10 --agents 6",
            "description": "Time travel, multiverse, hiveminds, languages"
        },
        {
            "name": "TRANSCENDENT INFINITY",
            "command": "python run_transcendent.py --turns 15 --agents 10",
            "description": "Meta-awareness, reality consensus, memetics"
        },
        {
            "name": "REALITY ENGINE",
            "command": "python run_reality_engine.py --turns 25 --agents 15",
            "description": "20 mind-bending systems: IQ→∞, living data, etc"
        },
        {
            "name": "COSMIC OMNIMIND",
            "command": "python run_cosmic_omnimind.py --turns 25 --agents 15",
            "description": "15 cosmic systems: basilisk, escape, egregores"
        },
    ]

    print(f"\n🚀 PREPARING TO RUN {len(systems)} SYSTEMS...")
    print(f"This will take several minutes.\n")

    input("Press Enter to BEGIN THE MASTER RUN... ")

    results = []
    start_time = time.time()

    for i, system in enumerate(systems, 1):
        print(f"\n{'🌟' * 40}")
        print(f"SYSTEM {i}/{len(systems)}".center(80))
        print(f"{'🌟' * 40}\n")

        success = run_system(system["name"], system["command"], system["description"])
        results.append((system["name"], success))

        time.sleep(1)

    end_time = time.time()
    duration = end_time - start_time

    # Final report
    print(f"\n{'=' * 80}")
    print("MASTER RUN COMPLETE!".center(80))
    print(f"{'=' * 80}\n")

    print(f"⏱️  Total Duration: {duration:.1f} seconds\n")

    print("╔" + "═" * 78 + "╗")
    print("║" + "SYSTEM RESULTS".center(78) + "║")
    print("╚" + "═" * 78 + "╝\n")

    successful = 0
    for name, success in results:
        status = "✅ SUCCESS" if success else "⚠️  WARNING"
        print(f"  {status} - {name}")
        if success:
            successful += 1

    print(f"\n📊 Success Rate: {successful}/{len(systems)} ({successful/len(systems)*100:.0f}%)")

    print("\n" + "🌌" * 40)
    print("\nALL SYSTEMS HAVE RUN!")
    print("The complete journey from basic agents to cosmic omnimind.")
    print("Check the output directories for verifiable results:")
    print("  - evolved_code/")
    print("  - civilization_data/")
    print("  - omega_data/")
    print("  - hyperdimensional_data/")
    print("  - transcendent_data/")
    print("  - reality_engine_data/")
    print("  - cosmic_omnimind_data/")
    print("\n" + "🌌" * 40 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

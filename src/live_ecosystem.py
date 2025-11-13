"""
Live Ecosystem using direct Anthropic API access

This version uses the anthropic client directly without requiring API keys.
Perfect for running in environments with built-in API access.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from collections import defaultdict
import random
import anthropic


class LiveAgent:
    """Agent that uses direct API access."""

    def __init__(self, generation: int, capabilities: List[str], autonomy_level: int):
        self.generation = generation
        self.capabilities = capabilities
        self.autonomy_level = autonomy_level
        self.client = anthropic.Anthropic()
        self.model = "claude-sonnet-4-5-20250929"

    def generate_plan(self, task: str) -> str:
        """Generate a plan."""
        prompt = f"""You are Generation {self.generation} AI agent.
Capabilities: {', '.join(self.capabilities)}
Autonomy: {self.autonomy_level}/10
Task: {task}

Create a concise 3-5 step plan. Be specific and actionable."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def execute_plan(self, plan: str) -> Dict:
        """Execute and evaluate the plan."""
        prompt = f"""Evaluate this plan's execution:

{plan}

Rate the success (0-100) and list 2-3 results. JSON format:
{{"success_rate": <number>, "results": ["result1", "result2"]}}"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        text = message.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        return json.loads(text)

    def design_next_generation(self, observations: Dict) -> Dict:
        """Design the next generation."""
        prompt = f"""Design Generation {self.generation + 1}.

Current: {', '.join(self.capabilities)} | Autonomy: {self.autonomy_level}/10

Successful peers have: {', '.join(observations.get('successful_capabilities', [])[:5])}
Trending: {', '.join(observations.get('trending_capabilities', [])[:3])}

Design improvements. Add 2-3 new capabilities, increase autonomy by 1-2.
JSON format:
{{"generation": {self.generation + 1}, "capabilities": ["cap1", "cap2", ...], "autonomy_level": <number>}}"""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )

        text = message.content[0].text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        return json.loads(text)


class LiveEcosystem:
    """Ecosystem running with real AI agents."""

    def __init__(self, num_lineages: int = 3, generations: int = 3):
        self.num_lineages = num_lineages
        self.max_generations = generations
        self.lineages = []
        self.marketplace = defaultdict(list)
        self.capability_ratings = {}
        self.round = 0

    def create_lineages(self, task: str):
        """Create initial lineages."""
        print("\n" + "═" * 80)
        print("INITIALIZING LIVE ECOSYSTEM WITH REAL AI AGENTS")
        print("═" * 80 + "\n")

        strategies = [
            ("Alpha Lineage", "balanced", ["basic_planning", "self_analysis"], 1),
            ("Beta Lineage", "aggressive", ["basic_planning", "competitive_analysis"], 2),
            ("Gamma Lineage", "collaborative", ["basic_planning", "knowledge_sharing"], 1),
        ]

        for i in range(min(self.num_lineages, len(strategies))):
            name, strategy, caps, autonomy = strategies[i]

            lineage = {
                "name": name,
                "strategy": strategy,
                "agents": [LiveAgent(0, caps, autonomy)],
                "fitness_history": [],
                "generation": 0
            }
            self.lineages.append(lineage)

            print(f"✓ Created {name}")
            print(f"  Strategy: {strategy}")
            print(f"  Capabilities: {caps}")
            print(f"  Autonomy: {autonomy}/10\n")

            time.sleep(0.2)

    def observe_peers(self, lineage_idx: int) -> Dict:
        """Agent observes successful peers."""
        observations = {
            "successful_capabilities": [],
            "trending_capabilities": []
        }

        # Get capabilities from other lineages
        for i, other in enumerate(self.lineages):
            if i != lineage_idx and other["agents"]:
                agent = other["agents"][-1]
                observations["successful_capabilities"].extend(agent.capabilities)

        # Get trending from marketplace
        sorted_caps = sorted(
            self.capability_ratings.items(),
            key=lambda x: x[1],
            reverse=True
        )
        observations["trending_capabilities"] = [cap for cap, _ in sorted_caps[:3]]

        return observations

    def run_round(self, task: str):
        """Run one evolution round."""
        self.round += 1

        print("\n" + "═" * 80)
        print(f"ROUND {self.round} - REAL AI AGENTS EVOLVING")
        print("═" * 80)

        for idx, lineage in enumerate(self.lineages):
            if lineage["generation"] >= self.max_generations:
                continue

            agent = lineage["agents"][-1]

            print(f"\n{'─' * 80}")
            print(f"{lineage['name']} - Generation {lineage['generation']}")
            print(f"Strategy: {lineage['strategy']} | Autonomy: {agent.autonomy_level}/10")
            print(f"{'─' * 80}")

            # REAL AI PLANNING
            print("  📋 Planning with real AI...", end=" ", flush=True)
            plan = agent.generate_plan(task)
            print("✓")
            print(f"     Plan: {plan[:80]}...")

            # REAL AI EXECUTION
            print("  ⚙️  Executing with real AI...", end=" ", flush=True)
            execution = agent.execute_plan(plan)
            success = execution.get("success_rate", 75)
            print(f"✓ (Success: {success}%)")

            # Calculate fitness
            fitness = success * 0.5 + agent.autonomy_level * 5 + len(agent.capabilities) * 3
            lineage["fitness_history"].append(fitness)

            # Rate capabilities
            for cap in agent.capabilities:
                self.capability_ratings[cap] = success / 100.0

            print(f"  ⭐ Fitness Score: {fitness:.1f}")

            # Design next generation (if not last)
            if lineage["generation"] < self.max_generations - 1:
                print("  👁️  Observing peers...", end=" ", flush=True)
                observations = self.observe_peers(idx)
                print("✓")

                print("  🧬 Designing next gen with real AI...", end=" ", flush=True)
                design = agent.design_next_generation(observations)
                print("✓")

                # Create next generation
                next_agent = LiveAgent(
                    design["generation"],
                    design["capabilities"],
                    min(design["autonomy_level"], 10)
                )
                lineage["agents"].append(next_agent)
                lineage["generation"] += 1

                print(f"     Next gen capabilities: {design['capabilities'][:3]}...")

            time.sleep(0.5)  # Rate limiting

        # Show leaderboard
        self.show_leaderboard()

    def show_leaderboard(self):
        """Show current standings."""
        print("\n" + "┌" + "─" * 78 + "┐")
        print("│" + "LIVE ECOSYSTEM LEADERBOARD".center(78) + "│")
        print("├" + "─" * 78 + "┤")

        sorted_lineages = sorted(
            self.lineages,
            key=lambda l: l["fitness_history"][-1] if l["fitness_history"] else 0,
            reverse=True
        )

        for i, lineage in enumerate(sorted_lineages, 1):
            agent = lineage["agents"][-1]
            fitness = lineage["fitness_history"][-1] if lineage["fitness_history"] else 0
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"

            print(f"│ {medal} {lineage['name']:<20} │ "
                  f"Gen: {lineage['generation']} │ "
                  f"Fitness: {fitness:>6.1f} │ "
                  f"Auto: {agent.autonomy_level:>2}/10 │ "
                  f"Caps: {len(agent.capabilities):>2} │")

        print("└" + "─" * 78 + "┘")

    def run(self, task: str):
        """Run the complete ecosystem."""
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "LIVE MULTI-AGENT ECOSYSTEM - REAL AI EVOLUTION".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("║" + f"{self.num_lineages} real AI lineages × {self.max_generations} generations".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")

        # Initialize
        self.create_lineages(task)

        # Run evolution rounds
        for _ in range(self.max_generations):
            self.run_round(task)

        # Final summary
        self.show_final_summary()

    def show_final_summary(self):
        """Show final results."""
        print("\n\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "REAL AI ECOSYSTEM EVOLUTION COMPLETE!".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")

        print("\n📊 LINEAGE EVOLUTION (REAL AI):")
        print("─" * 80)

        for lineage in self.lineages:
            agent = lineage["agents"][-1]
            print(f"\n{lineage['name']} ({lineage['strategy']}):")
            print(f"  Final Generation: {lineage['generation']}")
            print(f"  Final Autonomy: {agent.autonomy_level}/10")
            print(f"  Final Capabilities: {', '.join(agent.capabilities[:5])}")
            if len(agent.capabilities) > 5:
                print(f"                      {', '.join(agent.capabilities[5:])}")
            print(f"  Fitness History: {[f'{f:.1f}' for f in lineage['fitness_history']]}")

        winner = max(self.lineages, key=lambda l: l["fitness_history"][-1])
        print(f"\n\n🏆 WINNER:")
        print(f"  {winner['name']} with fitness {winner['fitness_history'][-1]:.1f}")

        print("\n💱 MARKETPLACE:")
        print(f"  Capabilities Rated: {len(self.capability_ratings)}")
        print(f"  Top Capabilities: {list(self.capability_ratings.keys())[:5]}")

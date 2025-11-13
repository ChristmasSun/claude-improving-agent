"""
Multi-Agent Evolution Ecosystem

A revolutionary system where multiple AI agent lineages evolve simultaneously,
competing, cooperating, and learning from each other in a shared environment.

This creates emergent behaviors and accelerates evolution through competition
and knowledge sharing.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from collections import defaultdict
import random
from .agent import Agent


class CapabilityMarketplace:
    """
    A marketplace where agents can discover, trade, and share capabilities.
    Successful capabilities spread through the ecosystem.
    """

    def __init__(self):
        self.capabilities_offered: Dict[str, List[Dict]] = defaultdict(list)
        self.trade_history: List[Dict] = []
        self.capability_ratings: Dict[str, float] = {}

    def list_capability(self, agent_id: str, capability: str, price: int = 0):
        """List a capability in the marketplace."""
        self.capabilities_offered[capability].append({
            "agent_id": agent_id,
            "capability": capability,
            "price": price,
            "timestamp": datetime.now().isoformat()
        })

    def browse_capabilities(self, exclude_agent: str = None) -> List[str]:
        """Browse available capabilities."""
        caps = []
        for cap, listings in self.capabilities_offered.items():
            if exclude_agent:
                listings = [l for l in listings if l["agent_id"] != exclude_agent]
            if listings:
                caps.append(cap)
        return list(set(caps))

    def trade_capability(self, from_agent: str, to_agent: str, capability: str):
        """Record a capability trade."""
        trade = {
            "from": from_agent,
            "to": to_agent,
            "capability": capability,
            "timestamp": datetime.now().isoformat()
        }
        self.trade_history.append(trade)

    def rate_capability(self, capability: str, rating: float):
        """Rate a capability based on performance."""
        if capability not in self.capability_ratings:
            self.capability_ratings[capability] = rating
        else:
            # Moving average
            self.capability_ratings[capability] = (
                self.capability_ratings[capability] * 0.7 + rating * 0.3
            )

    def get_trending_capabilities(self, top_n: int = 5) -> List[str]:
        """Get the most traded/rated capabilities."""
        sorted_caps = sorted(
            self.capability_ratings.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [cap for cap, _ in sorted_caps[:top_n]]


class AgentLineage:
    """
    Represents a lineage of evolving agents.
    Each lineage has its own evolutionary path.
    """

    def __init__(self, lineage_id: str, name: str, api_key: str, model: str):
        self.lineage_id = lineage_id
        self.name = name
        self.api_key = api_key
        self.model = model
        self.agents: List[Agent] = []
        self.current_generation = 0
        self.fitness_scores: List[float] = []
        self.total_trades = 0
        self.strategy = "balanced"  # balanced, aggressive, collaborative

    def create_initial_agent(self, strategy: str = "balanced") -> Agent:
        """Create the first agent in this lineage."""
        self.strategy = strategy

        # Different strategies start with different capabilities
        if strategy == "aggressive":
            capabilities = ["basic_planning", "competitive_analysis"]
            autonomy = 2
        elif strategy == "collaborative":
            capabilities = ["basic_planning", "knowledge_sharing"]
            autonomy = 1
        else:  # balanced
            capabilities = ["basic_planning", "self_analysis"]
            autonomy = 1

        agent = Agent(
            generation=0,
            capabilities=capabilities,
            autonomy_level=autonomy,
            api_key=self.api_key,
            model=self.model
        )
        self.agents.append(agent)
        return agent

    def add_generation(self, agent: Agent):
        """Add a new generation to this lineage."""
        self.agents.append(agent)
        self.current_generation += 1

    def get_current_agent(self) -> Optional[Agent]:
        """Get the current generation agent."""
        return self.agents[-1] if self.agents else None

    def calculate_fitness(self, execution_results: Dict) -> float:
        """Calculate fitness score for current generation."""
        success_rate = execution_results.get("success_rate", 50)
        agent = self.get_current_agent()

        # Fitness based on success, autonomy, and capabilities
        fitness = (
            success_rate * 0.5 +
            agent.autonomy_level * 5 +
            len(agent.capabilities) * 3
        )

        self.fitness_scores.append(fitness)
        return fitness

    def get_summary(self) -> Dict:
        """Get lineage summary."""
        agent = self.get_current_agent()
        return {
            "lineage_id": self.lineage_id,
            "name": self.name,
            "generation": self.current_generation,
            "strategy": self.strategy,
            "fitness": self.fitness_scores[-1] if self.fitness_scores else 0,
            "autonomy": agent.autonomy_level if agent else 0,
            "capabilities": len(agent.capabilities) if agent else 0,
            "trades": self.total_trades
        }


class Ecosystem:
    """
    The main ecosystem that manages multiple agent lineages evolving together.

    Features:
    - Multiple lineages evolve simultaneously
    - Agents observe and learn from successful peers
    - Capability marketplace for knowledge sharing
    - Competition drives innovation
    - Real-time tracking and visualization
    """

    def __init__(
        self,
        num_lineages: int = 3,
        generations_per_lineage: int = 3,
        output_dir: str = "ecosystem",
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929"
    ):
        self.num_lineages = num_lineages
        self.generations_per_lineage = generations_per_lineage
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_key = api_key
        self.model = model

        # Core components
        self.lineages: List[AgentLineage] = []
        self.marketplace = CapabilityMarketplace()
        self.ecosystem_log: List[Dict] = []
        self.current_round = 0

    def log_event(self, event_type: str, data: Dict):
        """Log an ecosystem-level event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "round": self.current_round,
            "event_type": event_type,
            "data": data
        }
        self.ecosystem_log.append(entry)

    def initialize_lineages(self):
        """Create initial lineages with different strategies."""
        strategies = ["balanced", "aggressive", "collaborative"]
        names = [
            "Alpha Lineage",
            "Beta Lineage",
            "Gamma Lineage",
            "Delta Lineage",
            "Epsilon Lineage"
        ]

        print("\n" + "═" * 80)
        print("INITIALIZING ECOSYSTEM")
        print("═" * 80 + "\n")

        for i in range(self.num_lineages):
            strategy = strategies[i % len(strategies)]
            name = names[i % len(names)]

            lineage = AgentLineage(
                lineage_id=f"lineage_{i}",
                name=name,
                api_key=self.api_key,
                model=self.model
            )

            agent = lineage.create_initial_agent(strategy=strategy)

            self.lineages.append(lineage)

            print(f"✓ Created {name}")
            print(f"  Strategy: {strategy}")
            print(f"  Capabilities: {agent.capabilities}")
            print(f"  Autonomy: {agent.autonomy_level}/10\n")

            self.log_event("lineage_created", {
                "lineage_id": lineage.lineage_id,
                "name": name,
                "strategy": strategy
            })

    def observe_peers(self, lineage: AgentLineage) -> Dict[str, Any]:
        """
        Agent observes other successful lineages to learn strategies.
        """
        observations = {
            "successful_capabilities": [],
            "high_performing_strategies": [],
            "trending_capabilities": []
        }

        # Find most successful lineages
        sorted_lineages = sorted(
            self.lineages,
            key=lambda l: l.fitness_scores[-1] if l.fitness_scores else 0,
            reverse=True
        )

        # Observe top 2 lineages (excluding self)
        for other in sorted_lineages[:3]:
            if other.lineage_id != lineage.lineage_id:
                other_agent = other.get_current_agent()
                if other_agent:
                    observations["successful_capabilities"].extend(
                        other_agent.capabilities
                    )
                    observations["high_performing_strategies"].append(
                        other.strategy
                    )

        # Get trending capabilities from marketplace
        observations["trending_capabilities"] = (
            self.marketplace.get_trending_capabilities()
        )

        return observations

    def enhance_design_with_ecosystem_knowledge(
        self,
        base_design: Dict,
        observations: Dict,
        lineage: AgentLineage
    ) -> Dict:
        """
        Enhance agent's self-design with knowledge from ecosystem.
        """
        # Potentially adopt successful capabilities from peers
        successful_caps = set(observations["successful_capabilities"])
        trending_caps = set(observations["trending_capabilities"])
        current_caps = set(base_design.get("new_capabilities", []))

        # Add 1-2 capabilities from successful peers
        potential_new_caps = (successful_caps | trending_caps) - current_caps
        if potential_new_caps:
            num_to_adopt = min(2, len(potential_new_caps))
            adopted = random.sample(list(potential_new_caps), num_to_adopt)

            base_design["new_capabilities"].extend(adopted)
            base_design["ecosystem_learnings"] = {
                "adopted_from_peers": adopted,
                "observed_successful": list(successful_caps)[:5],
                "trending": list(trending_caps)
            }

            # Record trades
            for cap in adopted:
                self.marketplace.trade_capability(
                    "ecosystem",
                    lineage.lineage_id,
                    cap
                )
                lineage.total_trades += 1

        return base_design

    def run_generation_for_lineage(
        self,
        lineage: AgentLineage,
        task: Optional[str] = None
    ) -> Dict:
        """Run one generation for a specific lineage."""
        agent = lineage.get_current_agent()

        print(f"\n{'─' * 80}")
        print(f"{lineage.name} - Generation {lineage.current_generation}")
        print(f"Strategy: {lineage.strategy} | Autonomy: {agent.autonomy_level}/10")
        print(f"{'─' * 80}")

        results = {
            "lineage_id": lineage.lineage_id,
            "generation": lineage.current_generation,
            "plan": None,
            "execution": None,
            "observations": None,
            "design": None,
            "fitness": 0
        }

        try:
            # Generate plan
            print("  📋 Planning...", end=" ", flush=True)
            plan = agent.generate_plan(task)
            results["plan"] = plan
            print("✓")

            # Execute plan
            print("  ⚙️  Executing...", end=" ", flush=True)
            execution = agent.execute_plan(plan)
            results["execution"] = execution
            print(f"✓ (Success: {execution.get('success_rate', 0)}%)")

            # Calculate fitness
            fitness = lineage.calculate_fitness(execution)
            results["fitness"] = fitness

            # Rate capabilities in marketplace
            for cap in agent.capabilities:
                self.marketplace.rate_capability(
                    cap,
                    execution.get("success_rate", 50) / 100.0
                )

            # If not last generation, design improvement
            if lineage.current_generation < self.generations_per_lineage - 1:
                # Observe peers
                print("  👁️  Observing peers...", end=" ", flush=True)
                observations = self.observe_peers(lineage)
                results["observations"] = observations
                print("✓")

                # Design improvement
                print("  🧬 Designing next generation...", end=" ", flush=True)
                base_design = agent.design_improved_self()

                # Enhance with ecosystem knowledge
                enhanced_design = self.enhance_design_with_ecosystem_knowledge(
                    base_design,
                    observations,
                    lineage
                )
                results["design"] = enhanced_design
                print("✓")

                # Create next generation
                next_agent = Agent(
                    generation=enhanced_design["generation"],
                    capabilities=enhanced_design["new_capabilities"],
                    autonomy_level=min(enhanced_design["autonomy_level"], 10),
                    api_key=self.api_key,
                    model=self.model
                )
                lineage.add_generation(next_agent)

            print(f"  ⭐ Fitness Score: {fitness:.1f}")

            return results

        except Exception as e:
            print(f"  ❌ Error: {e}")
            results["error"] = str(e)
            return results

    def run_round(self, task: Optional[str] = None):
        """Run one round where all lineages evolve once."""
        self.current_round += 1

        print("\n" + "═" * 80)
        print(f"ROUND {self.current_round}")
        print("═" * 80)

        round_results = []

        # Each lineage evolves
        for lineage in self.lineages:
            if lineage.current_generation < self.generations_per_lineage:
                results = self.run_generation_for_lineage(lineage, task)
                round_results.append(results)

                # Small delay for rate limits
                time.sleep(0.5)

        # Show leaderboard
        self.show_leaderboard()

        self.log_event("round_complete", {
            "round": self.current_round,
            "results": round_results
        })

        return round_results

    def show_leaderboard(self):
        """Display current ecosystem leaderboard."""
        print("\n" + "┌" + "─" * 78 + "┐")
        print("│" + "ECOSYSTEM LEADERBOARD".center(78) + "│")
        print("├" + "─" * 78 + "┤")

        sorted_lineages = sorted(
            self.lineages,
            key=lambda l: l.fitness_scores[-1] if l.fitness_scores else 0,
            reverse=True
        )

        for i, lineage in enumerate(sorted_lineages, 1):
            agent = lineage.get_current_agent()
            fitness = lineage.fitness_scores[-1] if lineage.fitness_scores else 0

            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."

            print(f"│ {medal} {lineage.name:<20} │ "
                  f"Gen: {lineage.current_generation} │ "
                  f"Fitness: {fitness:>6.1f} │ "
                  f"Auto: {agent.autonomy_level:>2}/10 │ "
                  f"Caps: {len(agent.capabilities):>2} │")

        print("└" + "─" * 78 + "┘")

    def run(self, task: Optional[str] = None):
        """Run the complete ecosystem evolution."""
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "MULTI-AGENT EVOLUTION ECOSYSTEM".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("║" + f"{self.num_lineages} lineages evolving over {self.generations_per_lineage} generations each".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")

        self.log_event("ecosystem_start", {
            "num_lineages": self.num_lineages,
            "generations": self.generations_per_lineage,
            "task": task
        })

        # Initialize lineages
        self.initialize_lineages()

        # Run rounds until all lineages complete
        max_rounds = self.generations_per_lineage
        for round_num in range(max_rounds):
            self.run_round(task)

        # Final summary
        self.show_final_summary()

        # Save results
        self.save_ecosystem_data()

    def show_final_summary(self):
        """Show final ecosystem summary."""
        print("\n\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "ECOSYSTEM EVOLUTION COMPLETE".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")

        print("\n📊 LINEAGE EVOLUTION:")
        print("─" * 80)

        for lineage in self.lineages:
            print(f"\n{lineage.name} ({lineage.strategy}):")
            agent = lineage.get_current_agent()

            print(f"  Generations: {lineage.current_generation + 1}")
            print(f"  Final Autonomy: {agent.autonomy_level}/10")
            print(f"  Final Capabilities: {len(agent.capabilities)}")
            print(f"  Capability Trades: {lineage.total_trades}")
            print(f"  Fitness Progression: {[f'{f:.1f}' for f in lineage.fitness_scores]}")

            if lineage.fitness_scores:
                improvement = lineage.fitness_scores[-1] - lineage.fitness_scores[0]
                print(f"  Total Improvement: {improvement:+.1f}")

        print("\n\n🏆 WINNER:")
        winner = max(self.lineages,
                    key=lambda l: l.fitness_scores[-1] if l.fitness_scores else 0)
        print(f"  {winner.name} with fitness {winner.fitness_scores[-1]:.1f}")

        print("\n\n💱 MARKETPLACE STATISTICS:")
        print(f"  Total Trades: {len(self.marketplace.trade_history)}")
        print(f"  Unique Capabilities Traded: {len(self.marketplace.capability_ratings)}")
        print(f"  Top Capabilities: {self.marketplace.get_trending_capabilities(3)}")

    def save_ecosystem_data(self):
        """Save all ecosystem data."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "num_lineages": self.num_lineages,
            "generations_per_lineage": self.generations_per_lineage,
            "lineages": [l.get_summary() for l in self.lineages],
            "marketplace": {
                "total_trades": len(self.marketplace.trade_history),
                "trade_history": self.marketplace.trade_history,
                "capability_ratings": self.marketplace.capability_ratings
            },
            "ecosystem_log": self.ecosystem_log
        }

        output_file = self.output_dir / "ecosystem_results.json"
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n📁 Ecosystem data saved to: {output_file}")

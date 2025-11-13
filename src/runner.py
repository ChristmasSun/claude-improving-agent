"""
Agent Runner - Orchestrates the recursive self-improvement loop
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from .agent import Agent


class AgentRunner:
    """
    Orchestrates the recursive self-improvement process.

    Manages multiple generations of agents, each improving on the previous.
    """

    def __init__(
        self,
        max_generations: int = 5,
        output_dir: str = "generations",
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929"
    ):
        """
        Initialize the agent runner.

        Args:
            max_generations: Maximum number of generations to run
            output_dir: Directory to save generation data
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.max_generations = max_generations
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_key = api_key
        self.model = model

        self.generations: List[Agent] = []
        self.run_log: List[dict] = []

    def log_event(self, event_type: str, data: dict):
        """Log a run-level event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        self.run_log.append(entry)
        print(f"\n[{event_type.upper()}] {json.dumps(data, indent=2)}")

    def create_initial_agent(self) -> Agent:
        """Create the Generation 0 agent."""
        agent = Agent(
            generation=0,
            capabilities=["basic_planning", "self_analysis"],
            autonomy_level=1,
            api_key=self.api_key,
            model=self.model
        )
        self.log_event("agent_created", agent.get_summary())
        return agent

    def create_next_generation(self, design: dict) -> Agent:
        """
        Create the next generation agent based on the design.

        Args:
            design: Design specification from previous agent

        Returns:
            New agent instance
        """
        agent = Agent(
            generation=design["generation"],
            capabilities=design["new_capabilities"],
            autonomy_level=min(design["autonomy_level"], 10),
            api_key=self.api_key,
            model=self.model
        )
        self.log_event("agent_created", agent.get_summary())
        return agent

    def run_generation(self, agent: Agent, task: Optional[str] = None) -> dict:
        """
        Run a single generation: plan, execute, improve.

        Args:
            agent: The agent to run
            task: Optional specific task

        Returns:
            Results of this generation's run
        """
        self.log_event("generation_start", {
            "generation": agent.generation,
            "autonomy_level": agent.autonomy_level
        })

        results = {
            "generation": agent.generation,
            "start_time": datetime.now().isoformat(),
            "plan": None,
            "execution": None,
            "improvement_design": None,
            "end_time": None
        }

        try:
            # Step 1: Generate plan
            print(f"\n{'='*80}")
            print(f"GENERATION {agent.generation} - PLANNING PHASE")
            print(f"{'='*80}")
            plan = agent.generate_plan(task)
            results["plan"] = plan
            print(f"\nPlan:\n{plan}")

            # Step 2: Execute plan
            print(f"\n{'='*80}")
            print(f"GENERATION {agent.generation} - EXECUTION PHASE")
            print(f"{'='*80}")
            execution = agent.execute_plan(plan)
            results["execution"] = execution
            print(f"\nExecution Results:\n{json.dumps(execution, indent=2)}")

            # Step 3: Design improvement (if not last generation)
            if agent.generation < self.max_generations - 1:
                print(f"\n{'='*80}")
                print(f"GENERATION {agent.generation} - IMPROVEMENT DESIGN PHASE")
                print(f"{'='*80}")
                improvement = agent.design_improved_self()
                results["improvement_design"] = improvement
                print(f"\nNext Generation Design:\n{json.dumps(improvement, indent=2)}")

            # Save generation
            agent.save_generation(self.output_dir)
            results["end_time"] = datetime.now().isoformat()

            self.log_event("generation_complete", {
                "generation": agent.generation,
                "thought_count": len(agent.thought_log)
            })

            return results

        except Exception as e:
            self.log_event("generation_error", {
                "generation": agent.generation,
                "error": str(e)
            })
            raise

    def run(self, task: Optional[str] = None) -> List[dict]:
        """
        Run the complete recursive improvement loop.

        Args:
            task: Optional task for agents to work on

        Returns:
            List of results for each generation
        """
        print(f"\n{'#'*80}")
        print("RECURSIVE SELF-IMPROVING AGENT SYSTEM")
        print(f"Running {self.max_generations} generations")
        print(f"{'#'*80}")

        self.log_event("run_start", {
            "max_generations": self.max_generations,
            "task": task
        })

        all_results = []

        # Create and run Generation 0
        current_agent = self.create_initial_agent()
        self.generations.append(current_agent)

        for gen in range(self.max_generations):
            print(f"\n\n{'#'*80}")
            print(f"STARTING GENERATION {gen}")
            print(f"Capabilities: {current_agent.capabilities}")
            print(f"Autonomy Level: {current_agent.autonomy_level}/10")
            print(f"{'#'*80}")

            # Run this generation
            results = self.run_generation(current_agent, task)
            all_results.append(results)

            # Create next generation if not done
            if gen < self.max_generations - 1 and results["improvement_design"]:
                print(f"\n{'*'*80}")
                print(f"EVOLVING TO GENERATION {gen + 1}")
                print(f"{'*'*80}")

                current_agent = self.create_next_generation(
                    results["improvement_design"]
                )
                self.generations.append(current_agent)

                # Small delay to respect rate limits
                time.sleep(1)

        # Save final run log
        self.save_run_summary(all_results)

        self.log_event("run_complete", {
            "total_generations": len(all_results)
        })

        return all_results

    def save_run_summary(self, all_results: List[dict]):
        """Save a summary of the entire run."""
        summary = {
            "run_timestamp": datetime.now().isoformat(),
            "max_generations": self.max_generations,
            "model": self.model,
            "generations": all_results,
            "run_log": self.run_log
        }

        summary_file = self.output_dir / "run_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"\n{'='*80}")
        print(f"Run summary saved to: {summary_file}")
        print(f"{'='*80}")

        # Print final comparison
        print("\n\nGENERATION COMPARISON:")
        print(f"{'='*80}")
        for i, gen in enumerate(self.generations):
            print(f"\nGeneration {i}:")
            print(f"  Capabilities: {gen.capabilities}")
            print(f"  Autonomy: {gen.autonomy_level}/10")
            print(f"  Thoughts Logged: {len(gen.thought_log)}")

    def get_generation_summary(self, generation: int) -> Optional[dict]:
        """Get summary for a specific generation."""
        if generation < len(self.generations):
            return self.generations[generation].get_summary()
        return None

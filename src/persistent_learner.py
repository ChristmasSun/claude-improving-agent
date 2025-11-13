#!/usr/bin/env python3
"""
PERSISTENT LEARNING ENGINE

Agents save their progress and continue learning across runs!
- Save agent skills, strategies, and best scores to disk
- Load previous generation on startup
- Continue evolving from where they left off
- Show improvement over ALL runs, not just current session
"""

import numpy as np
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class AgentState:
    """Serializable agent state."""
    agent_id: int
    search_skill: float
    learning_rate: float
    exploration: float
    best_score: float
    total_generations: int
    lifetime_improvements: int


class PersistentAgent:
    """Agent with persistent learning across runs."""

    def __init__(self, agent_id, state: Optional[AgentState] = None):
        self.agent_id = agent_id

        if state:
            # Load from saved state
            self.search_skill = state.search_skill
            self.learning_rate = state.learning_rate
            self.exploration = state.exploration
            self.best_score = state.best_score
            self.total_generations = state.total_generations
            self.lifetime_improvements = state.lifetime_improvements
        else:
            # Initialize new agent
            self.search_skill = np.random.uniform(0.1, 0.3)
            self.learning_rate = np.random.uniform(0.01, 0.1)
            self.exploration = np.random.uniform(0.3, 0.7)
            self.best_score = 0.0
            self.total_generations = 0
            self.lifetime_improvements = 0

        # Current session tracking
        self.session_improvements = 0

    def solve_problem(self, problem, n_attempts=50):
        """Solve problem with current skills."""
        position = np.random.uniform(-10, 10, problem.dimensions)
        best_position = position.copy()
        best_score = problem.evaluate(position)
        initial_score = best_score

        for attempt in range(n_attempts):
            progress = attempt / n_attempts
            step_size = self.search_skill * (2.0 - progress)

            if np.random.random() < self.exploration * (1.0 - progress):
                direction = np.random.randn(problem.dimensions)
            else:
                direction = best_position - position + np.random.randn(problem.dimensions) * 0.1

            direction = direction / (np.linalg.norm(direction) + 1e-8)
            new_position = position + step_size * direction
            new_score = problem.evaluate(new_position)

            if new_score > best_score:
                best_score = new_score
                best_position = new_position.copy()
                position = new_position.copy()
            elif np.random.random() < 0.2:
                position = new_position

        # Learn from experience
        improved = best_score > initial_score
        if improved:
            improvement = (best_score - initial_score) / (initial_score + 1e-8)
            self.search_skill = min(1.0, self.search_skill * (1.0 + self.learning_rate))
            self.learning_rate = min(0.2, self.learning_rate * 1.05)
            self.session_improvements += 1
            self.lifetime_improvements += 1

        if best_score > self.best_score:
            self.best_score = best_score

        self.total_generations += 1

        return best_score, improved

    def learn_from_best(self, best_agent):
        """Knowledge transfer from successful agent."""
        if best_agent.agent_id != self.agent_id:
            self.search_skill = 0.7 * self.search_skill + 0.3 * best_agent.search_skill
            self.exploration = 0.8 * self.exploration + 0.2 * best_agent.exploration

    def get_state(self) -> AgentState:
        """Get serializable state."""
        return AgentState(
            agent_id=self.agent_id,
            search_skill=self.search_skill,
            learning_rate=self.learning_rate,
            exploration=self.exploration,
            best_score=self.best_score,
            total_generations=self.total_generations,
            lifetime_improvements=self.lifetime_improvements
        )


class SimpleProblem:
    """20D optimization problem."""

    def __init__(self, dimensions=20):
        self.dimensions = dimensions
        self.optimum = np.random.uniform(-5, 5, dimensions)
        self.target_value = 1000.0

    def evaluate(self, position):
        distance = np.linalg.norm(position - self.optimum)
        return self.target_value / (1.0 + distance)


class PersistentLearningEngine:
    """Engine with persistent learning across runs."""

    def __init__(self, n_agents=50, save_dir="data/persistent_learning"):
        self.n_agents = n_agents
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = self.save_dir / "agent_states.json"
        self.history_file = self.save_dir / "training_history.json"

        self.problem = SimpleProblem(dimensions=20)
        self.agents = []
        self.global_generation = 0
        self.training_history = []

        # Load or create agents
        self.load_agents()

        print(f"🎯 Problem: {self.problem.dimensions}D optimization")
        print(f"🎯 Target: {self.problem.target_value:.0f}")
        print(f"🤖 Agents: {n_agents}")
        print()

    def load_agents(self):
        """Load agents from disk or create new ones."""
        if self.save_file.exists():
            print("📂 Loading previous generation from disk...")
            with open(self.save_file, 'r') as f:
                data = json.load(f)

            self.global_generation = data.get('global_generation', 0)

            # Recreate agents from saved states
            for state_dict in data['agents']:
                state = AgentState(**state_dict)
                agent = PersistentAgent(state.agent_id, state=state)
                self.agents.append(agent)

            # Load training history
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    self.training_history = json.load(f)

            print(f"✅ Loaded generation {self.global_generation}")
            print(f"✅ Best historical score: {max(a.best_score for a in self.agents):.2f}")
            print(f"✅ Avg skill level: {np.mean([a.search_skill for a in self.agents]):.3f}")
            print(f"✅ Total lifetime improvements: {sum(a.lifetime_improvements for a in self.agents):,}")
            print()
        else:
            print("🆕 Creating new generation (no saved state found)")
            for i in range(self.n_agents):
                self.agents.append(PersistentAgent(i))
            print()

    def save_agents(self):
        """Save agents to disk."""
        data = {
            'global_generation': self.global_generation,
            'agents': [asdict(agent.get_state()) for agent in self.agents]
        }

        with open(self.save_file, 'w') as f:
            json.dump(data, f, indent=2)

        # Save training history
        with open(self.history_file, 'w') as f:
            json.dump(self.training_history, f, indent=2)

        print(f"💾 Saved generation {self.global_generation} to disk")

    def run_generation(self):
        """Run one generation."""
        self.global_generation += 1
        scores = []
        improvements = []

        for agent in self.agents:
            score, improved = agent.solve_problem(self.problem, n_attempts=50)
            scores.append(score)
            improvements.append(improved)

        # Find best and share knowledge
        best_idx = np.argmax(scores)
        best_agent = self.agents[best_idx]

        for agent in self.agents:
            if np.random.random() < 0.5:
                agent.learn_from_best(best_agent)

        # Statistics
        result = {
            'global_generation': self.global_generation,
            'best_score': max(scores),
            'avg_score': np.mean(scores),
            'best_agent_id': best_agent.agent_id,
            'success_rate': np.mean(improvements),
            'gap_to_optimum': (self.problem.target_value - max(scores)) / self.problem.target_value * 100,
            'avg_search_skill': np.mean([a.search_skill for a in self.agents]),
            'total_lifetime_improvements': sum(a.lifetime_improvements for a in self.agents),
            'session_improvements': sum(a.session_improvements for a in self.agents)
        }

        self.training_history.append(result)
        return result

    def run(self, n_generations=10):
        """Run multiple generations and save progress."""
        print(f"🚀 STARTING SESSION: {n_generations} generations")
        print(f"📍 Continuing from global generation {self.global_generation}")
        print("=" * 80 + "\n")

        start_time = time.time()
        session_start_gen = self.global_generation

        for _ in range(n_generations):
            result = self.run_generation()

            print(f"Generation {result['global_generation']} (Lifetime):")
            print(f"  🏆 Best Score: {result['best_score']:.2f} / {self.problem.target_value:.0f} "
                  f"(gap: {result['gap_to_optimum']:.1f}%)")
            print(f"  📊 Avg Score: {result['avg_score']:.2f}")
            print(f"  ✅ Success Rate: {result['success_rate']:.1%}")
            print(f"  🧠 Avg Skill: {result['avg_search_skill']:.3f}")
            print(f"  📈 Lifetime Improvements: {result['total_lifetime_improvements']:,}")
            print()

        duration = time.time() - start_time

        # Save progress
        self.save_agents()

        # Show session summary
        print("=" * 80)
        print("📊 SESSION SUMMARY")
        print("=" * 80)
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📍 Generations this session: {n_generations}")
        print(f"📍 Total lifetime generations: {self.global_generation}")
        print()

        if len(self.training_history) > 1:
            session_history = self.training_history[-n_generations:]
            first = session_history[0]
            last = session_history[-1]

            print("📈 THIS SESSION:")
            print(f"  Best Score: {first['best_score']:.2f} → {last['best_score']:.2f} "
                  f"({((last['best_score']-first['best_score'])/first['best_score']*100):.1f}% improvement)")
            print(f"  Avg Skill: {first['avg_search_skill']:.3f} → {last['avg_search_skill']:.3f} "
                  f"({((last['avg_search_skill']-first['avg_search_skill'])/first['avg_search_skill']*100):.1f}% growth)")
            print()

        if session_start_gen > 0:
            print("🌟 LIFETIME PROGRESS:")
            all_time_first = self.training_history[0]
            all_time_last = self.training_history[-1]
            print(f"  Started at: {all_time_first['best_score']:.2f} (gen 1)")
            print(f"  Now at: {all_time_last['best_score']:.2f} (gen {self.global_generation})")
            print(f"  Total improvement: {((all_time_last['best_score']-all_time_first['best_score'])/all_time_first['best_score']*100):.1f}%")
            print(f"  Lifetime improvements: {all_time_last['total_lifetime_improvements']:,}")
            print()

        print("💡 TIP: Run again to continue training from this checkpoint!")
        print()


def main():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                  💾 PERSISTENT LEARNING ENGINE 💾                          ║
║                                                                            ║
║           Agents Save Progress and Continue Learning Forever!              ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  FEATURES:                                                                ║
║    💾 Save agent skills to disk after each session                        ║
║    🔄 Load previous generation on startup                                 ║
║    📈 Continue improving across multiple runs                             ║
║    🌟 Track lifetime progress, not just current session                   ║
║    🧠 Knowledge persists between runs                                     ║
║                                                                            ║
║  Run this multiple times to see agents get better and better!            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

    engine = PersistentLearningEngine(n_agents=50)
    engine.run(n_generations=10)


if __name__ == "__main__":
    main()

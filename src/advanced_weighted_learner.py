#!/usr/bin/env python3
"""
ADVANCED WEIGHTED AGENTIC LEARNING SYSTEM

Next-generation learning with sophisticated weight management:
- Multi-dimensional adaptive weight matrices
- Meta-learning (learning how to learn)
- Parallel agent execution
- Weight evolution and crossover
- Performance-based weight optimization
- Ensemble weighting strategies
- Continuous improvement across generations
"""

import numpy as np
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp


@dataclass
class WeightedAgentState:
    """Advanced agent state with sophisticated weighting."""
    agent_id: int

    # Multi-dimensional weight matrices
    exploration_weights: List[float]
    exploitation_weights: List[float]
    adaptation_weights: List[float]
    cooperation_weights: List[float]

    # Meta-weights (weights that control learning)
    meta_learning_rate: float
    meta_exploration: float
    meta_adaptation_speed: float

    # Performance metrics
    best_score: float
    avg_score: float
    consistency: float
    improvement_rate: float

    # Learning statistics
    total_generations: int
    lifetime_improvements: int
    weight_updates: int
    successful_strategies: List[str]

    # Ensemble weights (how much to trust different strategies)
    strategy_weights: Dict[str, float]


class WeightedAgent:
    """Agent with advanced multi-dimensional weighting system."""

    def __init__(self, agent_id: int, state: Optional[WeightedAgentState] = None):
        self.agent_id = agent_id
        self.weight_dim = 20  # Dimensionality of weight vectors

        if state:
            # Load from saved state
            self.exploration_weights = np.array(state.exploration_weights)
            self.exploitation_weights = np.array(state.exploitation_weights)
            self.adaptation_weights = np.array(state.adaptation_weights)
            self.cooperation_weights = np.array(state.cooperation_weights)

            self.meta_learning_rate = state.meta_learning_rate
            self.meta_exploration = state.meta_exploration
            self.meta_adaptation_speed = state.meta_adaptation_speed

            self.best_score = state.best_score
            self.avg_score = state.avg_score
            self.consistency = state.consistency
            self.improvement_rate = state.improvement_rate

            self.total_generations = state.total_generations
            self.lifetime_improvements = state.lifetime_improvements
            self.weight_updates = state.weight_updates
            self.successful_strategies = state.successful_strategies.copy()
            self.strategy_weights = state.strategy_weights.copy()
        else:
            # Initialize with random weights
            self.exploration_weights = np.random.randn(self.weight_dim) * 0.5
            self.exploitation_weights = np.random.randn(self.weight_dim) * 0.5
            self.adaptation_weights = np.random.randn(self.weight_dim) * 0.5
            self.cooperation_weights = np.random.randn(self.weight_dim) * 0.5

            # Meta-weights
            self.meta_learning_rate = np.random.uniform(0.01, 0.1)
            self.meta_exploration = np.random.uniform(0.3, 0.7)
            self.meta_adaptation_speed = np.random.uniform(0.1, 0.5)

            # Performance
            self.best_score = 0.0
            self.avg_score = 0.0
            self.consistency = 0.5
            self.improvement_rate = 0.0

            # Statistics
            self.total_generations = 0
            self.lifetime_improvements = 0
            self.weight_updates = 0
            self.successful_strategies = []
            self.strategy_weights = {
                'exploration': 0.25,
                'exploitation': 0.25,
                'adaptation': 0.25,
                'cooperation': 0.25
            }

        # Current session tracking
        self.session_scores = []
        self.session_improvements = 0

    def compute_weighted_action(self, problem_state: np.ndarray, strategy: str = 'auto') -> np.ndarray:
        """Compute action using weighted combination of strategies."""

        if strategy == 'auto':
            # Use ensemble of all strategies weighted by past success
            exploration_action = np.dot(problem_state, self.exploration_weights)
            exploitation_action = np.dot(problem_state, self.exploitation_weights)
            adaptation_action = np.dot(problem_state, self.adaptation_weights)
            cooperation_action = np.dot(problem_state, self.cooperation_weights)

            # Weighted ensemble
            action = (
                self.strategy_weights['exploration'] * exploration_action +
                self.strategy_weights['exploitation'] * exploitation_action +
                self.strategy_weights['adaptation'] * adaptation_action +
                self.strategy_weights['cooperation'] * cooperation_action
            )
        elif strategy == 'exploration':
            action = np.dot(problem_state, self.exploration_weights)
        elif strategy == 'exploitation':
            action = np.dot(problem_state, self.exploitation_weights)
        elif strategy == 'adaptation':
            action = np.dot(problem_state, self.adaptation_weights)
        else:  # cooperation
            action = np.dot(problem_state, self.cooperation_weights)

        return action

    def solve_weighted_problem(self, problem, n_attempts: int = 100) -> Tuple[float, str]:
        """Solve problem using weighted strategies."""
        # Initialize position
        position = np.random.uniform(-10, 10, problem.dimensions)
        best_position = position.copy()
        best_score = problem.evaluate(position)
        initial_score = best_score

        # Track which strategy works best
        strategy_performance = {
            'exploration': [],
            'exploitation': [],
            'adaptation': [],
            'cooperation': []
        }

        for attempt in range(n_attempts):
            progress = attempt / n_attempts

            # Create problem state representation
            problem_state = np.random.randn(self.weight_dim)
            problem_state[:problem.dimensions] = (position[:self.weight_dim]
                                                  if problem.dimensions >= self.weight_dim
                                                  else np.pad(position, (0, self.weight_dim - problem.dimensions)))
            problem_state = problem_state / (np.linalg.norm(problem_state) + 1e-8)

            # Try different strategies with adaptive weighting
            if np.random.random() < self.meta_exploration * (1.0 - progress):
                # Exploration phase - try different strategies
                strategies = ['exploration', 'exploitation', 'adaptation', 'cooperation']
                strategy = np.random.choice(strategies, p=list(self.strategy_weights.values()))
            else:
                # Exploitation phase - use best ensemble
                strategy = 'auto'

            # Compute weighted action
            action_weight = self.compute_weighted_action(problem_state, strategy)

            # Convert to direction and step
            step_size = abs(action_weight) * self.meta_adaptation_speed * (2.0 - progress)
            direction = np.random.randn(problem.dimensions)
            direction = direction / (np.linalg.norm(direction) + 1e-8)

            # Apply weighted direction
            direction = direction * (1.0 + action_weight * 0.5)

            new_position = position + step_size * direction
            new_score = problem.evaluate(new_position)

            # Track strategy performance
            improvement = new_score - best_score
            if strategy != 'auto':
                strategy_performance[strategy].append(improvement)

            if new_score > best_score:
                best_score = new_score
                best_position = new_position.copy()
                position = new_position.copy()
                self.session_improvements += 1
                self.lifetime_improvements += 1

                # Update weights based on success
                self.update_weights(problem_state, strategy, improvement)
            elif np.random.random() < 0.2:  # Simulated annealing
                position = new_position

        # Update strategy weights based on performance
        self.update_strategy_weights(strategy_performance)

        # Update meta-weights based on overall performance
        if best_score > initial_score:
            improvement = (best_score - initial_score) / (initial_score + 1e-8)
            self.meta_learning_rate = min(0.2, self.meta_learning_rate * (1.0 + improvement * 0.1))
            self.improvement_rate = 0.9 * self.improvement_rate + 0.1 * improvement
            best_strategy = max(strategy_performance, key=lambda k: np.mean(strategy_performance[k]) if strategy_performance[k] else -np.inf)
            self.successful_strategies.append(best_strategy)

        # Track performance
        self.session_scores.append(best_score)
        self.best_score = max(self.best_score, best_score)
        self.avg_score = 0.9 * self.avg_score + 0.1 * best_score

        # Update consistency metric
        if len(self.session_scores) > 1:
            score_variance = np.var(self.session_scores[-10:])
            self.consistency = 1.0 / (1.0 + score_variance)

        self.total_generations += 1

        return best_score, max(strategy_performance, key=lambda k: len(strategy_performance[k]))

    def update_weights(self, problem_state: np.ndarray, strategy: str, improvement: float):
        """Update weight matrices based on performance."""
        learning_rate = self.meta_learning_rate * min(1.0, abs(improvement))

        # Gradient-like update: strengthen weights that led to improvement
        gradient = problem_state * improvement

        if strategy == 'exploration' or strategy == 'auto':
            self.exploration_weights += learning_rate * gradient
        if strategy == 'exploitation' or strategy == 'auto':
            self.exploitation_weights += learning_rate * gradient
        if strategy == 'adaptation' or strategy == 'auto':
            self.adaptation_weights += learning_rate * gradient
        if strategy == 'cooperation' or strategy == 'auto':
            self.cooperation_weights += learning_rate * gradient

        # Normalize weights to prevent explosion
        self.exploration_weights = np.clip(self.exploration_weights, -5, 5)
        self.exploitation_weights = np.clip(self.exploitation_weights, -5, 5)
        self.adaptation_weights = np.clip(self.adaptation_weights, -5, 5)
        self.cooperation_weights = np.clip(self.cooperation_weights, -5, 5)

        self.weight_updates += 1

    def update_strategy_weights(self, strategy_performance: Dict[str, List[float]]):
        """Update ensemble strategy weights based on performance."""
        # Calculate average improvement per strategy
        strategy_scores = {}
        for strategy, improvements in strategy_performance.items():
            if improvements:
                strategy_scores[strategy] = np.mean([imp for imp in improvements if imp > 0] or [0])
            else:
                strategy_scores[strategy] = 0

        # Softmax to get new weights
        total_score = sum(np.exp(score) for score in strategy_scores.values()) + 1e-8
        for strategy in self.strategy_weights:
            old_weight = self.strategy_weights[strategy]
            new_weight = np.exp(strategy_scores[strategy]) / total_score
            # Smooth update
            self.strategy_weights[strategy] = 0.9 * old_weight + 0.1 * new_weight

    def crossover_weights(self, other_agent: 'WeightedAgent', crossover_rate: float = 0.3):
        """Crossover weights with another successful agent."""
        mask = np.random.random(self.weight_dim) < crossover_rate

        self.exploration_weights = np.where(mask, other_agent.exploration_weights, self.exploration_weights)
        self.exploitation_weights = np.where(mask, other_agent.exploitation_weights, self.exploitation_weights)
        self.adaptation_weights = np.where(mask, other_agent.adaptation_weights, self.adaptation_weights)
        self.cooperation_weights = np.where(mask, other_agent.cooperation_weights, self.cooperation_weights)

        # Also blend meta-weights
        self.meta_learning_rate = 0.7 * self.meta_learning_rate + 0.3 * other_agent.meta_learning_rate
        self.meta_exploration = 0.7 * self.meta_exploration + 0.3 * other_agent.meta_exploration
        self.meta_adaptation_speed = 0.7 * self.meta_adaptation_speed + 0.3 * other_agent.meta_adaptation_speed

    def get_state(self) -> WeightedAgentState:
        """Get serializable state."""
        return WeightedAgentState(
            agent_id=self.agent_id,
            exploration_weights=self.exploration_weights.tolist(),
            exploitation_weights=self.exploitation_weights.tolist(),
            adaptation_weights=self.adaptation_weights.tolist(),
            cooperation_weights=self.cooperation_weights.tolist(),
            meta_learning_rate=float(self.meta_learning_rate),
            meta_exploration=float(self.meta_exploration),
            meta_adaptation_speed=float(self.meta_adaptation_speed),
            best_score=float(self.best_score),
            avg_score=float(self.avg_score),
            consistency=float(self.consistency),
            improvement_rate=float(self.improvement_rate),
            total_generations=self.total_generations,
            lifetime_improvements=self.lifetime_improvements,
            weight_updates=self.weight_updates,
            successful_strategies=self.successful_strategies[-100:],  # Keep last 100
            strategy_weights=self.strategy_weights.copy()
        )


class OptimizationProblem:
    """Advanced optimization problem."""

    def __init__(self, dimensions: int = 30):
        self.dimensions = dimensions
        self.optimum = np.random.uniform(-5, 5, dimensions)
        self.target_value = 1000.0

        # Add multiple local optima
        self.n_peaks = 10
        self.peak_locations = np.random.uniform(-8, 8, (self.n_peaks, dimensions))
        self.peak_heights = np.random.uniform(200, 800, self.n_peaks)

    def evaluate(self, position: np.ndarray) -> float:
        """Evaluate with multiple peaks."""
        # Main optimum
        main_distance = np.linalg.norm(position - self.optimum)
        main_score = self.target_value / (1.0 + main_distance)

        # Local optima
        local_scores = []
        for i in range(self.n_peaks):
            dist = np.linalg.norm(position - self.peak_locations[i])
            local_scores.append(self.peak_heights[i] / (1.0 + dist))

        # Return max (creates challenging landscape)
        return max(main_score, max(local_scores))


def solve_problem_parallel(agent_state_dict: dict, problem_dict: dict, n_attempts: int) -> dict:
    """Helper function for parallel processing."""
    # Reconstruct agent from state
    state = WeightedAgentState(**agent_state_dict)
    agent = WeightedAgent(state.agent_id, state=state)

    # Reconstruct problem
    problem = OptimizationProblem(dimensions=problem_dict['dimensions'])
    problem.optimum = np.array(problem_dict['optimum'])
    problem.target_value = problem_dict['target_value']
    problem.peak_locations = np.array(problem_dict['peak_locations'])
    problem.peak_heights = np.array(problem_dict['peak_heights'])

    # Solve
    score, best_strategy = agent.solve_weighted_problem(problem, n_attempts)

    # Return updated state
    return {
        'state': asdict(agent.get_state()),
        'score': score,
        'strategy': best_strategy
    }


class AdvancedWeightedLearner:
    """Advanced learning system with weighted agents and parallel execution."""

    def __init__(self, n_agents: int = 50, save_dir: str = "data/weighted_learning"):
        self.n_agents = n_agents
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.save_file = self.save_dir / "weighted_agent_states.json"
        self.history_file = self.save_dir / "weighted_training_history.json"

        self.problem = OptimizationProblem(dimensions=30)
        self.agents: List[WeightedAgent] = []
        self.global_generation = 0
        self.training_history = []

        # Load or create agents
        self.load_agents()

        print(f"🎯 Problem: {self.problem.dimensions}D optimization with {self.problem.n_peaks} local optima")
        print(f"🎯 Target: {self.problem.target_value:.0f}")
        print(f"🤖 Weighted Agents: {n_agents}")
        print(f"⚖️  Weight Dimensions: {self.agents[0].weight_dim if self.agents else 20}")
        print()

    def load_agents(self):
        """Load agents from disk or create new ones."""
        if self.save_file.exists():
            print("📂 Loading previous weighted agents from disk...")
            with open(self.save_file, 'r') as f:
                data = json.load(f)

            self.global_generation = data.get('global_generation', 0)

            for state_dict in data['agents']:
                state = WeightedAgentState(**state_dict)
                agent = WeightedAgent(state.agent_id, state=state)
                self.agents.append(agent)

            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    self.training_history = json.load(f)

            print(f"✅ Loaded generation {self.global_generation}")
            print(f"✅ Best historical score: {max(a.best_score for a in self.agents):.2f}")
            print(f"✅ Avg improvement rate: {np.mean([a.improvement_rate for a in self.agents]):.1%}")
            print(f"✅ Total weight updates: {sum(a.weight_updates for a in self.agents):,}")
            print()
        else:
            print("🆕 Creating new weighted agent population")
            for i in range(self.n_agents):
                self.agents.append(WeightedAgent(i))
            print()

    def save_agents(self):
        """Save agents to disk."""
        data = {
            'global_generation': self.global_generation,
            'agents': [asdict(agent.get_state()) for agent in self.agents]
        }

        with open(self.save_file, 'w') as f:
            json.dump(data, f, indent=2)

        with open(self.history_file, 'w') as f:
            json.dump(self.training_history, f, indent=2)

        print(f"💾 Saved generation {self.global_generation} with all weights to disk")

    def run_generation_parallel(self, n_attempts: int = 100) -> dict:
        """Run one generation with parallel execution."""
        self.global_generation += 1

        # Prepare problem dict for serialization
        problem_dict = {
            'dimensions': self.problem.dimensions,
            'optimum': self.problem.optimum.tolist(),
            'target_value': self.problem.target_value,
            'peak_locations': self.problem.peak_locations.tolist(),
            'peak_heights': self.problem.peak_heights.tolist()
        }

        # Prepare agent states
        agent_state_dicts = [asdict(agent.get_state()) for agent in self.agents]

        # Run in parallel
        results = []
        n_workers = min(mp.cpu_count(), self.n_agents)

        with ProcessPoolExecutor(max_workers=n_workers) as executor:
            futures = [
                executor.submit(solve_problem_parallel, state_dict, problem_dict, n_attempts)
                for state_dict in agent_state_dicts
            ]

            for future in as_completed(futures):
                results.append(future.result())

        # Update agents from results
        scores = []
        strategies = []
        for i, result in enumerate(results):
            # Reconstruct agent from returned state
            state = WeightedAgentState(**result['state'])
            self.agents[i] = WeightedAgent(state.agent_id, state=state)
            scores.append(result['score'])
            strategies.append(result['strategy'])

        # Crossover: best agents share weights with others
        best_indices = np.argsort(scores)[-5:]  # Top 5 agents
        for _ in range(self.n_agents // 4):  # 25% of population learns from best
            learner_idx = np.random.randint(self.n_agents)
            teacher_idx = np.random.choice(best_indices)
            if learner_idx != teacher_idx:
                self.agents[learner_idx].crossover_weights(self.agents[teacher_idx])

        # Statistics
        result = {
            'global_generation': self.global_generation,
            'best_score': max(scores),
            'avg_score': np.mean(scores),
            'median_score': np.median(scores),
            'best_agent_id': int(np.argmax(scores)),
            'improvement_rate': np.mean([a.improvement_rate for a in self.agents]),
            'consistency': np.mean([a.consistency for a in self.agents]),
            'avg_weight_updates': np.mean([a.weight_updates for a in self.agents]),
            'strategy_distribution': {s: strategies.count(s) / len(strategies) for s in set(strategies)},
            'meta_learning_rate': np.mean([a.meta_learning_rate for a in self.agents]),
            'meta_exploration': np.mean([a.meta_exploration for a in self.agents])
        }

        self.training_history.append(result)
        return result

    def run(self, n_generations: int = 10, parallel: bool = True):
        """Run training with optional parallel execution."""
        print(f"🚀 STARTING WEIGHTED LEARNING SESSION: {n_generations} generations")
        print(f"📍 Continuing from global generation {self.global_generation}")
        print(f"⚡ Parallel execution: {'ENABLED' if parallel else 'DISABLED'}")
        print("=" * 80 + "\n")

        start_time = time.time()

        for _ in range(n_generations):
            if parallel:
                result = self.run_generation_parallel(n_attempts=100)
            else:
                # Sequential fallback
                result = self.run_generation_sequential(n_attempts=100)

            print(f"Generation {result['global_generation']} (Lifetime):")
            print(f"  🏆 Best Score: {result['best_score']:.2f} / {self.problem.target_value:.0f}")
            print(f"  📊 Avg Score: {result['avg_score']:.2f} | Median: {result['median_score']:.2f}")
            print(f"  📈 Improvement Rate: {result['improvement_rate']:.1%}")
            print(f"  🎯 Consistency: {result['consistency']:.3f}")
            print(f"  ⚖️  Avg Weight Updates: {result['avg_weight_updates']:.0f}")
            print(f"  🧠 Meta Learning Rate: {result['meta_learning_rate']:.4f}")
            print(f"  🔍 Meta Exploration: {result['meta_exploration']:.3f}")
            print(f"  📋 Strategy Distribution: {result['strategy_distribution']}")
            print()

        duration = time.time() - start_time

        # Save progress
        self.save_agents()

        # Show summary
        print("=" * 80)
        print("📊 WEIGHTED LEARNING SESSION SUMMARY")
        print("=" * 80)
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📍 Generations this session: {n_generations}")
        print(f"📍 Total lifetime generations: {self.global_generation}")
        print()

        if len(self.training_history) > 1:
            first = self.training_history[-n_generations]
            last = self.training_history[-1]

            print("📈 THIS SESSION:")
            print(f"  Best Score: {first['best_score']:.2f} → {last['best_score']:.2f} "
                  f"({((last['best_score']-first['best_score'])/first['best_score']*100):.1f}% improvement)")
            print(f"  Avg Score: {first['avg_score']:.2f} → {last['avg_score']:.2f}")
            print(f"  Improvement Rate: {first['improvement_rate']:.1%} → {last['improvement_rate']:.1%}")
            print(f"  Consistency: {first['consistency']:.3f} → {last['consistency']:.3f}")
            print()

        # Best agent analysis
        best_agent = max(self.agents, key=lambda a: a.best_score)
        print("🏆 BEST AGENT ANALYSIS:")
        print(f"  Agent #{best_agent.agent_id}")
        print(f"  Best Score: {best_agent.best_score:.2f}")
        print(f"  Avg Score: {best_agent.avg_score:.2f}")
        print(f"  Improvement Rate: {best_agent.improvement_rate:.1%}")
        print(f"  Consistency: {best_agent.consistency:.3f}")
        print(f"  Weight Updates: {best_agent.weight_updates:,}")
        print(f"  Meta Learning Rate: {best_agent.meta_learning_rate:.4f}")
        print(f"  Strategy Weights: {best_agent.strategy_weights}")
        print()

        print("💡 TIP: Run again to continue evolving weights from this checkpoint!")
        print()

    def run_generation_sequential(self, n_attempts: int = 100) -> dict:
        """Sequential fallback for non-parallel execution."""
        self.global_generation += 1

        scores = []
        strategies = []

        for agent in self.agents:
            score, strategy = agent.solve_weighted_problem(self.problem, n_attempts)
            scores.append(score)
            strategies.append(strategy)

        # Crossover
        best_indices = np.argsort(scores)[-5:]
        for _ in range(self.n_agents // 4):
            learner_idx = np.random.randint(self.n_agents)
            teacher_idx = np.random.choice(best_indices)
            if learner_idx != teacher_idx:
                self.agents[learner_idx].crossover_weights(self.agents[teacher_idx])

        result = {
            'global_generation': self.global_generation,
            'best_score': max(scores),
            'avg_score': np.mean(scores),
            'median_score': np.median(scores),
            'best_agent_id': int(np.argmax(scores)),
            'improvement_rate': np.mean([a.improvement_rate for a in self.agents]),
            'consistency': np.mean([a.consistency for a in self.agents]),
            'avg_weight_updates': np.mean([a.weight_updates for a in self.agents]),
            'strategy_distribution': {s: strategies.count(s) / len(strategies) for s in set(strategies)},
            'meta_learning_rate': np.mean([a.meta_learning_rate for a in self.agents]),
            'meta_exploration': np.mean([a.meta_exploration for a in self.agents])
        }

        self.training_history.append(result)
        return result


def main():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              ⚖️  ADVANCED WEIGHTED AGENTIC LEARNER ⚖️                      ║
║                                                                            ║
║           Next-Generation Learning with Adaptive Weights!                  ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  FEATURES:                                                                ║
║    ⚖️  Multi-dimensional adaptive weight matrices                         ║
║    🧠 Meta-learning (learning how to learn)                               ║
║    ⚡ Parallel agent execution                                            ║
║    🧬 Weight evolution and crossover                                      ║
║    📊 Performance-based weight optimization                               ║
║    🎯 Ensemble weighting strategies                                       ║
║    💾 Continuous improvement with persistence                             ║
║    🔄 Weight sharing between successful agents                            ║
║                                                                            ║
║  Each agent has 4 weight matrices (20D each):                            ║
║    • Exploration weights                                                  ║
║    • Exploitation weights                                                 ║
║    • Adaptation weights                                                   ║
║    • Cooperation weights                                                  ║
║                                                                            ║
║  Plus meta-weights that control learning itself!                         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

    learner = AdvancedWeightedLearner(n_agents=50)
    learner.run(n_generations=15, parallel=True)


if __name__ == "__main__":
    main()

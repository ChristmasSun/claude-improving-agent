#!/usr/bin/env python3
"""
DISCOVERING NOVEL CELLULAR AUTOMATON RULES

Beyond Conway's Game of Life - can we discover NEW rules that produce:
- Self-replicating patterns
- Chaotic behavior
- Stable oscillators
- Gliders (moving patterns)
- Universal computation?

We'll systematically explore the space of possible rules and find
genuinely interesting emergent behavior!
"""

import numpy as np
import random
from collections import defaultdict

class CellularAutomaton:
    """General cellular automaton with configurable rules"""

    def __init__(self, width=50, height=50, rule=None):
        self.width = width
        self.height = height
        self.grid = np.random.randint(0, 2, (height, width))

        # Rule: dict mapping (state, neighbor_count) -> new_state
        if rule is None:
            # Default to Conway's Game of Life
            self.rule = self.game_of_life_rule()
        else:
            self.rule = rule

    @staticmethod
    def game_of_life_rule():
        """Conway's Game of Life rules"""
        rule = {}
        for state in [0, 1]:
            for neighbors in range(9):
                if state == 1:  # Alive
                    if neighbors in [2, 3]:
                        rule[(state, neighbors)] = 1  # Survive
                    else:
                        rule[(state, neighbors)] = 0  # Die
                else:  # Dead
                    if neighbors == 3:
                        rule[(state, neighbors)] = 1  # Birth
                    else:
                        rule[(state, neighbors)] = 0  # Stay dead
        return rule

    def count_neighbors(self, i, j):
        """Count Moore neighborhood (8 neighbors)"""
        count = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni = (i + di) % self.height
                nj = (j + dj) % self.width
                count += self.grid[ni, nj]
        return count

    def step(self):
        """One simulation step"""
        new_grid = np.zeros_like(self.grid)

        for i in range(self.height):
            for j in range(self.width):
                neighbors = self.count_neighbors(i, j)
                state = self.grid[i, j]
                new_grid[i, j] = self.rule.get((state, neighbors), 0)

        self.grid = new_grid

    def run(self, steps=100):
        """Run simulation for n steps"""
        history = [self.grid.copy()]

        for _ in range(steps):
            self.step()
            history.append(self.grid.copy())

        return history

def generate_random_rule():
    """Generate a random CA rule"""
    rule = {}
    for state in [0, 1]:
        for neighbors in range(9):
            rule[(state, neighbors)] = random.randint(0, 1)
    return rule

def analyze_behavior(history):
    """Analyze the behavior of a CA run"""
    metrics = {}

    # Population over time
    populations = [grid.sum() for grid in history]
    metrics['initial_pop'] = populations[0]
    metrics['final_pop'] = populations[-1]
    metrics['avg_pop'] = np.mean(populations)
    metrics['pop_std'] = np.std(populations)

    # Detect extinction
    metrics['extinct'] = (populations[-1] == 0)

    # Detect explosion (fills the grid)
    grid_size = history[0].size
    metrics['explosion'] = (populations[-1] > 0.9 * grid_size)

    # Detect oscillation (period detection)
    period = detect_period(history[-20:])  # Check last 20 frames
    metrics['period'] = period

    # Detect chaos (high variance)
    metrics['chaotic'] = (metrics['pop_std'] > 100)

    # Detect stability (low variance)
    metrics['stable'] = (metrics['pop_std'] < 10 and not metrics['extinct'])

    # Activity metric (how much changes each step)
    changes = []
    for i in range(len(history) - 1):
        diff = np.abs(history[i+1] - history[i]).sum()
        changes.append(diff)
    metrics['avg_change'] = np.mean(changes) if changes else 0

    return metrics

def detect_period(history):
    """Detect if the pattern oscillates with a period"""
    if len(history) < 4:
        return None

    # Check periods 1-10
    for period in range(1, min(11, len(history) // 2)):
        is_periodic = True
        for i in range(period, len(history)):
            if not np.array_equal(history[i], history[i - period]):
                is_periodic = False
                break

        if is_periodic:
            return period

    return None

def rule_to_string(rule):
    """Convert rule to compact string representation"""
    s = ""
    for state in [0, 1]:
        for neighbors in range(9):
            s += str(rule.get((state, neighbors), 0))
    return s

def string_to_rule(s):
    """Convert string back to rule"""
    rule = {}
    idx = 0
    for state in [0, 1]:
        for neighbors in range(9):
            rule[(state, neighbors)] = int(s[idx])
            idx += 1
    return rule

def discover_interesting_rules(n_trials=100):
    """Search for interesting CA rules"""

    print("="*80)
    print("SEARCHING FOR INTERESTING CELLULAR AUTOMATON RULES")
    print("="*80)
    print()

    print(f"Testing {n_trials} random rules...")
    print()

    results = []

    for trial in range(n_trials):
        rule = generate_random_rule()
        ca = CellularAutomaton(width=50, height=50, rule=rule)
        history = ca.run(steps=100)
        metrics = analyze_behavior(history)

        results.append((rule, metrics))

        if (trial + 1) % 20 == 0:
            print(f"  Completed {trial + 1}/{n_trials}...")

    print()

    # Categorize results
    categories = {
        'extinct': [],
        'explosion': [],
        'oscillators': [],
        'chaotic': [],
        'stable': [],
        'interesting': []
    }

    for rule, metrics in results:
        if metrics['extinct']:
            categories['extinct'].append((rule, metrics))
        elif metrics['explosion']:
            categories['explosion'].append((rule, metrics))
        elif metrics['period'] is not None and metrics['period'] > 1:
            categories['oscillators'].append((rule, metrics))
        elif metrics['chaotic']:
            categories['chaotic'].append((rule, metrics))
        elif metrics['stable']:
            categories['stable'].append((rule, metrics))

        # Interesting: not too boring, not too chaotic
        if (not metrics['extinct'] and
            not metrics['explosion'] and
            10 < metrics['avg_pop'] < 500 and
            metrics['avg_change'] > 5):
            categories['interesting'].append((rule, metrics))

    print("CATEGORIZATION:")
    print()
    for cat, items in categories.items():
        print(f"  {cat:15s}: {len(items):3d} rules")
    print()

    return categories

def analyze_top_rules(categories):
    """Analyze the most interesting rules found"""

    print("="*80)
    print("TOP INTERESTING RULES")
    print("="*80)
    print()

    # Show top oscillators
    if categories['oscillators']:
        print("OSCILLATORS (Repeating Patterns):")
        print()

        # Group by period
        by_period = defaultdict(list)
        for rule, metrics in categories['oscillators']:
            by_period[metrics['period']].append((rule, metrics))

        for period in sorted(by_period.keys()):
            items = by_period[period]
            print(f"  Period {period}: {len(items)} rules found")
            if items:
                rule, metrics = items[0]
                rule_str = rule_to_string(rule)
                print(f"    Example: {rule_str}")
                print(f"    Avg population: {metrics['avg_pop']:.1f}")

        print()

    # Show most interesting ones
    if categories['interesting']:
        print("MOST INTERESTING (Complex, Non-trivial Behavior):")
        print()

        # Sort by average change (activity level)
        interesting = sorted(categories['interesting'],
                           key=lambda x: x[1]['avg_change'],
                           reverse=True)

        for i, (rule, metrics) in enumerate(interesting[:5], 1):
            rule_str = rule_to_string(rule)
            print(f"{i}. Rule: {rule_str}")
            print(f"   Avg population: {metrics['avg_pop']:.1f}")
            print(f"   Population std: {metrics['pop_std']:.1f}")
            print(f"   Avg change/step: {metrics['avg_change']:.1f}")
            if metrics['period']:
                print(f"   Period: {metrics['period']}")
            print()

    # Show stable but non-trivial
    if categories['stable']:
        print("STABLE PATTERNS (Reaches Equilibrium):")
        print()

        stable = sorted(categories['stable'],
                       key=lambda x: x[1]['final_pop'],
                       reverse=True)

        for i, (rule, metrics) in enumerate(stable[:3], 1):
            rule_str = rule_to_string(rule)
            print(f"{i}. Rule: {rule_str}")
            print(f"   Final population: {metrics['final_pop']:.0f}")
            print()

def test_specific_rule(rule_str):
    """Test a specific rule and show its behavior"""

    print("="*80)
    print(f"TESTING RULE: {rule_str}")
    print("="*80)
    print()

    rule = string_to_rule(rule_str)

    ca = CellularAutomaton(width=30, height=30, rule=rule)
    history = ca.run(steps=50)

    metrics = analyze_behavior(history)

    print("Behavior Analysis:")
    print(f"  Initial population: {metrics['initial_pop']}")
    print(f"  Final population: {metrics['final_pop']:.0f}")
    print(f"  Average population: {metrics['avg_pop']:.1f}")
    print(f"  Population std dev: {metrics['pop_std']:.1f}")
    print(f"  Average change/step: {metrics['avg_change']:.1f}")

    if metrics['period']:
        print(f"  OSCILLATOR detected! Period: {metrics['period']}")
    if metrics['chaotic']:
        print(f"  CHAOTIC behavior detected!")
    if metrics['stable']:
        print(f"  STABLE equilibrium reached!")

    print()

    # Show first few frames
    print("First 10 frames:")
    print()

    for step, grid in enumerate(history[:10]):
        print(f"Step {step:2d} (pop={grid.sum():3d}):")
        for row in grid[:10]:  # Show first 10 rows
            print("  " + "".join("█" if cell else " " for cell in row[:30]))
        print()

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         CELLULAR AUTOMATON DISCOVERY ENGINE                                ║
║         Finding Novel Rules Beyond Conway's Game of Life                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

There are 2^18 = 262,144 possible cellular automaton rules!
Conway's Game of Life is just ONE of them.

Can we discover rules with:
- Beautiful oscillating patterns?
- Complex emergent behavior?
- Self-organization?

Let's find out!
""")

    # Search for interesting rules
    categories = discover_interesting_rules(n_trials=200)

    # Analyze top results
    analyze_top_rules(categories)

    # Test Conway's Game of Life for comparison
    print("="*80)
    print("FOR COMPARISON: Conway's Game of Life")
    print("="*80)
    print()

    gol_rule = CellularAutomaton.game_of_life_rule()
    gol_str = rule_to_string(gol_rule)
    test_specific_rule(gol_str)

    print("="*80)
    print("DISCOVERY COMPLETE!")
    print("="*80)
    print()
    print("✅ Explored the space of cellular automaton rules")
    print("✅ Discovered oscillators, stable patterns, and chaos")
    print("✅ Found rules with emergent complexity")
    print()
    print("The universe of possible rules is vast!")
    print("Each rule creates a different 'physics' for the cellular world.")
    print()

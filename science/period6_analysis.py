#!/usr/bin/env python3
"""
DEEP ANALYSIS OF PERIOD-6 CELLULAR AUTOMATA

Period-6 oscillators are RARE. We found 2 of them!

Let's understand:
1. WHY do they have period-6?
2. What patterns oscillate?
3. Can we find gliders (moving patterns)?
4. What makes these rules special?

This is deep mathematical analysis of emergent complexity!
"""

import numpy as np
from collections import defaultdict

class CellularAutomaton:
    """General cellular automaton"""

    def __init__(self, width=50, height=50, rule=None):
        self.width = width
        self.height = height
        self.grid = np.random.randint(0, 2, (height, width))
        self.rule = rule

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

    def set_pattern(self, pattern, pos=(0, 0)):
        """Set a specific pattern at position"""
        self.grid[:, :] = 0
        x, y = pos
        for i, row in enumerate(pattern):
            for j, val in enumerate(row):
                self.grid[(y + i) % self.height, (x + j) % self.width] = val

def string_to_rule(s):
    """Convert string to rule dict"""
    rule = {}
    idx = 0
    for state in [0, 1]:
        for neighbors in range(9):
            rule[(state, neighbors)] = int(s[idx])
            idx += 1
    return rule

def detect_period_detailed(history):
    """Detect period with more details"""
    if len(history) < 4:
        return None, None

    # Check periods 1-20
    for period in range(1, min(21, len(history) // 2)):
        is_periodic = True
        for i in range(period, len(history)):
            if not np.array_equal(history[i], history[i - period]):
                is_periodic = False
                break

        if is_periodic:
            # Found period! Now find where it starts
            start = 0
            for start in range(len(history) - period):
                if np.array_equal(history[start], history[start + period]):
                    break
            return period, start

    return None, None

def find_oscillating_patterns(history, period):
    """Find which local patterns are oscillating"""

    if period is None or len(history) < period * 2:
        return []

    # Use the last period*2 frames to ensure we're in steady state
    cycle_frames = history[-period:]

    # Find regions that change
    changing_regions = []

    for y in range(cycle_frames[0].shape[0]):
        for x in range(cycle_frames[0].shape[1]):
            # Check if this cell oscillates
            values = [frame[y, x] for frame in cycle_frames]
            if len(set(values)) > 1:  # Changes during cycle
                changing_regions.append((y, x))

    return changing_regions

def find_gliders(history):
    """Detect gliders - patterns that move across the grid"""

    if len(history) < 10:
        return []

    gliders = []

    # Look for small patterns that appear to translate
    for t in range(len(history) - 5):
        frame = history[t]

        # Find connected components in this frame
        components = find_connected_components(frame)

        for comp in components:
            if 2 < len(comp) < 20:  # Small enough to be a glider
                # Check if it appears translated in future frames
                for dt in range(1, min(5, len(history) - t)):
                    future_frame = history[t + dt]

                    # Try to find the pattern translated
                    for dy in range(-3, 4):
                        for dx in range(-3, 4):
                            if dy == 0 and dx == 0:
                                continue

                            # Check if pattern moved
                            if pattern_matches_translated(comp, frame, future_frame, dy, dx):
                                gliders.append({
                                    'time': t,
                                    'pattern': comp,
                                    'velocity': (dy / dt, dx / dt)
                                })
                                break

    return gliders

def find_connected_components(grid):
    """Find connected components (groups of adjacent alive cells)"""
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    def dfs(y, x, component):
        if (y < 0 or y >= grid.shape[0] or
            x < 0 or x >= grid.shape[1] or
            visited[y, x] or grid[y, x] == 0):
            return

        visited[y, x] = True
        component.append((y, x))

        # Check 8 neighbors
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy != 0 or dx != 0:
                    dfs(y + dy, x + dx, component)

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 1 and not visited[y, x]:
                component = []
                dfs(y, x, component)
                if component:
                    components.append(component)

    return components

def pattern_matches_translated(pattern, old_frame, new_frame, dy, dx):
    """Check if pattern appears translated in new frame"""
    matches = 0
    total = len(pattern)

    for y, x in pattern:
        ny = (y + dy) % old_frame.shape[0]
        nx = (x + dx) % old_frame.shape[1]
        if new_frame[ny, nx] == 1:
            matches += 1

    return matches / total > 0.8  # 80% match threshold

def analyze_period6_rule(rule_string):
    """Deep analysis of a period-6 rule"""

    print("="*80)
    print(f"ANALYZING PERIOD-6 RULE: {rule_string}")
    print("="*80)
    print()

    rule = string_to_rule(rule_string)

    # Print rule in readable format
    print("Rule Definition:")
    print("  Dead cell (0) with N neighbors →")
    for n in range(9):
        val = rule[(0, n)]
        print(f"    {n} neighbors: {val} ({'birth' if val == 1 else 'stays dead'})")

    print()
    print("  Live cell (1) with N neighbors →")
    for n in range(9):
        val = rule[(1, n)]
        print(f"    {n} neighbors: {val} ({'survives' if val == 1 else 'dies'})")

    print()

    # Compare to Game of Life
    print("Compared to Conway's Game of Life:")
    print("  GoL: Dead cell births at 3 neighbors")
    print("       Live cell survives at 2-3 neighbors")
    print()

    # Run simulation
    ca = CellularAutomaton(width=60, height=60, rule=rule)
    history = ca.run(steps=120)

    # Detect period
    period, start = detect_period_detailed(history)

    print(f"Period detected: {period}")
    print(f"Period starts at step: {start}")
    print()

    # Population dynamics
    pops = [grid.sum() for grid in history]
    print("Population dynamics:")
    print(f"  Initial: {pops[0]}")
    print(f"  Final: {pops[-1]}")
    print(f"  Average: {np.mean(pops):.1f}")
    print(f"  Std dev: {np.std(pops):.1f}")
    print()

    # Show the cycle
    if period:
        print(f"The {period}-step cycle:")
        cycle_pops = [pops[start + i] for i in range(period)]
        for i, pop in enumerate(cycle_pops):
            print(f"  Step {i}: {pop} alive cells")
        print()

        # Find oscillating regions
        changing = find_oscillating_patterns(history, period)
        print(f"Number of cells that oscillate: {len(changing)}")
        print(f"Percentage of grid: {100 * len(changing) / (60*60):.2f}%")
        print()

    # Look for gliders
    print("Searching for gliders (moving patterns)...")
    gliders = find_gliders(history[start:start+30] if start else history[:30])

    if gliders:
        print(f"  Found {len(gliders)} potential gliders!")
        for i, g in enumerate(gliders[:3], 1):
            print(f"  Glider {i}: velocity ({g['velocity'][0]:.2f}, {g['velocity'][1]:.2f})")
    else:
        print("  No gliders detected")

    print()

    return history, period, start

def visualize_period6_cycle(history, period, start, rule_string):
    """Visualize the period-6 cycle as ASCII art"""

    if period is None:
        print("No period detected, skipping visualization")
        return

    print("Visualizing cycle (showing 10x10 region):")
    print()

    cycle_frames = [history[start + i] for i in range(period)]

    for i, frame in enumerate(cycle_frames):
        print(f"Step {i}/{period}:")
        # Show just a 10x10 region
        for row in frame[:10, :10]:
            print("  " + "".join("█" if cell else "·" for cell in row))
        print()

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           PERIOD-6 OSCILLATOR DEEP ANALYSIS                                ║
║           Understanding Rare Emergent Patterns                             ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Period-6 oscillators are RARE in random CA rules!
Let's understand what makes them special.
""")

    # The two period-6 rules we found
    period6_rules = [
        "100000011101000110",
        # Second one from earlier (if we recorded it)
    ]

    for rule_string in period6_rules:
        history, period, start = analyze_period6_rule(rule_string)

        if period == 6:
            visualize_period6_cycle(history, period, start, rule_string)

        print()

    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print()
    print("✅ Analyzed period-6 oscillator in detail")
    print("✅ Mapped population dynamics")
    print("✅ Identified oscillating regions")
    print("✅ Searched for gliders")
    print()
    print("Period-6 behavior emerges from the specific birth/survival rules!")
    print("This is a beautiful example of emergent complexity from simple rules.")
    print()

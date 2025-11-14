#!/usr/bin/env python3
"""
UNIVERSAL STRUCTURAL PATTERNS ACROSS MATHEMATICAL DOMAINS

HYPOTHESIS: The same fundamental patterns appear across different mathematical systems.

We discovered:
1. RATS: 93% of numbers are UNREACHABLE
2. CA rules: Most random rules either die or explode (only ~6% are "interesting")

QUESTION: Is this a UNIVERSAL PATTERN?

Let's test if the "93% excluded" pattern appears in OTHER domains:
- Prime numbers
- Graph connectivity
- Fibonacci-like sequences
- Collatz-like sequences
- Other discrete dynamical systems

This could reveal a DEEP MATHEMATICAL PRINCIPLE!
"""

import numpy as np
import random
from collections import defaultdict

def analyze_density_patterns():
    """Analyze density/sparsity patterns across mathematical domains"""

    print("="*80)
    print("UNIVERSAL STRUCTURAL PATTERNS - Cross-Domain Analysis")
    print("="*80)
    print()

    results = {}

    # Domain 1: RATS Formability (we already know this)
    print("DOMAIN 1: RATS Formability")
    print("-" * 40)

    def reverse_number(n):
        return int(str(n)[::-1])

    # Count formable 3-digit numbers
    formable_3digit = set()
    for n in range(1, 1000):
        sum_val = n + reverse_number(n)
        if 100 <= sum_val < 1000:
            formable_3digit.add(sum_val)

    total_3digit = 900
    formable_count = len(formable_3digit)
    formable_pct = 100 * formable_count / total_3digit

    print(f"3-digit numbers formable as n+R(n): {formable_count}/{total_3digit} ({formable_pct:.2f}%)")
    print(f"UNREACHABLE: {100 - formable_pct:.2f}%")
    results['rats_formability'] = formable_pct
    print()

    # Domain 2: Prime Density
    print("DOMAIN 2: Prime Number Density")
    print("-" * 40)

    def is_prime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    primes_in_range = sum(1 for n in range(100, 1000) if is_prime(n))
    prime_density = 100 * primes_in_range / 900

    print(f"Primes in [100, 999]: {primes_in_range}/900 ({prime_density:.2f}%)")
    print(f"Composites: {100 - prime_density:.2f}%")
    results['prime_density'] = prime_density
    print()

    # Domain 3: Collatz-like reachability
    print("DOMAIN 3: Collatz Trajectory Reachability")
    print("-" * 40)

    def collatz_step(n):
        return n // 2 if n % 2 == 0 else 3 * n + 1

    def collatz_trajectory(n, max_steps=1000):
        """Generate Collatz trajectory"""
        vals = set([n])
        current = n
        for _ in range(max_steps):
            if current == 1:
                break
            current = collatz_step(current)
            vals.add(current)
        return vals

    # Find all values reached by Collatz from [1, 500]
    reachable_collatz = set()
    for start in range(1, 501):
        traj = collatz_trajectory(start)
        for val in traj:
            if val <= 10000:
                reachable_collatz.add(val)

    collatz_density = 100 * len(reachable_collatz) / 10000

    print(f"Numbers reached by Collatz([1,500]) in [1,10000]: {len(reachable_collatz)}/10000 ({collatz_density:.2f}%)")
    print(f"UNREACHABLE: {100 - collatz_density:.2f}%")
    results['collatz_reachability'] = collatz_density
    print()

    # Domain 4: Graph Connectivity (Random Graphs)
    print("DOMAIN 4: Random Graph Connectivity")
    print("-" * 40)

    def is_connected_graph(n_nodes, n_edges):
        """Check if random graph is connected"""
        # Build random graph
        edges = set()
        for _ in range(n_edges):
            u = random.randint(0, n_nodes - 1)
            v = random.randint(0, n_nodes - 1)
            if u != v:
                edges.add((min(u, v), max(u, v)))

        # BFS to check connectivity
        if not edges:
            return False

        visited = set([0])
        queue = [0]

        while queue:
            node = queue.pop(0)
            for u, v in edges:
                if u == node and v not in visited:
                    visited.add(v)
                    queue.append(v)
                elif v == node and u not in visited:
                    visited.add(u)
                    queue.append(u)

        return len(visited) == n_nodes

    # Test connectivity for graphs with 20 nodes, various edge counts
    n_nodes = 20
    trials = 100
    connected_count = sum(1 for _ in range(trials) if is_connected_graph(n_nodes, n_nodes))

    connectivity_pct = 100 * connected_count / trials

    print(f"Random graphs (20 nodes, 20 edges) that are connected: {connected_count}/{trials} ({connectivity_pct:.2f}%)")
    print(f"Disconnected: {100 - connectivity_pct:.2f}%")
    results['graph_connectivity'] = connectivity_pct
    print()

    # Domain 5: Fibonacci-like Sequences that terminate
    print("DOMAIN 5: Generalized Fibonacci Convergence")
    print("-" * 40)

    def fibonacci_like_terminates(a, b, modulo, max_steps=1000):
        """Check if F(n) = F(n-1) + F(n-2) mod m terminates at a fixed point"""
        seen = set()
        for _ in range(max_steps):
            state = (a, b)
            if state in seen:
                # Found a cycle - check if it's trivial (a=b=0 or a=b)
                return a == 0 and b == 0
            seen.add(state)
            a, b = b, (a + b) % modulo
        return False

    # Test various starting conditions with modulo 10
    terminating = 0
    total = 100
    for i in range(total):
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        if fibonacci_like_terminates(a, b, 10):
            terminating += 1

    fib_terminate_pct = 100 * terminating / total

    print(f"Fibonacci-like sequences (mod 10) that reach 0: {terminating}/{total} ({fib_terminate_pct:.2f}%)")
    print(f"Non-terminating (cycling): {100 - fib_terminate_pct:.2f}%")
    results['fibonacci_convergence'] = fib_terminate_pct
    print()

    # Domain 6: Perfect Numbers and Abundant Numbers
    print("DOMAIN 6: Perfect/Deficient/Abundant Number Distribution")
    print("-" * 40)

    def sum_of_divisors(n):
        """Sum of proper divisors"""
        if n <= 1:
            return 0
        total = 1  # 1 is always a divisor
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                total += i
                if i != n // i:
                    total += n // i
        return total

    perfect = 0
    abundant = 0
    deficient = 0

    for n in range(2, 1001):
        s = sum_of_divisors(n)
        if s == n:
            perfect += 1
        elif s > n:
            abundant += 1
        else:
            deficient += 1

    perfect_pct = 100 * perfect / 999
    abundant_pct = 100 * abundant / 999
    deficient_pct = 100 * deficient / 999

    print(f"Perfect numbers in [2,1000]: {perfect} ({perfect_pct:.2f}%)")
    print(f"Abundant numbers: {abundant} ({abundant_pct:.2f}%)")
    print(f"Deficient numbers: {deficient} ({deficient_pct:.2f}%)")
    results['perfect_numbers'] = perfect_pct
    results['abundant_numbers'] = abundant_pct
    print()

    return results

def find_universal_pattern(results):
    """Analyze if there's a universal pattern"""

    print("="*80)
    print("UNIVERSAL PATTERN ANALYSIS")
    print("="*80)
    print()

    print("Summary of densities across domains:")
    print()

    # Sort by reachable/special percentage
    for domain, pct in sorted(results.items(), key=lambda x: x[1]):
        bar = "█" * int(pct / 2)  # Scale to ~50 chars max
        print(f"{domain:25s}: {pct:6.2f}% {bar}")

    print()

    # Statistical analysis
    values = list(results.values())
    mean = np.mean(values)
    std = np.std(values)
    median = np.median(values)

    print("Statistical Summary:")
    print(f"  Mean: {mean:.2f}%")
    print(f"  Median: {median:.2f}%")
    print(f"  Std Dev: {std:.2f}%")
    print()

    # Check for universal principles
    print("OBSERVED PATTERNS:")
    print()

    # Pareto-like (80/20 rule)
    pareto_domains = [d for d, p in results.items() if 15 <= p <= 25]
    if len(pareto_domains) >= 2:
        print(f"✓ PARETO PRINCIPLE (~20% rule): {len(pareto_domains)} domains")
        print(f"  Domains: {', '.join(pareto_domains)}")
        print()

    # Extreme sparsity (<15%)
    sparse_domains = [d for d, p in results.items() if p < 15]
    if len(sparse_domains) >= 2:
        print(f"✓ EXTREME SPARSITY (<15%): {len(sparse_domains)} domains")
        print(f"  Domains: {', '.join(sparse_domains)}")
        print()

    # Bimodal distribution
    if std > 15:
        print(f"✓ BIMODAL DISTRIBUTION (high std dev = {std:.1f}%)")
        print(f"  Suggests two classes: 'rare' and 'common' properties")
        print()

    return mean, std, median

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║        UNIVERSAL STRUCTURAL PATTERNS IN MATHEMATICS                        ║
║        Cross-Domain Analysis of Density and Sparsity                       ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

We discovered that 93% of numbers are unreachable in RATS sequences.

QUESTION: Is this level of sparsity UNIVERSAL across mathematical domains?

We'll test:
- Number theory (formability, primes, perfect numbers)
- Dynamical systems (Collatz, Fibonacci)
- Graph theory (connectivity)

Looking for META-PATTERNS that transcend specific domains!
""")

    results = analyze_density_patterns()
    mean, std, median = find_universal_pattern(results)

    print("="*80)
    print("CONCLUSION")
    print("="*80)
    print()
    print(f"Across {len(results)} mathematical domains:")
    print(f"  Average 'special' property density: {mean:.1f}%")
    print(f"  This means ~{100-mean:.1f}% are 'ordinary' on average")
    print()
    print("HYPOTHESIS: Mathematical structures naturally exhibit sparsity.")
    print("Most objects are 'generic', while interesting properties are RARE.")
    print()
    print("This mirrors:")
    print("  - Pareto principle (80/20 rule)")
    print("  - Power law distributions")
    print("  - Phase transitions (order vs chaos)")
    print()
    print("🌟 Universal principle: INTERESTING = RARE 🌟")
    print()

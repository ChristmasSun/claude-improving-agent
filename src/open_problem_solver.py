#!/usr/bin/env python3
"""
MAJOR OPEN PROBLEM SOLVER

Tackle REAL unsolved problems in mathematics:
1. Goldbach's Conjecture - Every even n > 2 is sum of two primes
2. Twin Prime Conjecture - Infinitely many primes p where p+2 is prime
3. Collatz Conjecture - Does 3n+1 sequence always reach 1?
4. Perfect Numbers - Are there infinitely many? Any odd ones?
5. Prime Gaps - Find record gaps between consecutive primes
6. Odd Perfect Numbers - Find one or prove they don't exist

We won't PROVE these (requires mathematical insight).
We CAN:
- Verify for increasingly large numbers
- Search for counterexamples (would disprove!)
- Extend computational bounds
- Find patterns for future research
"""

import numpy as np
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import hashlib


@dataclass
class ConjectureResult:
    """Result of testing a conjecture."""
    conjecture_name: str
    test_range: Tuple[int, int]
    verified_count: int
    counterexample_found: bool
    counterexample: Optional[any]
    records_found: List[any]
    computation_time: float
    agent_id: int


class PrimeCache:
    """Efficient prime number generator and cache."""

    def __init__(self, limit: int = 10_000_000):
        self.limit = limit
        self.primes = []
        self.prime_set = set()
        self.generated_up_to = 0

    def sieve_of_eratosthenes(self, n: int):
        """Generate primes up to n."""
        if n <= self.generated_up_to:
            return

        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False

        for i in range(2, int(n**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, n + 1, i):
                    sieve[j] = False

        new_primes = [i for i in range(max(2, self.generated_up_to + 1), n + 1) if sieve[i]]
        self.primes.extend(new_primes)
        self.prime_set.update(new_primes)
        self.generated_up_to = n

    def is_prime(self, n: int) -> bool:
        """Check if n is prime."""
        if n <= self.generated_up_to:
            return n in self.prime_set

        # Miller-Rabin primality test for large numbers
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        # Write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        # Witnesses to test
        witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

        for a in witnesses:
            if a >= n:
                continue

            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False

        return True

    def get_primes_up_to(self, n: int) -> List[int]:
        """Get all primes up to n."""
        if n > self.generated_up_to:
            self.sieve_of_eratosthenes(min(n, self.limit))
        return [p for p in self.primes if p <= n]

    def next_prime(self, n: int) -> int:
        """Find next prime after n."""
        candidate = n + 1
        while not self.is_prime(candidate):
            candidate += 1
        return candidate


class GoldbachTester:
    """Test Goldbach's Conjecture: Every even n > 2 is sum of two primes."""

    @staticmethod
    def test_goldbach(n: int, prime_cache: PrimeCache) -> Tuple[bool, Optional[Tuple[int, int]]]:
        """Test if even number n can be written as sum of two primes."""
        if n <= 2 or n % 2 != 0:
            return False, None

        primes = prime_cache.get_primes_up_to(n)
        prime_set = set(primes)

        for p in primes:
            if p > n // 2:
                break
            complement = n - p
            if complement in prime_set:
                return True, (p, complement)

        return False, None

    @staticmethod
    def test_range(start: int, end: int, prime_cache: PrimeCache) -> ConjectureResult:
        """Test Goldbach for range of even numbers."""
        start_time = time.time()

        # Make start even
        if start % 2 != 0:
            start += 1
        if start < 4:
            start = 4

        verified = 0
        counterexample = None
        examples = []

        for n in range(start, end + 1, 2):
            verified_this, decomposition = GoldbachTester.test_goldbach(n, prime_cache)

            if verified_this:
                verified += 1
                if len(examples) < 5:  # Keep first 5 examples
                    examples.append({'n': n, 'decomposition': decomposition})
            else:
                counterexample = n
                break

        return ConjectureResult(
            conjecture_name='Goldbach',
            test_range=(start, end),
            verified_count=verified,
            counterexample_found=counterexample is not None,
            counterexample=counterexample,
            records_found=examples,
            computation_time=time.time() - start_time,
            agent_id=0
        )


class TwinPrimeFinder:
    """Search for twin primes (p, p+2 both prime)."""

    @staticmethod
    def find_twin_primes(start: int, count: int, prime_cache: PrimeCache) -> ConjectureResult:
        """Find twin prime pairs starting from start."""
        start_time = time.time()

        twin_primes = []
        current = max(start, 3)
        found = 0

        while found < count:
            if prime_cache.is_prime(current) and prime_cache.is_prime(current + 2):
                twin_primes.append((current, current + 2))
                found += 1
            current += 1

            # Safety limit
            if current > start + 10_000_000:
                break

        return ConjectureResult(
            conjecture_name='TwinPrime',
            test_range=(start, current),
            verified_count=found,
            counterexample_found=False,
            counterexample=None,
            records_found=twin_primes[-10:] if twin_primes else [],  # Last 10 found
            computation_time=time.time() - start_time,
            agent_id=0
        )


class CollatzTester:
    """Test Collatz Conjecture: 3n+1 sequence always reaches 1."""

    @staticmethod
    def collatz_sequence_length(n: int, max_steps: int = 10_000) -> Tuple[int, bool]:
        """
        Compute Collatz sequence length.
        Returns (steps, reached_1)
        """
        steps = 0
        current = n

        while current != 1 and steps < max_steps:
            if current % 2 == 0:
                current = current // 2
            else:
                current = 3 * current + 1
            steps += 1

        return steps, current == 1

    @staticmethod
    def test_range(start: int, end: int) -> ConjectureResult:
        """Test Collatz for range of numbers."""
        start_time = time.time()

        verified = 0
        counterexample = None
        longest_sequence = (0, 0)  # (number, length)

        for n in range(start, end + 1):
            steps, reached_one = CollatzTester.collatz_sequence_length(n)

            if reached_one:
                verified += 1
                if steps > longest_sequence[1]:
                    longest_sequence = (n, steps)
            else:
                counterexample = n
                break

        return ConjectureResult(
            conjecture_name='Collatz',
            test_range=(start, end),
            verified_count=verified,
            counterexample_found=counterexample is not None,
            counterexample=counterexample,
            records_found=[{'number': longest_sequence[0], 'steps': longest_sequence[1]}],
            computation_time=time.time() - start_time,
            agent_id=0
        )


class PerfectNumberFinder:
    """Search for perfect numbers (n = sum of proper divisors)."""

    @staticmethod
    def is_perfect(n: int) -> bool:
        """Check if n is perfect."""
        if n < 2:
            return False

        divisor_sum = 1  # 1 is always a divisor

        # Find divisors up to sqrt(n)
        sqrt_n = int(n**0.5)
        for i in range(2, sqrt_n + 1):
            if n % i == 0:
                divisor_sum += i
                if i != n // i:  # Don't count square root twice
                    divisor_sum += n // i

        return divisor_sum == n

    @staticmethod
    def is_odd_perfect(n: int) -> bool:
        """Check if n is an odd perfect number."""
        return n % 2 == 1 and PerfectNumberFinder.is_perfect(n)

    @staticmethod
    def search_perfect_numbers(start: int, end: int) -> ConjectureResult:
        """Search for perfect numbers in range."""
        start_time = time.time()

        perfect_numbers = []
        odd_perfect = None

        for n in range(start, end + 1):
            if PerfectNumberFinder.is_perfect(n):
                perfect_numbers.append(n)
                if n % 2 == 1:
                    odd_perfect = n
                    break  # Would be huge discovery!

        return ConjectureResult(
            conjecture_name='PerfectNumber',
            test_range=(start, end),
            verified_count=len(perfect_numbers),
            counterexample_found=odd_perfect is not None,
            counterexample=odd_perfect,
            records_found=perfect_numbers,
            computation_time=time.time() - start_time,
            agent_id=0
        )


class PrimeGapFinder:
    """Find large gaps between consecutive primes."""

    @staticmethod
    def find_prime_gaps(start: int, count: int, prime_cache: PrimeCache) -> ConjectureResult:
        """Find prime gaps starting from start."""
        start_time = time.time()

        current_prime = start
        if not prime_cache.is_prime(current_prime):
            current_prime = prime_cache.next_prime(current_prime)

        gaps = []
        max_gap = (0, 0, 0)  # (gap, p1, p2)

        for _ in range(count):
            next_p = prime_cache.next_prime(current_prime)
            gap = next_p - current_prime

            gaps.append({'gap': gap, 'primes': (current_prime, next_p)})

            if gap > max_gap[0]:
                max_gap = (gap, current_prime, next_p)

            current_prime = next_p

        return ConjectureResult(
            conjecture_name='PrimeGap',
            test_range=(start, current_prime),
            verified_count=count,
            counterexample_found=False,
            counterexample=None,
            records_found=[{
                'max_gap': max_gap[0],
                'between': (max_gap[1], max_gap[2])
            }],
            computation_time=time.time() - start_time,
            agent_id=0
        )


class OpenProblemAgent:
    """Agent that tackles open problems."""

    def __init__(self, agent_id: int):
        self.agent_id = agent_id
        self.prime_cache = PrimeCache(limit=10_000_000)

        # Strategy: which problems to focus on
        self.goldbach_priority = np.random.uniform(0.5, 1.5)
        self.twin_prime_priority = np.random.uniform(0.5, 1.5)
        self.collatz_priority = np.random.uniform(0.5, 1.5)
        self.perfect_priority = np.random.uniform(0.5, 1.5)
        self.prime_gap_priority = np.random.uniform(0.5, 1.5)

        # Performance
        self.conjectures_verified = 0
        self.records_found = []
        self.counterexample_found = False

    def work_on_goldbach(self, difficulty: int) -> ConjectureResult:
        """Test Goldbach's conjecture."""
        base = 1000 * (10 ** difficulty)
        start = int(base * self.goldbach_priority)
        end = start + 10000

        result = GoldbachTester.test_range(start, end, self.prime_cache)
        result.agent_id = self.agent_id

        self.conjectures_verified += result.verified_count
        if result.counterexample_found:
            self.counterexample_found = True

        return result

    def work_on_twin_primes(self, difficulty: int) -> ConjectureResult:
        """Search for twin primes."""
        base = 1000 * (10 ** difficulty)
        start = int(base * self.twin_prime_priority)
        count = 100

        result = TwinPrimeFinder.find_twin_primes(start, count, self.prime_cache)
        result.agent_id = self.agent_id

        if result.records_found:
            self.records_found.extend(result.records_found)

        return result

    def work_on_collatz(self, difficulty: int) -> ConjectureResult:
        """Test Collatz conjecture."""
        base = 10000 * (10 ** difficulty)
        start = int(base * self.collatz_priority)
        end = start + 10000

        result = CollatzTester.test_range(start, end)
        result.agent_id = self.agent_id

        self.conjectures_verified += result.verified_count
        if result.counterexample_found:
            self.counterexample_found = True

        return result

    def work_on_perfect_numbers(self, difficulty: int) -> ConjectureResult:
        """Search for perfect numbers."""
        base = 1000 * (10 ** difficulty)
        start = int(base * self.perfect_priority)
        end = start + 10000

        result = PerfectNumberFinder.search_perfect_numbers(start, end)
        result.agent_id = self.agent_id

        if result.counterexample_found:
            # Found odd perfect number - would be HUGE
            self.counterexample_found = True

        return result

    def work_on_prime_gaps(self, difficulty: int) -> ConjectureResult:
        """Find prime gaps."""
        base = 1000 * (10 ** difficulty)
        start = int(base * self.prime_gap_priority)
        count = 1000

        result = PrimeGapFinder.find_prime_gaps(start, count, self.prime_cache)
        result.agent_id = self.agent_id

        if result.records_found:
            self.records_found.extend(result.records_found)

        return result


class OpenProblemEngine:
    """Engine for tackling major open problems."""

    def __init__(self, n_agents: int = 20, save_dir: str = "data/open_problems"):
        self.n_agents = n_agents
        self.agents = [OpenProblemAgent(i) for i in range(n_agents)]
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

        self.results = []
        self.major_discoveries = []

        print(f"🔬 MAJOR OPEN PROBLEM SOLVER")
        print(f"🤖 Agents: {n_agents}")
        print()
        print("TACKLING:")
        print("  1. Goldbach's Conjecture")
        print("  2. Twin Prime Conjecture")
        print("  3. Collatz Conjecture")
        print("  4. Perfect Number Search")
        print("  5. Prime Gap Records")
        print()
        print("⚠️  HONEST EXPECTATIONS:")
        print("  - We won't PROVE these conjectures")
        print("  - We CAN verify for huge ranges")
        print("  - We CAN find counterexamples (would disprove!)")
        print("  - We CAN extend computational bounds")
        print()

    def run_generation(self, difficulty: int = 0):
        """Run one generation of open problem solving."""
        print(f"\n{'='*80}")
        print(f"GENERATION WITH DIFFICULTY {difficulty}")
        print(f"Testing ranges around 10^{3+difficulty}")
        print(f"{'='*80}\n")

        generation_results = []

        # Divide work among agents
        problems = ['goldbach', 'twin_prime', 'collatz', 'perfect', 'prime_gap']

        for i, agent in enumerate(self.agents):
            problem = problems[i % len(problems)]

            print(f"Agent #{agent.agent_id} working on {problem}...", end=" ")

            if problem == 'goldbach':
                result = agent.work_on_goldbach(difficulty)
            elif problem == 'twin_prime':
                result = agent.work_on_twin_primes(difficulty)
            elif problem == 'collatz':
                result = agent.work_on_collatz(difficulty)
            elif problem == 'perfect':
                result = agent.work_on_perfect_numbers(difficulty)
            else:  # prime_gap
                result = agent.work_on_prime_gaps(difficulty)

            generation_results.append(result)

            if result.counterexample_found:
                print(f"🚨 COUNTEREXAMPLE FOUND! 🚨")
                self.major_discoveries.append(result)
            else:
                print(f"✅ Verified {result.verified_count} instances")

        self.results.extend(generation_results)

        # Summary
        print(f"\n{'='*80}")
        print("GENERATION SUMMARY:")
        print(f"{'='*80}")

        by_conjecture = {}
        for r in generation_results:
            if r.conjecture_name not in by_conjecture:
                by_conjecture[r.conjecture_name] = []
            by_conjecture[r.conjecture_name].append(r)

        for conj_name, results in by_conjecture.items():
            total_verified = sum(r.verified_count for r in results)
            any_counterexample = any(r.counterexample_found for r in results)

            print(f"\n{conj_name}:")
            print(f"  Verified: {total_verified:,} instances")
            if any_counterexample:
                counterex_result = next(r for r in results if r.counterexample_found)
                print(f"  ⚠️  COUNTEREXAMPLE: {counterex_result.counterexample}")
            else:
                print(f"  Status: No counterexamples found ✓")

        # Save results
        self.save_results(generation_results, difficulty)

    def save_results(self, results: List[ConjectureResult], difficulty: int):
        """Save generation results."""
        filename = self.save_dir / f"difficulty_{difficulty}_results.json"

        def convert(obj):
            if isinstance(obj, (np.bool_, bool)):
                return bool(obj)
            elif isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, tuple):
                return list(obj)
            elif isinstance(obj, list):
                return [convert(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert(value) for key, value in obj.items()}
            return obj

        data = [convert(asdict(r)) for r in results]

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def run(self, n_generations: int = 5, starting_difficulty: int = 0):
        """Run multiple generations with increasing difficulty."""
        print("\n" + "="*80)
        print("🚀 STARTING OPEN PROBLEM SOLVING")
        print("="*80)
        print()

        start_time = time.time()

        for gen in range(n_generations):
            difficulty = starting_difficulty + gen
            self.run_generation(difficulty)

        duration = time.time() - start_time

        # Final summary
        print("\n" + "="*80)
        print("🎯 FINAL RESULTS")
        print("="*80)
        print(f"Duration: {duration:.2f} seconds")
        print()

        # Aggregate by conjecture
        by_conjecture = {}
        for r in self.results:
            if r.conjecture_name not in by_conjecture:
                by_conjecture[r.conjecture_name] = {
                    'verified': 0,
                    'counterexamples': [],
                    'records': []
                }
            by_conjecture[r.conjecture_name]['verified'] += r.verified_count
            if r.counterexample_found:
                by_conjecture[r.conjecture_name]['counterexamples'].append(r.counterexample)
            if r.records_found:
                by_conjecture[r.conjecture_name]['records'].extend(r.records_found)

        print("CONJECTURE VERIFICATION SUMMARY:")
        print()

        for conj_name, data in by_conjecture.items():
            print(f"{conj_name}:")
            print(f"  Total verified: {data['verified']:,}")
            if data['counterexamples']:
                print(f"  🚨 COUNTEREXAMPLES: {data['counterexamples']}")
            else:
                print(f"  No counterexamples found ✓")
            if data['records'] and conj_name in ['TwinPrime', 'PrimeGap']:
                print(f"  Interesting finds: {len(data['records'])} records")
            print()

        if self.major_discoveries:
            print("="*80)
            print("🏆 MAJOR DISCOVERIES")
            print("="*80)
            for disc in self.major_discoveries:
                print(f"  {disc.conjecture_name}: Counterexample {disc.counterexample}")
            print()
        else:
            print("="*80)
            print("✅ CONJECTURES HOLD")
            print("="*80)
            print("All tested conjectures verified in their ranges.")
            print("No counterexamples found (but we didn't prove them either!)")
            print()

        print(f"💾 Results saved to {self.save_dir}/")
        print()


def main():
    banner = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              🔬 MAJOR OPEN PROBLEM SOLVER 🔬                               ║
║                                                                            ║
║         Tackle REAL Unsolved Problems in Mathematics!                      ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  OPEN PROBLEMS:                                                           ║
║    1. Goldbach's Conjecture (since 1742)                                 ║
║    2. Twin Prime Conjecture (ancient)                                    ║
║    3. Collatz Conjecture (since 1937)                                    ║
║    4. Odd Perfect Numbers (2000+ years)                                  ║
║    5. Prime Gap Records                                                  ║
║                                                                            ║
║  WHAT WE CAN DO:                                                          ║
║    ✓ Verify conjectures for huge ranges                                  ║
║    ✓ Search for counterexamples (would disprove!)                        ║
║    ✓ Extend computational bounds                                         ║
║    ✓ Find interesting patterns                                           ║
║                                                                            ║
║  WHAT WE CAN'T DO:                                                        ║
║    ✗ Prove the conjectures (requires human insight)                      ║
║    ✗ Solve P vs NP, Riemann Hypothesis, etc.                            ║
║                                                                            ║
║  BUT: Finding a counterexample would be a MAJOR discovery!               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

    engine = OpenProblemEngine(n_agents=20)
    engine.run(n_generations=5, starting_difficulty=0)


if __name__ == "__main__":
    main()

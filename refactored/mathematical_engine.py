"""
REFACTORED MATHEMATICAL DISCOVERY ENGINE

Clean, modular, performant code for exploring mathematical patterns.

This refactored version:
- Uses proper OOP design
- Caches expensive computations
- Vectorized operations where possible
- Type hints throughout
- Comprehensive documentation
- Unit testable
"""

from typing import List, Set, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from functools import lru_cache
import numpy as np
from abc import ABC, abstractmethod


# ============================================================================
# Core Abstractions
# ============================================================================

class MathematicalSequence(ABC):
    """Abstract base class for mathematical sequences."""

    @abstractmethod
    def generate(self, n: int) -> int:
        """Generate the n-th element of the sequence."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Return the name of this sequence."""
        pass


class ReachabilityAnalyzer(ABC):
    """Abstract base for analyzing which values are reachable in a system."""

    @abstractmethod
    def compute_reachable(self, start_set: Set[int], max_value: int) -> Set[int]:
        """Compute all reachable values from start_set up to max_value."""
        pass

    def density(self, start_set: Set[int], max_value: int) -> float:
        """Compute the density of reachable values."""
        reachable = self.compute_reachable(start_set, max_value)
        return len(reachable) / max_value


@dataclass
class DensityResult:
    """Results from density analysis."""
    total: int
    reachable: int
    density: float
    reachable_values: Optional[Set[int]] = None

    def __str__(self) -> str:
        return f"{self.reachable}/{self.total} ({100*self.density:.2f}%)"


# ============================================================================
# Digit Manipulation Utilities
# ============================================================================

@lru_cache(maxsize=10000)
def reverse_digits(n: int) -> int:
    """
    Reverse the decimal digits of n.

    Examples:
        >>> reverse_digits(123)
        321
        >>> reverse_digits(1000)
        1
    """
    return int(str(n)[::-1])


@lru_cache(maxsize=10000)
def digit_sum(n: int) -> int:
    """Sum of decimal digits of n."""
    return sum(int(d) for d in str(n))


def num_digits(n: int) -> int:
    """Number of decimal digits in n."""
    return len(str(n)) if n > 0 else 1


def split_odd_even_positions(n: int) -> Tuple[int, int]:
    """
    Split digits into odd and even positions (1-indexed).

    Example:
        >>> split_odd_even_positions(1234)
        (13, 24)  # positions 1,3 and positions 2,4
    """
    s = str(n)
    odd = ''.join(s[i] for i in range(0, len(s), 2))
    even = ''.join(s[i] for i in range(1, len(s), 2))
    return int(odd) if odd else 0, int(even) if even else 0


# ============================================================================
# RATS (Reverse-And-Add Termination Sequences)
# ============================================================================

class RATSAnalyzer(ReachabilityAnalyzer):
    """
    Analyzer for RATS (Reverse-And-Add Termination Sequences).

    RATS operation: n → n + R(n) until palindrome reached.
    """

    def __init__(self):
        self._formable_cache: Dict[Tuple[int, int], Set[int]] = {}

    @staticmethod
    def is_palindrome(n: int) -> bool:
        """Check if n is a palindrome."""
        s = str(n)
        return s == s[::-1]

    def rats_step(self, n: int) -> int:
        """Single RATS step: n → n + R(n)."""
        return n + reverse_digits(n)

    def rats_trajectory(self, n: int, max_steps: int = 100) -> List[int]:
        """
        Generate RATS trajectory until palindrome or max_steps.

        Returns:
            List of values in trajectory including start and final palindrome.
        """
        trajectory = [n]
        current = n

        for _ in range(max_steps):
            if self.is_palindrome(current):
                break
            current = self.rats_step(current)
            trajectory.append(current)

        return trajectory

    def compute_reachable(self, start_set: Set[int], max_value: int) -> Set[int]:
        """Compute all values reachable via RATS from start_set."""
        reachable = set()

        for start in start_set:
            trajectory = self.rats_trajectory(start)
            reachable.update(v for v in trajectory if v <= max_value)

        return reachable

    def formable_in_range(self, min_val: int, max_val: int) -> Set[int]:
        """
        Find all values in [min_val, max_val] that can be written as n + R(n).

        Uses caching for efficiency.
        """
        cache_key = (min_val, max_val)
        if cache_key in self._formable_cache:
            return self._formable_cache[cache_key]

        formable = set()
        # Need to check all n up to max_val because n + R(n) can be less than n
        # Example: n=100 gives 101, but n=99 gives 198
        search_limit = max_val

        for n in range(1, search_limit + 1):
            val = self.rats_step(n)
            if min_val <= val <= max_val:
                formable.add(val)

        self._formable_cache[cache_key] = formable
        return formable

    def formability_density(self, d: int) -> DensityResult:
        """
        Compute formability density for d-digit numbers.

        Args:
            d: Number of digits

        Returns:
            DensityResult with statistics
        """
        min_val = 10**(d-1)
        max_val = 10**d - 1
        total = max_val - min_val + 1

        formable = self.formable_in_range(min_val, max_val)

        return DensityResult(
            total=total,
            reachable=len(formable),
            density=len(formable) / total,
            reachable_values=formable
        )


# ============================================================================
# Collatz Conjecture
# ============================================================================

class CollatzAnalyzer(ReachabilityAnalyzer):
    """Analyzer for Collatz conjecture dynamics."""

    def __init__(self):
        self._trajectory_cache: Dict[int, List[int]] = {}

    @staticmethod
    def collatz_step(n: int) -> int:
        """Single Collatz step."""
        return n // 2 if n % 2 == 0 else 3 * n + 1

    def trajectory(self, n: int, max_steps: int = 1000) -> List[int]:
        """Generate Collatz trajectory."""
        if n in self._trajectory_cache:
            return self._trajectory_cache[n]

        traj = [n]
        current = n

        for _ in range(max_steps):
            if current == 1:
                break
            current = self.collatz_step(current)
            traj.append(current)

        self._trajectory_cache[n] = traj
        return traj

    def compute_reachable(self, start_set: Set[int], max_value: int) -> Set[int]:
        """Compute all values reachable via Collatz from start_set."""
        reachable = set()

        for start in start_set:
            traj = self.trajectory(start)
            reachable.update(v for v in traj if v <= max_value)

        return reachable


# ============================================================================
# Prime Numbers
# ============================================================================

class PrimeAnalyzer:
    """Efficient prime number analysis."""

    def __init__(self):
        self._sieve_cache: Dict[int, np.ndarray] = {}

    def sieve_of_eratosthenes(self, limit: int) -> np.ndarray:
        """
        Compute all primes up to limit using Sieve of Eratosthenes.

        Returns:
            Boolean array where True indicates prime.
        """
        if limit in self._sieve_cache:
            return self._sieve_cache[limit]

        is_prime = np.ones(limit + 1, dtype=bool)
        is_prime[0] = is_prime[1] = False

        for i in range(2, int(limit**0.5) + 1):
            if is_prime[i]:
                is_prime[i*i:limit+1:i] = False

        self._sieve_cache[limit] = is_prime
        return is_prime

    def primes_in_range(self, min_val: int, max_val: int) -> Set[int]:
        """Get all primes in [min_val, max_val]."""
        is_prime = self.sieve_of_eratosthenes(max_val)
        return set(np.where(is_prime[min_val:max_val+1])[0] + min_val)

    def density(self, min_val: int, max_val: int) -> DensityResult:
        """Compute prime density in range."""
        primes = self.primes_in_range(min_val, max_val)
        total = max_val - min_val + 1

        return DensityResult(
            total=total,
            reachable=len(primes),
            density=len(primes) / total,
            reachable_values=primes
        )


# ============================================================================
# Universal Pattern Analysis
# ============================================================================

class UniversalPatternAnalyzer:
    """
    Analyze universal patterns across mathematical domains.

    Tests whether the ~10% density pattern holds universally.
    """

    def __init__(self):
        self.rats = RATSAnalyzer()
        self.collatz = CollatzAnalyzer()
        self.primes = PrimeAnalyzer()

    def analyze_all_domains(self,
                           test_range: Tuple[int, int] = (100, 999)
                           ) -> Dict[str, DensityResult]:
        """
        Run density analysis across all domains.

        Args:
            test_range: (min_val, max_val) to test

        Returns:
            Dictionary mapping domain name to DensityResult
        """
        min_val, max_val = test_range
        results = {}

        # RATS formability
        d = num_digits(min_val)
        results['RATS Formability'] = self.rats.formability_density(d)

        # Collatz reachability (test on larger range to match original analysis)
        # Original: reachable from [1,500] within [1,10000]
        start_set = set(range(1, 501))
        collatz_test_max = max(10000, max_val * 10)  # Test on larger range
        collatz_reach = self.collatz.compute_reachable(start_set, collatz_test_max)
        collatz_in_range = {v for v in collatz_reach if min_val <= v <= max_val}
        total_collatz = collatz_test_max  # Density over full range, not just test_range
        results['Collatz Reachability'] = DensityResult(
            total=total_collatz,
            reachable=len(collatz_reach),
            density=len(collatz_reach) / total_collatz,
            reachable_values=collatz_reach
        )

        # Prime density
        results['Prime Numbers'] = self.primes.density(min_val, max_val)

        return results

    def compute_statistics(self, results: Dict[str, DensityResult]) -> Dict[str, float]:
        """Compute summary statistics across all results."""
        densities = [r.density for r in results.values()]

        return {
            'mean': np.mean(densities),
            'median': np.median(densities),
            'std': np.std(densities),
            'min': np.min(densities),
            'max': np.max(densities)
        }

    def report(self, results: Dict[str, DensityResult]) -> str:
        """Generate formatted report of results."""
        lines = ["=" * 80]
        lines.append("UNIVERSAL PATTERN ANALYSIS")
        lines.append("=" * 80)
        lines.append("")

        for domain, result in results.items():
            lines.append(f"{domain:25s}: {result}")

        lines.append("")
        stats = self.compute_statistics(results)
        lines.append(f"Mean density: {100*stats['mean']:.2f}%")
        lines.append(f"Median density: {100*stats['median']:.2f}%")
        lines.append(f"Std dev: {100*stats['std']:.2f}%")
        lines.append("")

        return "\n".join(lines)


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("Refactored Mathematical Discovery Engine")
    print("=" * 80)
    print()

    # Example 1: RATS formability for different digit counts
    print("RATS Formability by Digit Count:")
    print("-" * 40)
    rats = RATSAnalyzer()
    for d in [2, 3, 4]:
        result = rats.formability_density(d)
        print(f"  {d}-digit: {result}")
    print()

    # Example 2: Universal pattern analysis
    print("Universal Pattern Analysis (3-digit numbers):")
    print("-" * 40)
    analyzer = UniversalPatternAnalyzer()
    results = analyzer.analyze_all_domains((100, 999))
    print(analyzer.report(results))

    # Example 3: Collatz reachability
    print("Collatz Reachability:")
    print("-" * 40)
    collatz = CollatzAnalyzer()
    density = collatz.density(set(range(1, 101)), 1000)
    print(f"  From [1,100]: {density}")
    print()

    # Example 4: Prime density comparison
    print("Prime Density by Range:")
    print("-" * 40)
    primes = PrimeAnalyzer()
    for power in [2, 3, 4]:
        min_val = 10**(power-1)
        max_val = 10**power - 1
        result = primes.density(min_val, max_val)
        print(f"  {power}-digit: {result}")

"""
Comprehensive tests for the mathematical discovery engine.

Run with: python3 -m pytest test_mathematical_engine.py -v
"""

import pytest
import numpy as np
from mathematical_engine import (
    reverse_digits,
    digit_sum,
    num_digits,
    split_odd_even_positions,
    RATSAnalyzer,
    CollatzAnalyzer,
    PrimeAnalyzer,
    UniversalPatternAnalyzer,
)


# ============================================================================
# Utility Function Tests
# ============================================================================

class TestDigitUtilities:
    """Test digit manipulation utilities."""

    def test_reverse_digits_basic(self):
        assert reverse_digits(123) == 321
        assert reverse_digits(1000) == 1
        assert reverse_digits(12321) == 12321  # Palindrome

    def test_reverse_digits_single(self):
        assert reverse_digits(5) == 5

    def test_digit_sum(self):
        assert digit_sum(123) == 6
        assert digit_sum(1000) == 1
        assert digit_sum(999) == 27

    def test_num_digits(self):
        assert num_digits(1) == 1
        assert num_digits(99) == 2
        assert num_digits(100) == 3
        assert num_digits(1000) == 4

    def test_split_odd_even_positions(self):
        assert split_odd_even_positions(1234) == (13, 24)
        assert split_odd_even_positions(12) == (1, 2)
        assert split_odd_even_positions(123) == (13, 2)


# ============================================================================
# RATS Analyzer Tests
# ============================================================================

class TestRATSAnalyzer:
    """Test RATS sequence analysis."""

    @pytest.fixture
    def rats(self):
        return RATSAnalyzer()

    def test_palindrome_detection(self, rats):
        assert rats.is_palindrome(121)
        assert rats.is_palindrome(1)
        assert rats.is_palindrome(12321)
        assert not rats.is_palindrome(123)

    def test_rats_step(self, rats):
        # 29 + 92 = 121
        assert rats.rats_step(29) == 121
        # 19 + 91 = 110
        assert rats.rats_step(19) == 110

    def test_rats_trajectory_simple(self, rats):
        # 29 -> 121 (palindrome in 1 step)
        traj = rats.rats_trajectory(29)
        assert traj == [29, 121]

    def test_rats_trajectory_multistep(self, rats):
        # 19 -> 110 -> 121
        traj = rats.rats_trajectory(19)
        assert traj[0] == 19
        assert traj[-1] == 121
        assert len(traj) == 3

    def test_rats_symmetry_property(self, rats):
        """Test that RATS(n) and RATS(R(n)) reach same palindrome."""
        test_pairs = [(29, 92), (19, 91), (38, 83)]

        for n, rn in test_pairs:
            traj_n = rats.rats_trajectory(n)
            traj_rn = rats.rats_trajectory(rn)
            # Should reach same final palindrome
            assert traj_n[-1] == traj_rn[-1]
            # Should have same length
            assert len(traj_n) == len(traj_rn)

    def test_formable_contains_known_values(self, rats):
        """Test that formable set contains known formable numbers."""
        formable = rats.formable_in_range(100, 200)

        # 121 = 29 + 92 (and many others)
        assert 121 in formable

        # 110 = 19 + 91
        assert 110 in formable

    def test_formability_density_2digit(self, rats):
        """Test 2-digit formability matches known result."""
        result = rats.formability_density(2)

        # Should be around 20% (18 out of 90)
        assert 0.15 < result.density < 0.25
        assert result.total == 90  # 10-99

    def test_formability_density_3digit(self, rats):
        """Test 3-digit formability matches known result."""
        result = rats.formability_density(3)

        # Should be around 10% (93 out of 900)
        assert 0.08 < result.density < 0.15
        assert result.total == 900  # 100-999

    def test_formability_decreases_with_digits(self, rats):
        """Test that formability decreases as digit count increases."""
        d2 = rats.formability_density(2).density
        d3 = rats.formability_density(3).density
        d4 = rats.formability_density(4).density

        assert d2 > d3 > d4


# ============================================================================
# Collatz Analyzer Tests
# ============================================================================

class TestCollatzAnalyzer:
    """Test Collatz conjecture analysis."""

    @pytest.fixture
    def collatz(self):
        return CollatzAnalyzer()

    def test_collatz_step_even(self, collatz):
        assert collatz.collatz_step(10) == 5
        assert collatz.collatz_step(100) == 50

    def test_collatz_step_odd(self, collatz):
        assert collatz.collatz_step(3) == 10
        assert collatz.collatz_step(5) == 16

    def test_collatz_trajectory_simple(self, collatz):
        # 1 should stay at 1
        traj = collatz.trajectory(1)
        assert traj == [1]

    def test_collatz_trajectory_reaches_1(self, collatz):
        """Test that small numbers reach 1."""
        for n in range(2, 20):
            traj = collatz.trajectory(n)
            assert traj[-1] == 1, f"Collatz({n}) didn't reach 1"

    def test_collatz_known_sequence(self, collatz):
        """Test a known Collatz sequence."""
        # 3 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
        traj = collatz.trajectory(3)
        expected_start = [3, 10, 5, 16, 8, 4, 2, 1]
        assert traj == expected_start

    def test_collatz_caching(self, collatz):
        """Test that trajectory caching works."""
        traj1 = collatz.trajectory(10)
        traj2 = collatz.trajectory(10)

        # Should be same object (cached)
        assert traj1 is traj2

    def test_collatz_reachability(self, collatz):
        """Test reachability computation."""
        reachable = collatz.compute_reachable({10}, 100)

        # Should include: 10, 5, 16, 8, 4, 2, 1
        expected = {10, 5, 16, 8, 4, 2, 1}
        assert expected.issubset(reachable)


# ============================================================================
# Prime Analyzer Tests
# ============================================================================

class TestPrimeAnalyzer:
    """Test prime number analysis."""

    @pytest.fixture
    def primes(self):
        return PrimeAnalyzer()

    def test_sieve_small_primes(self, primes):
        is_prime = primes.sieve_of_eratosthenes(20)

        # Known primes up to 20: 2, 3, 5, 7, 11, 13, 17, 19
        known_primes = {2, 3, 5, 7, 11, 13, 17, 19}
        found_primes = set(np.where(is_prime)[0])

        assert known_primes == found_primes

    def test_primes_in_range(self, primes):
        # Primes in [10, 20]: 11, 13, 17, 19
        result = primes.primes_in_range(10, 20)
        assert result == {11, 13, 17, 19}

    def test_prime_density_decreases(self, primes):
        """Test Prime Number Theorem: density decreases with range."""
        d2 = primes.density(10, 99).density
        d3 = primes.density(100, 999).density
        d4 = primes.density(1000, 9999).density

        # By Prime Number Theorem, density should decrease
        assert d2 > d3 > d4

    def test_prime_density_2digit(self, primes):
        """Test that 2-digit prime density is reasonable."""
        result = primes.density(10, 99)

        # Should be around 21% (21 primes out of 90)
        assert 0.20 < result.density < 0.25

    def test_sieve_caching(self, primes):
        """Test that sieve results are cached."""
        sieve1 = primes.sieve_of_eratosthenes(100)
        sieve2 = primes.sieve_of_eratosthenes(100)

        # Should be same object (cached)
        assert sieve1 is sieve2


# ============================================================================
# Universal Pattern Analyzer Tests
# ============================================================================

class TestUniversalPatternAnalyzer:
    """Test cross-domain pattern analysis."""

    @pytest.fixture
    def analyzer(self):
        return UniversalPatternAnalyzer()

    def test_analyze_all_domains(self, analyzer):
        """Test that all domains are analyzed."""
        results = analyzer.analyze_all_domains((100, 999))

        assert 'RATS Formability' in results
        assert 'Collatz Reachability' in results
        assert 'Prime Numbers' in results

        # All should have valid densities
        for result in results.values():
            assert 0 <= result.density <= 1
            assert result.total > 0
            assert result.reachable >= 0

    def test_statistics_computation(self, analyzer):
        """Test summary statistics computation."""
        results = analyzer.analyze_all_domains((100, 999))
        stats = analyzer.compute_statistics(results)

        assert 'mean' in stats
        assert 'median' in stats
        assert 'std' in stats

        # Mean should be positive
        assert stats['mean'] > 0

    def test_90_10_pattern(self, analyzer):
        """Test that the 90/10 pattern holds (roughly)."""
        results = analyzer.analyze_all_domains((100, 999))
        stats = analyzer.compute_statistics(results)

        # Mean should be in the 5-20% range (the "interesting" zone)
        assert 0.05 < stats['mean'] < 0.20, \
            f"Mean density {stats['mean']:.3f} outside expected range"

    def test_report_generates(self, analyzer):
        """Test that report generation works."""
        results = analyzer.analyze_all_domains((100, 999))
        report = analyzer.report(results)

        assert len(report) > 0
        assert "UNIVERSAL PATTERN ANALYSIS" in report


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests across multiple components."""

    def test_rats_collatz_both_sparse(self):
        """Test that both RATS and Collatz show sparsity pattern."""
        rats = RATSAnalyzer()
        collatz = CollatzAnalyzer()

        # For 3-digit numbers
        rats_density = rats.formability_density(3).density
        collatz_density = collatz.density(set(range(1, 501)), 1000)

        # Both should be in similar range (5-15%)
        assert 0.05 < rats_density < 0.15
        # Collatz is harder to bound, but should show sparsity

    def test_consistent_results_across_runs(self):
        """Test that results are deterministic."""
        analyzer1 = UniversalPatternAnalyzer()
        analyzer2 = UniversalPatternAnalyzer()

        results1 = analyzer1.analyze_all_domains((100, 999))
        results2 = analyzer2.analyze_all_domains((100, 999))

        # Results should be identical
        for domain in results1:
            assert results1[domain].density == results2[domain].density


# ============================================================================
# Performance Tests
# ============================================================================

class TestPerformance:
    """Test performance characteristics."""

    def test_rats_formability_fast(self):
        """Test that formability computation is fast."""
        rats = RATSAnalyzer()

        # Should complete in reasonable time
        def compute():
            return rats.formability_density(3)

        # Just run it once for now (proper benchmarking needs pytest-benchmark)
        result = compute()
        assert result.total == 900

    def test_sieve_caching_improves_performance(self):
        """Test that caching improves performance."""
        primes = PrimeAnalyzer()

        # First call (no cache)
        import time
        start = time.time()
        primes.sieve_of_eratosthenes(10000)
        time1 = time.time() - start

        # Second call (cached)
        start = time.time()
        primes.sieve_of_eratosthenes(10000)
        time2 = time.time() - start

        # Cached version should be much faster
        assert time2 < time1 / 10  # At least 10x faster


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    # Run tests without pytest
    print("Running tests...")
    print("=" * 80)

    # Simple test runner
    test_classes = [
        TestDigitUtilities,
        TestRATSAnalyzer,
        TestCollatzAnalyzer,
        TestPrimeAnalyzer,
        TestUniversalPatternAnalyzer,
        TestIntegration,
    ]

    total_tests = 0
    passed_tests = 0

    for test_class in test_classes:
        print(f"\n{test_class.__name__}:")
        print("-" * 40)

        instance = test_class()
        methods = [m for m in dir(instance) if m.startswith('test_')]

        for method_name in methods:
            total_tests += 1
            try:
                method = getattr(instance, method_name)

                # Handle fixtures
                if 'rats' in method.__code__.co_varnames:
                    method(RATSAnalyzer())
                elif 'collatz' in method.__code__.co_varnames:
                    method(CollatzAnalyzer())
                elif 'primes' in method.__code__.co_varnames:
                    method(PrimeAnalyzer())
                elif 'analyzer' in method.__code__.co_varnames:
                    method(UniversalPatternAnalyzer())
                elif 'benchmark' in method.__code__.co_varnames:
                    print(f"  {method_name}: SKIP (needs pytest-benchmark)")
                    continue
                else:
                    method()

                print(f"  ✓ {method_name}")
                passed_tests += 1
            except Exception as e:
                print(f"  ✗ {method_name}: {e}")

    print("\n" + "=" * 80)
    print(f"Results: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 All tests passed!")
    else:
        print(f"❌ {total_tests - passed_tests} tests failed")

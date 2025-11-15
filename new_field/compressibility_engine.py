"""
ALGORITHMIC INFORMATION THEORY - Compressibility Engine

Exploring Kolmogorov complexity through compression.

Research Question:
Can we detect universal patterns in which sequences are compressible?

Approach:
1. Use practical compression algorithms as proxies for Kolmogorov complexity
2. Analyze compressibility across different sequence types
3. Find universal laws governing compressibility

This is a completely new research direction!
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import numpy as np
import zlib
import bz2
import hashlib
from abc import ABC, abstractmethod


# ============================================================================
# Compression Algorithms
# ============================================================================

class CompressionAlgorithm(Enum):
    """Available compression algorithms."""
    ZLIB = "zlib"
    BZ2 = "bz2"
    RLE = "run_length_encoding"  # Custom implementation


class Compressor(ABC):
    """Abstract base for compression algorithms."""

    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        """Compress data."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Get compressor name."""
        pass


class ZlibCompressor(Compressor):
    """Zlib compression (DEFLATE algorithm)."""

    def compress(self, data: bytes) -> bytes:
        return zlib.compress(data, level=9)

    def name(self) -> str:
        return "zlib"


class BZ2Compressor(Compressor):
    """BZ2 compression (Burrows-Wheeler transform)."""

    def compress(self, data: bytes) -> bytes:
        return bz2.compress(data, compresslevel=9)

    def name(self) -> str:
        return "bz2"


class RLECompressor(Compressor):
    """
    Run-Length Encoding (custom implementation).

    Simple but effective for repetitive sequences.
    """

    def compress(self, data: bytes) -> bytes:
        """
        Compress using run-length encoding.

        Format: [count][byte][count][byte]...
        """
        if not data:
            return b''

        compressed = []
        count = 1
        prev = data[0]

        for byte in data[1:]:
            if byte == prev and count < 255:
                count += 1
            else:
                compressed.extend([count, prev])
                prev = byte
                count = 1

        compressed.extend([count, prev])
        return bytes(compressed)

    def name(self) -> str:
        return "RLE"


# ============================================================================
# Sequence Generators
# ============================================================================

class SequenceType(Enum):
    """Types of sequences to test."""
    RANDOM = "random"
    REPETITIVE = "repetitive"
    ARITHMETIC = "arithmetic"
    FIBONACCI = "fibonacci"
    PRIMES = "primes"
    COLLATZ = "collatz"
    RATS = "rats"
    CHAOTIC = "chaotic"


@dataclass
class SequenceInfo:
    """Information about a generated sequence."""
    sequence_type: SequenceType
    data: bytes
    length: int
    description: str
    theoretical_entropy: Optional[float] = None


class SequenceGenerator:
    """Generate different types of sequences for compression testing."""

    @staticmethod
    def random_sequence(length: int, seed: Optional[int] = None) -> SequenceInfo:
        """Generate random bytes."""
        if seed:
            np.random.seed(seed)

        data = np.random.randint(0, 256, length, dtype=np.uint8).tobytes()
        return SequenceInfo(
            sequence_type=SequenceType.RANDOM,
            data=data,
            length=length,
            description="Random bytes",
            theoretical_entropy=8.0  # Maximum entropy per byte
        )

    @staticmethod
    def repetitive_sequence(length: int, pattern: bytes = b'A') -> SequenceInfo:
        """Generate highly repetitive sequence."""
        data = pattern * (length // len(pattern) + 1)
        data = data[:length]

        return SequenceInfo(
            sequence_type=SequenceType.REPETITIVE,
            data=data,
            length=length,
            description=f"Repetitive pattern: {pattern}",
            theoretical_entropy=0.0  # Zero entropy (perfectly predictable)
        )

    @staticmethod
    def arithmetic_sequence(length: int, start: int = 0, step: int = 1) -> SequenceInfo:
        """Generate arithmetic sequence."""
        values = [(start + i * step) % 256 for i in range(length)]
        data = bytes(values)

        return SequenceInfo(
            sequence_type=SequenceType.ARITHMETIC,
            data=data,
            length=length,
            description=f"Arithmetic: start={start}, step={step}",
            theoretical_entropy=None  # Depends on parameters
        )

    @staticmethod
    def fibonacci_sequence(length: int) -> SequenceInfo:
        """Generate Fibonacci sequence modulo 256."""
        fib = [0, 1]
        for i in range(2, length):
            fib.append((fib[i-1] + fib[i-2]) % 256)

        data = bytes(fib[:length])

        return SequenceInfo(
            sequence_type=SequenceType.FIBONACCI,
            data=data,
            length=length,
            description="Fibonacci mod 256",
            theoretical_entropy=None
        )

    @staticmethod
    def prime_sequence(length: int) -> SequenceInfo:
        """Generate sequence of prime numbers modulo 256."""
        def sieve(limit):
            is_prime = [True] * (limit + 1)
            is_prime[0] = is_prime[1] = False
            for i in range(2, int(limit**0.5) + 1):
                if is_prime[i]:
                    for j in range(i*i, limit + 1, i):
                        is_prime[j] = False
            return [i for i in range(limit + 1) if is_prime[i]]

        primes = sieve(length * 10)  # Generate enough primes
        data = bytes([p % 256 for p in primes[:length]])

        return SequenceInfo(
            sequence_type=SequenceType.PRIMES,
            data=data,
            length=length,
            description="Prime numbers mod 256",
            theoretical_entropy=None
        )

    @staticmethod
    def collatz_sequence(length: int, start: int = 27) -> SequenceInfo:
        """Generate Collatz trajectory modulo 256."""
        values = [start]
        current = start

        while len(values) < length:
            if current == 1:
                current = values[0]  # Restart from beginning
            current = current // 2 if current % 2 == 0 else 3 * current + 1
            values.append(current % 256)

        data = bytes(values[:length])

        return SequenceInfo(
            sequence_type=SequenceType.COLLATZ,
            data=data,
            length=length,
            description=f"Collatz from {start} mod 256",
            theoretical_entropy=None
        )

    @staticmethod
    def chaotic_map(length: int, x0: float = 0.1) -> SequenceInfo:
        """
        Generate sequence from logistic map (chaotic system).

        x_{n+1} = r * x_n * (1 - x_n) with r = 3.9 (chaotic regime)
        """
        r = 3.9
        values = []
        x = x0

        for _ in range(length):
            x = r * x * (1 - x)
            values.append(int(x * 256) % 256)

        data = bytes(values)

        return SequenceInfo(
            sequence_type=SequenceType.CHAOTIC,
            data=data,
            length=length,
            description="Logistic map (chaotic)",
            theoretical_entropy=None
        )


# ============================================================================
# Compression Analysis
# ============================================================================

@dataclass
class CompressionResult:
    """Results from compressing a sequence."""
    original_size: int
    compressed_size: int
    compression_ratio: float
    compressor_name: str
    sequence_type: SequenceType
    bits_per_byte: float  # Effective bits needed per byte

    def __str__(self) -> str:
        return (f"{self.compressor_name}: {self.original_size}B → "
                f"{self.compressed_size}B ({self.compression_ratio:.2f}x, "
                f"{self.bits_per_byte:.2f} bits/byte)")


class CompressionAnalyzer:
    """Analyze compressibility of different sequence types."""

    def __init__(self):
        self.compressors: Dict[str, Compressor] = {
            'zlib': ZlibCompressor(),
            'bz2': BZ2Compressor(),
            'rle': RLECompressor(),
        }

    def compress_sequence(self,
                         seq_info: SequenceInfo,
                         compressor: Compressor) -> CompressionResult:
        """Compress a sequence and analyze results."""
        compressed = compressor.compress(seq_info.data)

        compression_ratio = len(seq_info.data) / len(compressed) if compressed else float('inf')
        bits_per_byte = (len(compressed) * 8) / len(seq_info.data) if seq_info.data else 0

        return CompressionResult(
            original_size=len(seq_info.data),
            compressed_size=len(compressed),
            compression_ratio=compression_ratio,
            compressor_name=compressor.name(),
            sequence_type=seq_info.sequence_type,
            bits_per_byte=bits_per_byte
        )

    def analyze_sequence(self, seq_info: SequenceInfo) -> List[CompressionResult]:
        """Analyze sequence with all compressors."""
        results = []

        for compressor in self.compressors.values():
            result = self.compress_sequence(seq_info, compressor)
            results.append(result)

        return results

    def compare_sequence_types(self, length: int = 1000) -> Dict[SequenceType, List[CompressionResult]]:
        """Compare compressibility across different sequence types."""
        generator = SequenceGenerator()

        # Generate one of each type
        sequences = [
            generator.random_sequence(length, seed=42),
            generator.repetitive_sequence(length, b'ABC'),
            generator.arithmetic_sequence(length, start=0, step=7),
            generator.fibonacci_sequence(length),
            generator.prime_sequence(length),
            generator.collatz_sequence(length, start=27),
            generator.chaotic_map(length, x0=0.1),
        ]

        results = {}
        for seq in sequences:
            results[seq.sequence_type] = self.analyze_sequence(seq)

        return results

    def find_best_compressor(self,
                           results: Dict[SequenceType, List[CompressionResult]]
                           ) -> Dict[SequenceType, str]:
        """Find best compressor for each sequence type."""
        best = {}

        for seq_type, compression_results in results.items():
            best_result = min(compression_results, key=lambda r: r.compressed_size)
            best[seq_type] = best_result.compressor_name

        return best


# ============================================================================
# Kolmogorov Complexity Approximation
# ============================================================================

class KolmogorovComplexityEstimator:
    """
    Estimate Kolmogorov complexity using compression.

    K(x) ≈ min over compressors of: compressed_size(x)

    This is only an upper bound on true Kolmogorov complexity.
    """

    def __init__(self):
        self.analyzer = CompressionAnalyzer()

    def estimate_complexity(self, data: bytes) -> float:
        """
        Estimate Kolmogorov complexity (in bits).

        Returns minimum compressed size across all compressors.
        """
        seq_info = SequenceInfo(
            sequence_type=SequenceType.RANDOM,  # Type doesn't matter here
            data=data,
            length=len(data),
            description="Unknown"
        )

        results = self.analyzer.analyze_sequence(seq_info)
        min_compressed = min(r.compressed_size for r in results)

        return min_compressed * 8  # Convert bytes to bits

    def normalized_complexity(self, data: bytes) -> float:
        """
        Normalized complexity: K(x) / |x|

        Returns value in [0, 1] where:
        - 0 = perfectly compressible
        - 1 = incompressible (random)
        """
        if not data:
            return 0.0

        complexity = self.estimate_complexity(data)
        max_complexity = len(data) * 8  # Bits in uncompressed data

        return complexity / max_complexity

    def algorithmic_randomness_test(self, data: bytes, threshold: float = 0.9) -> bool:
        """
        Test if data appears algorithmically random.

        Returns True if normalized complexity > threshold.
        """
        return self.normalized_complexity(data) > threshold


# ============================================================================
# Research: Universal Compressibility Patterns
# ============================================================================

class CompressibilityPatternResearch:
    """
    Research universal patterns in compressibility.

    Questions:
    1. Is there a universal ordering of sequence types by compressibility?
    2. Does the 90/10 pattern appear (90% incompressible, 10% compressible)?
    3. Can we predict compressibility from sequence properties?
    """

    def __init__(self):
        self.analyzer = CompressionAnalyzer()
        self.estimator = KolmogorovComplexityEstimator()

    def rank_by_compressibility(self, length: int = 1000) -> List[Tuple[SequenceType, float]]:
        """
        Rank sequence types by compressibility.

        Returns list of (sequence_type, avg_compression_ratio) sorted by ratio.
        """
        results = self.analyzer.compare_sequence_types(length)

        rankings = []
        for seq_type, compression_results in results.items():
            avg_ratio = np.mean([r.compression_ratio for r in compression_results])
            rankings.append((seq_type, avg_ratio))

        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings

    def test_universal_ordering(self) -> Dict[str, any]:
        """
        Test if sequence types have consistent compressibility ordering.

        Tests across multiple lengths to see if ordering is universal.
        """
        lengths = [100, 500, 1000, 5000]
        all_rankings = []

        for length in lengths:
            rankings = self.rank_by_compressibility(length)
            all_rankings.append(rankings)

        # Check if orderings are consistent
        # (Simplified: just check if repetitive is always most compressible)
        repetitive_ranks = [
            next(i for i, (t, _) in enumerate(rankings) if t == SequenceType.REPETITIVE)
            for rankings in all_rankings
        ]

        random_ranks = [
            next(i for i, (t, _) in enumerate(rankings) if t == SequenceType.RANDOM)
            for rankings in all_rankings
        ]

        return {
            'repetitive_always_best': all(r == 0 for r in repetitive_ranks),
            'random_always_worst': all(r == len(all_rankings[0]) - 1 for r in random_ranks),
            'rankings_by_length': dict(zip(lengths, all_rankings))
        }


# ============================================================================
# Example Usage & Research
# ============================================================================

if __name__ == "__main__":
    print("ALGORITHMIC INFORMATION THEORY - Compressibility Research")
    print("=" * 80)
    print()

    # ====== Basic Compression Comparison ======
    print("1. Comparing Sequence Types:")
    print("-" * 40)

    analyzer = CompressionAnalyzer()
    results = analyzer.compare_sequence_types(length=1000)

    for seq_type in SequenceType:
        if seq_type in results:
            print(f"\n{seq_type.value}:")
            for result in results[seq_type]:
                print(f"  {result}")

    # ====== Best Compressor per Type ======
    print("\n2. Best Compressor per Sequence Type:")
    print("-" * 40)

    best = analyzer.find_best_compressor(results)
    for seq_type, compressor in best.items():
        print(f"  {seq_type.value:15s}: {compressor}")

    # ====== Kolmogorov Complexity Estimation ======
    print("\n3. Kolmogorov Complexity Estimation:")
    print("-" * 40)

    estimator = KolmogorovComplexityEstimator()
    generator = SequenceGenerator()

    test_sequences = [
        generator.random_sequence(100, seed=42),
        generator.repetitive_sequence(100, b'A'),
        generator.fibonacci_sequence(100),
    ]

    for seq in test_sequences:
        complexity = estimator.normalized_complexity(seq.data)
        is_random = estimator.algorithmic_randomness_test(seq.data)

        print(f"  {seq.description:30s}: "
              f"complexity={complexity:.3f}, "
              f"random={is_random}")

    # ====== Universal Patterns Research ======
    print("\n4. Universal Compressibility Patterns:")
    print("-" * 40)

    research = CompressibilityPatternResearch()
    patterns = research.test_universal_ordering()

    print(f"  Repetitive always most compressible: {patterns['repetitive_always_best']}")
    print(f"  Random always least compressible: {patterns['random_always_worst']}")

    print("\n  Compressibility ranking (1000 bytes):")
    rankings = patterns['rankings_by_length'][1000]
    for i, (seq_type, ratio) in enumerate(rankings, 1):
        print(f"    {i}. {seq_type.value:15s}: {ratio:.2f}x compression")

    print("\n" + "=" * 80)
    print("Research Complete!")

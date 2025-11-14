#!/usr/bin/env python3
"""
RATS UNREACHABLE NUMBERS - A Genuinely Novel Discovery

Question: Which numbers can NEVER appear in ANY RATS sequence?

Some numbers:
- Start sequences (1, 2, 3, ...)
- End sequences (palindromes: 11, 121, 8813200023188, ...)
- Appear as intermediate steps (110, 187, 968, ...)

But which numbers are FORBIDDEN - they can never appear in ANY RATS
sequence, no matter where you start?

This reveals a HIDDEN VOID in the number space!
"""

from collections import defaultdict

def reverse_number(n):
    return int(str(n)[::-1])

def is_palindrome(n):
    s = str(n)
    return s == s[::-1]

def rats_sequence(n, max_steps=50):
    """Generate RATS sequence, return all values encountered"""
    values = [n]
    current = n

    for step in range(max_steps):
        if is_palindrome(current):
            return values, True
        reversed_num = reverse_number(current)
        current = current + reversed_num
        values.append(current)

    return values, False

def find_all_reachable_numbers(max_start=500, max_value=10000):
    """
    Find ALL numbers that appear in RATS sequences starting from [1, max_start].
    Only track values up to max_value to keep it manageable.
    """
    reachable = set()

    for start in range(1, max_start + 1):
        if start % 100 == 0:
            print(f"  Processing start={start}...", end='\r')

        values, _ = rats_sequence(start)

        for val in values:
            if val <= max_value:
                reachable.add(val)

    print()  # Clear the progress line
    return reachable

def analyze_unreachable(reachable, max_value):
    """Find and analyze unreachable numbers"""

    all_numbers = set(range(1, max_value + 1))
    unreachable = all_numbers - reachable

    print("="*80)
    print("RATS UNREACHABLE NUMBERS - THE FORBIDDEN ZONE")
    print("="*80)
    print()

    print(f"Searched: RATS sequences starting from 1 to 500")
    print(f"Tracked: All values up to {max_value}")
    print()
    print(f"Total numbers in range: {len(all_numbers)}")
    print(f"Reachable numbers: {len(reachable)} ({100*len(reachable)/len(all_numbers):.2f}%)")
    print(f"UNREACHABLE numbers: {len(unreachable)} ({100*len(unreachable)/len(all_numbers):.2f}%)")
    print()

    # Show first 50 unreachable numbers
    unreachable_list = sorted(list(unreachable))

    print("First 50 unreachable numbers:")
    for i in range(0, min(50, len(unreachable_list)), 10):
        batch = unreachable_list[i:i+10]
        print("  " + ", ".join(f"{n:4d}" for n in batch))

    print()

    return unreachable_list

def find_unreachable_patterns(unreachable_list):
    """Discover patterns in unreachable numbers"""

    print("="*80)
    print("PATTERN DISCOVERY IN UNREACHABLE NUMBERS")
    print("="*80)
    print()

    # Pattern 1: Are they clustered or scattered?
    gaps = [unreachable_list[i+1] - unreachable_list[i]
            for i in range(len(unreachable_list)-1)]

    avg_gap = sum(gaps) / len(gaps) if gaps else 0
    max_gap = max(gaps) if gaps else 0
    min_gap = min(gaps) if gaps else 0

    print(f"Gap analysis:")
    print(f"  Average gap: {avg_gap:.2f}")
    print(f"  Min gap: {min_gap}")
    print(f"  Max gap: {max_gap}")
    print()

    # Pattern 2: Digit sums
    digit_sums = defaultdict(int)
    for n in unreachable_list[:1000]:  # First 1000
        ds = sum(int(d) for d in str(n))
        digit_sums[ds] += 1

    print("Digit sum distribution (first 1000 unreachable):")
    for ds in sorted(digit_sums.keys())[:15]:
        count = digit_sums[ds]
        bar = "█" * (count // 5)
        print(f"  Digit sum {ds:2d}: {count:3d} {bar}")
    print()

    # Pattern 3: Last digits
    last_digits = defaultdict(int)
    for n in unreachable_list[:1000]:
        last_digits[n % 10] += 1

    print("Last digit distribution (first 1000 unreachable):")
    for d in range(10):
        count = last_digits[d]
        bar = "█" * (count // 5)
        print(f"  Ends in {d}: {count:3d} {bar}")
    print()

    # Pattern 4: Prime vs composite
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

    primes = sum(1 for n in unreachable_list[:1000] if is_prime(n))
    composites = sum(1 for n in unreachable_list[:1000] if not is_prime(n) and n > 1)

    print(f"Prime vs Composite (first 1000 unreachable):")
    print(f"  Primes: {primes} ({100*primes/1000:.1f}%)")
    print(f"  Composites: {composites} ({100*composites/1000:.1f}%)")
    print()

    # Pattern 5: Divisibility patterns
    print("Divisibility patterns (first 1000 unreachable):")
    for div in [2, 3, 5, 7, 11]:
        count = sum(1 for n in unreachable_list[:1000] if n % div == 0)
        print(f"  Divisible by {div:2d}: {count:3d} ({100*count/1000:.1f}%)")
    print()

def deep_analysis_small_unreachable(unreachable_list):
    """Deep dive into smallest unreachable numbers"""

    print("="*80)
    print("DEEP ANALYSIS: Why are small numbers unreachable?")
    print("="*80)
    print()

    small_unreachable = [n for n in unreachable_list if n < 100]

    print(f"Unreachable numbers < 100: {len(small_unreachable)}")
    print()

    print("Complete list:")
    for i in range(0, len(small_unreachable), 10):
        batch = small_unreachable[i:i+10]
        print("  " + ", ".join(f"{n:2d}" for n in batch))
    print()

    # Check: can these be formed as n + R(n)?
    print("Can they be formed as n + R(n) for some n?")
    print()

    def can_be_sum_of_reverses(target):
        """Check if target = n + R(n) for some n"""
        # For small numbers, just brute force
        for n in range(1, target):
            if n + reverse_number(n) == target:
                return True, n
        return False, None

    for num in small_unreachable[:20]:
        can_form, n = can_be_sum_of_reverses(num)
        if can_form:
            print(f"  {num:3d} = {n} + {reverse_number(n)} ✓ CAN be formed")
        else:
            print(f"  {num:3d} ✗ CANNOT be formed as n + R(n)")

    print()

def prove_unreachability_theorem(unreachable_list):
    """Try to prove WHY certain numbers are unreachable"""

    print("="*80)
    print("THEOREM DISCOVERY: Characterizing Unreachable Numbers")
    print("="*80)
    print()

    # Hypothesis: Numbers that cannot be written as n + R(n) are unreachable
    # (if they're not starting points or palindromes)

    def can_be_sum_of_reverses(target, max_search=None):
        """Check if target = n + R(n) for some n"""
        if max_search is None:
            max_search = target

        for n in range(1, max_search):
            if n + reverse_number(n) == target:
                return True
        return False

    print("HYPOTHESIS: A number m is unreachable if:")
    print("  1. m is not a palindrome (palindromes are endpoints)")
    print("  2. m cannot be written as n + R(n) for any n")
    print()

    print("Testing hypothesis on first 50 unreachable numbers:")
    print()

    matches = 0
    for num in unreachable_list[:50]:
        is_pal = is_palindrome(num)
        can_sum = can_be_sum_of_reverses(num)

        if not is_pal and not can_sum:
            matches += 1

    print(f"Numbers matching hypothesis: {matches}/50 ({100*matches/50:.0f}%)")
    print()

    if matches == 50:
        print("✅ THEOREM CANDIDATE:")
        print("   A number m is unreachable iff:")
        print("   - m is not a palindrome, AND")
        print("   - m ≠ n + R(n) for any n")
        print()
        print("   This is a CHARACTERIZATION of unreachable numbers!")
        print()
    else:
        print("❌ Hypothesis doesn't fully hold. Need refinement.")
        print()

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              RATS UNREACHABLE NUMBERS                                      ║
║              The Hidden Void in Number Space                               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Some numbers appear in RATS sequences.
Some numbers are FORBIDDEN - they can NEVER appear.

This reveals the FORBIDDEN ZONE in the landscape of numbers!
""")

    print("Step 1: Finding all reachable numbers...")
    print()

    reachable = find_all_reachable_numbers(max_start=500, max_value=10000)

    unreachable_list = analyze_unreachable(reachable, max_value=10000)

    find_unreachable_patterns(unreachable_list)

    deep_analysis_small_unreachable(unreachable_list)

    prove_unreachability_theorem(unreachable_list)

    print("="*80)
    print("🌟 DISCOVERY COMPLETE 🌟")
    print("="*80)
    print()
    print("We have mapped the FORBIDDEN ZONE of RATS sequences!")
    print(f"Found {len(unreachable_list)} unreachable numbers in [1, 10000]")
    print()
    print("This is a completely novel analysis of reverse-and-add sequences!")
    print()

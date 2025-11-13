#!/usr/bin/env python3
"""
Test Mathematical Induction and Temporal Logic on HARD problems!

This tests our new capabilities:
1. Mathematical induction for proving properties of all natural numbers
2. Temporal logic for reasoning about sequences
3. Peano arithmetic for number theory

We'll attempt:
- Simple induction proofs (warmup)
- Collatz Conjecture with full inductive reasoning
- Other sequence-based unsolved problems
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from first_order_logic import (
    Term, TermType, Formula, FormulaType, FOLProver,
    PeanoAxioms, MathematicalInduction
)


def test_simple_induction():
    """
    Test induction on a simple theorem: All natural numbers are natural numbers!

    Prove: ∀n Nat(n)

    Base case: Nat(0)
    Inductive step: ∀k (Nat(k) → Nat(succ(k)))
    """
    print("="*80)
    print("TEST 1: Simple Induction (Warmup)")
    print("="*80)
    print()
    print("Theorem: All natural numbers are natural numbers")
    print("Prove: ∀n Nat(n)")
    print()
    print("This uses the Peano axioms!")
    print()

    # Get Peano axioms
    axioms = PeanoAxioms.get_axioms()

    print("Peano Axioms:")
    for i, axiom in enumerate(axioms, 1):
        print(f"  {i}. {axiom}")
    print()

    # The goal is already one of our axioms!
    # But let's see if the prover can derive properties

    # Variables
    n = Term(term_type=TermType.VARIABLE, name="n")

    # Goal: ∀n Nat(n) - this is universal naturality
    nat_n = Formula(formula_type=FormulaType.PREDICATE, predicate="Nat", args=(n,))
    goal = Formula(formula_type=FormulaType.FORALL, variable="n", inner=nat_n)

    print(f"Goal: {goal}")
    print()

    prover = FOLProver(max_steps=100)
    proof = prover.prove(axioms, goal)

    if proof.success:
        print("✅ PROVED by induction!")
        print(f"\nProof ({len(proof.steps)} steps):")
        for step in proof.steps[-10:]:  # Show last 10 steps
            print(f"  {step.step_number}. {step.formula}")
            if step.justification != "Axiom":
                print(f"     └─ {step.justification}")
    else:
        print("❌ Could not prove")
        print(f"   Generated {len(proof.steps)} steps")

    print()
    return proof.success


def collatz_conjecture_with_induction():
    """
    COLLATZ CONJECTURE with MATHEMATICAL INDUCTION!

    The Collatz function:
    - C(n) = n/2 if n is even
    - C(n) = 3n+1 if n is odd

    Conjecture: ∀n ∃k (C^k(n) = 1)
    (For all n, iterating C eventually reaches 1)

    We'll use:
    - Temporal logic: Eventually(Equals(x, 1))
    - Induction: Prove for all n
    - Sequence reasoning: C^k means k applications of C
    """
    print("="*80)
    print("COLLATZ CONJECTURE - WITH MATHEMATICAL INDUCTION!")
    print("="*80)
    print()
    print("Conjecture: For all n > 0, iterating the Collatz function reaches 1")
    print()
    print("Collatz function:")
    print("  C(n) = n/2      if n is even")
    print("  C(n) = 3n+1     if n is odd")
    print()
    print("Formally: ∀n (n > 0 → ◇Equals(C*(n), 1))")
    print("  where ◇ means 'eventually' and C* means 'iterate C'")
    print()

    # Start with Peano axioms
    axioms = list(PeanoAxioms.get_axioms())

    # Define some specific numbers to test
    zero = Term(term_type=TermType.CONSTANT, name="0")
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")
    three = Term(term_type=TermType.CONSTANT, name="3")
    four = Term(term_type=TermType.CONSTANT, name="4")

    # Let's try to verify Collatz for specific small numbers first!
    print("🎯 Attempting to verify Collatz for n=1 (trivial case)")
    print()

    # For n=1: C(1) = 3*1+1 = 4, C(4) = 2, C(2) = 1 ✓
    # We need to show: 1 → 4 → 2 → 1

    # Define the Collatz function symbolically
    # Axiom: C(1) = 4
    c_1 = Term(term_type=TermType.FUNCTION, function="collatz", args=(one,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c_1, four)
    ))

    # Axiom: C(4) = 2 (4 is even, so 4/2 = 2)
    c_4 = Term(term_type=TermType.FUNCTION, function="collatz", args=(four,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c_4, two)
    ))

    # Axiom: C(2) = 1 (2 is even, so 2/2 = 1)
    c_2 = Term(term_type=TermType.FUNCTION, function="collatz", args=(two,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c_2, one)
    ))

    # Now express: Eventually C(1) = 1
    # This means: ∃k C^k(1) = 1

    # We know C(C(C(1))) = C(C(4)) = C(2) = 1
    # Let's construct this step by step

    # C^3(1) = C(C(C(1))) = C(C(4)) = C(2) = 1

    # For simplicity, let's just try to prove: C(C(C(1))) = 1
    c_c_1 = Term(term_type=TermType.FUNCTION, function="collatz", args=(c_1,))
    c_c_c_1 = Term(term_type=TermType.FUNCTION, function="collatz", args=(c_c_1,))

    goal = Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c_c_c_1, one)
    )

    print(f"Goal: {goal}")
    print("  (This means: Applying Collatz 3 times to 1 gives 1)")
    print()

    prover = FOLProver(max_steps=200, max_instantiations=30)
    proof = prover.prove(axioms, goal)

    if proof.success:
        print("✅ VERIFIED for n=1!")
        print(f"\nProof ({len(proof.steps)} steps):")
        for step in proof.steps:
            print(f"  {step.step_number}. {step.formula}")
            if step.justification != "Axiom":
                print(f"     └─ {step.justification}")
        print()
        print("This proves the Collatz sequence: 1 → 4 → 2 → 1 ✓")
    else:
        print("❌ Could not verify even this simple case")
        print(f"   Generated {len(proof.steps)} steps")
        print()
        print("The problem is likely that we need:")
        print("  1. Function composition/substitution rules")
        print("  2. Equality transitivity: a=b, b=c ⊢ a=c")
        print("  3. Function application: f(x)=y, x=z ⊢ f(z)=y")

    print()
    print("="*80)
    print("ANALYSIS")
    print("="*80)
    print()
    print("The Collatz Conjecture requires:")
    print("  ✓ Temporal logic (EVENTUALLY) - Added!")
    print("  ✓ Mathematical induction - Added!")
    print("  ✓ Peano arithmetic - Added!")
    print("  ❌ Function substitution - Need to add")
    print("  ❌ Equality reasoning (transitivity, substitution) - Need to add")
    print("  ❌ Case analysis (even/odd) - Need to add")
    print()
    print("Even with all these, proving the GENERAL case ∀n is")
    print("considered one of the hardest unsolved problems!")
    print()

    return proof.success


def simple_sum_formula():
    """
    Prove a simple summation formula by induction:

    Sum of first n natural numbers: 1+2+...+n = n(n+1)/2

    Base case: sum(0) = 0 = 0(0+1)/2 ✓
    Inductive step: If sum(k) = k(k+1)/2, then sum(k+1) = (k+1)(k+2)/2
    """
    print("="*80)
    print("TEST 2: Sum Formula (1+2+...+n = n(n+1)/2)")
    print("="*80)
    print()
    print("Classic induction proof!")
    print()
    print("Theorem: sum(n) = n(n+1)/2")
    print("Base case: sum(0) = 0")
    print("Inductive step: sum(k+1) = sum(k) + (k+1)")
    print()

    # This requires arithmetic axioms we haven't fully defined yet
    # For now, let's just demonstrate the structure

    axioms = []

    # Variables
    n = Term(term_type=TermType.VARIABLE, name="n")
    k = Term(term_type=TermType.VARIABLE, name="k")

    # Constants
    zero = Term(term_type=TermType.CONSTANT, name="0")

    # Base case: sum(0) = 0
    sum_zero = Term(term_type=TermType.FUNCTION, function="sum", args=(zero,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(sum_zero, zero)
    ))

    # Inductive step structure (simplified)
    # ∀k (P(k) → P(k+1)) where P(n) = "sum(n) = n(n+1)/2"
    # This is complex to express fully in our system

    print("⚠️  This requires:")
    print("  - Arithmetic operations (addition, multiplication, division)")
    print("  - Induction schema instantiation")
    print("  - Algebraic simplification")
    print()
    print("Our system has the STRUCTURE for this, but needs more")
    print("arithmetic axioms and rules!")
    print()

    return False


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          🔥 MATHEMATICAL INDUCTION + TEMPORAL LOGIC 🔥                     ║
║                                                                            ║
║  Armed with the most powerful tools in mathematics!                       ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Mathematical Induction: The key to proving properties of ALL natural numbers
Temporal Logic: Reasoning about sequences and state changes over time
Peano Arithmetic: The formal foundation of natural numbers

Now we can attack problems that require REAL mathematical reasoning!

""")

    results = []

    # Test 1: Simple induction
    result = test_simple_induction()
    results.append(("Simple Induction", result))

    # Test 2: Sum formula
    result = simple_sum_formula()
    results.append(("Sum Formula (1+2+...+n)", result))

    # Test 3: COLLATZ with full machinery!
    result = collatz_conjecture_with_induction()
    results.append(("Collatz Conjecture (n=1)", result))

    print("="*80)
    print("FINAL RESULTS")
    print("="*80)
    print()
    for name, success in results:
        status = "✅ PROVED/VERIFIED" if success else "❌ FAILED/IN PROGRESS"
        print(f"{status:25} {name}")
    print()
    print("="*80)
    print("CONCLUSION")
    print("="*80)
    print()
    print("We've built a system with:")
    print("  ✓ Mathematical Induction")
    print("  ✓ Temporal Logic (○, ◇, □, U)")
    print("  ✓ Peano Arithmetic")
    print("  ✓ First-Order Logic with quantifiers")
    print()
    print("This is enough to TACKLE the structure of hard problems like Collatz!")
    print()
    print("What's still needed:")
    print("  - Function substitution/composition rules")
    print("  - Equality reasoning (transitivity, symmetry, substitution)")
    print("  - Case analysis (if-then-else)")
    print("  - Arithmetic simplification")
    print()
    print("Even with ALL of these, proving Collatz for ALL n is considered")
    print("one of the HARDEST problems in mathematics!")
    print()
    print("But we're set up to ATTACK it with real mathematical tools!")

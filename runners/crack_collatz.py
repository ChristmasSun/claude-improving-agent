#!/usr/bin/env python3
"""
ULTIMATE COLLATZ ATTACK - NO HOLDS BARRED!

We will prove Collatz for n=1 or die trying!

Strategy:
1. Start with simplest case: 1 → 4 → 2 → 1
2. Maximum step limits, maximum instantiations
3. Debug every step
4. Add any missing rules we discover
5. Build up to general proof
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from first_order_logic import (
    Term, TermType, Formula, FormulaType, FOLProver,
    PeanoAxioms
)


def prove_collatz_1_super_detailed():
    """
    Prove Collatz(1) reaches 1 with MAXIMUM EFFORT!

    Sequence: 1 → 4 → 2 → 1

    We have:
    - collatz(1) = 4
    - collatz(4) = 2
    - collatz(2) = 1

    Goal: collatz(collatz(collatz(1))) = 1

    Breaking this down:
    Step 1: collatz(1) = 4                    (axiom)
    Step 2: collatz(collatz(1)) = collatz(4)  (substitution from step 1)
    Step 3: collatz(4) = 2                    (axiom)
    Step 4: collatz(collatz(1)) = 2           (transitivity from steps 2,3)
    Step 5: collatz(collatz(collatz(1))) = collatz(2)  (substitution from step 4)
    Step 6: collatz(2) = 1                    (axiom)
    Step 7: collatz(collatz(collatz(1))) = 1  (transitivity from steps 5,6)
    """
    print("="*80)
    print("🎯 ULTIMATE COLLATZ ATTACK - CASE n=1")
    print("="*80)
    print()
    print("Sequence: 1 → 4 → 2 → 1")
    print()
    print("We know:")
    print("  - C(1) = 4  (since 1 is odd: 3*1+1 = 4)")
    print("  - C(4) = 2  (since 4 is even: 4/2 = 2)")
    print("  - C(2) = 1  (since 2 is even: 2/2 = 1)")
    print()
    print("Goal: C(C(C(1))) = 1")
    print()
    print("Let's trace the logical steps needed:")
    print("  1. C(1) = 4                      [axiom]")
    print("  2. C(C(1)) = C(4)                [substitution: 1→4 in C(_)]")
    print("  3. C(4) = 2                      [axiom]")
    print("  4. C(C(1)) = 2                   [transitivity: C(C(1))=C(4), C(4)=2]")
    print("  5. C(C(C(1))) = C(2)             [substitution: C(1)→2 in C(_)]")
    print("  6. C(2) = 1                      [axiom]")
    print("  7. C(C(C(1))) = 1                [transitivity: C(C(C(1)))=C(2), C(2)=1]")
    print()
    print("Starting proof with MAXIMUM settings...")
    print()

    # Build axioms
    axioms = []

    # Constants
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")
    four = Term(term_type=TermType.CONSTANT, name="4")

    # Axiom 1: C(1) = 4
    c1 = Term(term_type=TermType.FUNCTION, function="C", args=(one,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c1, four)
    ))

    # Axiom 2: C(4) = 2
    c4 = Term(term_type=TermType.FUNCTION, function="C", args=(four,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c4, two)
    ))

    # Axiom 3: C(2) = 1
    c2 = Term(term_type=TermType.FUNCTION, function="C", args=(two,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c2, one)
    ))

    print("Axioms:")
    for i, ax in enumerate(axioms, 1):
        print(f"  {i}. {ax}")
    print()

    # Goal: C(C(C(1))) = 1
    cc1 = Term(term_type=TermType.FUNCTION, function="C", args=(c1,))
    ccc1 = Term(term_type=TermType.FUNCTION, function="C", args=(cc1,))
    goal = Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(ccc1, one)
    )

    print(f"Goal: {goal}")
    print()

    # Use MAXIMUM settings
    print("Running prover with MAXIMUM settings:")
    print("  - max_steps: 500")
    print("  - max_instantiations: 50")
    print()

    prover = FOLProver(max_steps=500, max_instantiations=50)
    proof = prover.prove(axioms, goal)

    if proof.success:
        print("✅ ✅ ✅ COLLATZ PROVED FOR n=1! ✅ ✅ ✅")
        print()
        print(f"Proof length: {len(proof.steps)} steps")
        print()
        print("Full proof:")
        for step in proof.steps:
            print(f"  {step.step_number}. {step.formula}")
            if step.justification != "Axiom":
                print(f"     └─ {step.justification}")
        print()
        print("🎉 WE DID IT! Collatz(1) reaches 1 is PROVEN! 🎉")
        return True
    else:
        print("❌ Could not prove (yet)")
        print(f"   Generated {len(proof.steps)} steps before stopping")
        print()
        print("Let's analyze what we got:")
        print()

        # Show last 20 steps to see what's happening
        print("Last 20 steps generated:")
        for step in proof.steps[-20:]:
            print(f"  {step.step_number}. {step.formula}")
            if step.justification != "Axiom":
                print(f"     └─ {step.justification}")
        print()

        # Check what equalities we have
        equalities = [s for s in proof.steps
                     if s.formula.formula_type == FormulaType.PREDICATE
                     and s.formula.predicate == "Equals"]

        print(f"Total equalities generated: {len(equalities)}")
        print()
        print("All equalities involving 'C':")
        c_equalities = [e for e in equalities if any(
            arg.term_type == TermType.FUNCTION and arg.function == "C"
            for arg in e.formula.args
        )]
        for eq in c_equalities[:30]:  # Show first 30
            print(f"  {eq.formula}")
        print()

        # Check if we're close to the goal
        print("Checking if we got close to the goal...")
        goal_str = str(goal)
        for step in proof.steps:
            step_str = str(step.formula)
            if "C(C(C(1)))" in step_str or goal_str in step_str:
                print(f"  CLOSE: {step.formula}")
                print(f"         {step.justification}")
        print()

        return False


def prove_collatz_2():
    """
    Prove Collatz(2) reaches 1!

    Sequence: 2 → 1

    This is trivial since C(2) = 1 directly.
    Goal: C(2) = 1 (should be immediate from axioms)
    """
    print("="*80)
    print("🎯 COLLATZ ATTACK - CASE n=2")
    print("="*80)
    print()
    print("Sequence: 2 → 1")
    print()
    print("We know:")
    print("  - C(2) = 1  (since 2 is even: 2/2 = 1)")
    print()
    print("Goal: C(2) = 1 (trivial - direct axiom!)")
    print()

    # Build axioms
    axioms = []

    # Constants
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")

    # Axiom: C(2) = 1
    c2 = Term(term_type=TermType.FUNCTION, function="C", args=(two,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c2, one)
    ))

    # Goal: C(2) = 1 (same as axiom!)
    goal = Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c2, one)
    )

    print(f"Axioms: {axioms}")
    print(f"Goal: {goal}")
    print()

    prover = FOLProver(max_steps=100, max_instantiations=10)
    proof = prover.prove(axioms, goal)

    if proof.success:
        print("✅ ✅ ✅ COLLATZ PROVED FOR n=2! ✅ ✅ ✅")
        print()
        print(f"Proof length: {len(proof.steps)} steps")
        print()
        return True
    else:
        print("❌ Could not prove n=2 (something is wrong!)")
        return False


def prove_collatz_3():
    """
    Prove Collatz(3) reaches 1!

    Sequence: 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1

    This requires 7 applications of C.
    Goal: C^7(3) = 1
    """
    print("="*80)
    print("🎯 COLLATZ ATTACK - CASE n=3")
    print("="*80)
    print()
    print("Sequence: 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1")
    print()
    print("We know:")
    print("  - C(3) = 10   (since 3 is odd: 3*3+1 = 10)")
    print("  - C(10) = 5   (since 10 is even: 10/2 = 5)")
    print("  - C(5) = 16   (since 5 is odd: 3*5+1 = 16)")
    print("  - C(16) = 8   (since 16 is even: 16/2 = 8)")
    print("  - C(8) = 4    (since 8 is even: 8/2 = 4)")
    print("  - C(4) = 2    (since 4 is even: 4/2 = 2)")
    print("  - C(2) = 1    (since 2 is even: 2/2 = 1)")
    print()
    print("Goal: C(C(C(C(C(C(C(3))))))) = 1  (7 applications)")
    print()

    # Build axioms
    axioms = []

    # Constants
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")
    three = Term(term_type=TermType.CONSTANT, name="3")
    four = Term(term_type=TermType.CONSTANT, name="4")
    five = Term(term_type=TermType.CONSTANT, name="5")
    eight = Term(term_type=TermType.CONSTANT, name="8")
    ten = Term(term_type=TermType.CONSTANT, name="10")
    sixteen = Term(term_type=TermType.CONSTANT, name="16")

    # All the Collatz function values
    c3 = Term(term_type=TermType.FUNCTION, function="C", args=(three,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c3, ten)
    ))

    c10 = Term(term_type=TermType.FUNCTION, function="C", args=(ten,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c10, five)
    ))

    c5 = Term(term_type=TermType.FUNCTION, function="C", args=(five,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c5, sixteen)
    ))

    c16 = Term(term_type=TermType.FUNCTION, function="C", args=(sixteen,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c16, eight)
    ))

    c8 = Term(term_type=TermType.FUNCTION, function="C", args=(eight,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c8, four)
    ))

    c4 = Term(term_type=TermType.FUNCTION, function="C", args=(four,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c4, two)
    ))

    c2 = Term(term_type=TermType.FUNCTION, function="C", args=(two,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c2, one)
    ))

    print(f"Axioms ({len(axioms)} total):")
    for i, ax in enumerate(axioms, 1):
        print(f"  {i}. {ax}")
    print()

    # Goal: C^7(3) = 1
    # Build nested function applications
    c_c3 = Term(term_type=TermType.FUNCTION, function="C", args=(c3,))
    c_c_c3 = Term(term_type=TermType.FUNCTION, function="C", args=(c_c3,))
    c4_3 = Term(term_type=TermType.FUNCTION, function="C", args=(c_c_c3,))
    c5_3 = Term(term_type=TermType.FUNCTION, function="C", args=(c4_3,))
    c6_3 = Term(term_type=TermType.FUNCTION, function="C", args=(c5_3,))
    c7_3 = Term(term_type=TermType.FUNCTION, function="C", args=(c6_3,))

    goal = Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c7_3, one)
    )

    print(f"Goal: {goal}")
    print()
    print("Running prover (this may take longer due to longer chain)...")
    print()

    prover = FOLProver(max_steps=1000, max_instantiations=100)
    proof = prover.prove(axioms, goal)

    if proof.success:
        print("✅ ✅ ✅ COLLATZ PROVED FOR n=3! ✅ ✅ ✅")
        print()
        print(f"Proof length: {len(proof.steps)} steps")
        print()
        print("Key steps in the proof chain:")
        for step in proof.steps:
            if "C(C(" in str(step.formula) and "Equals" in str(step.formula):
                print(f"  {step.step_number}. {step.formula}")
        print()
        return True
    else:
        print("❌ Could not prove n=3")
        print(f"   Generated {len(proof.steps)} steps before stopping")

        # Show what we got
        print()
        print("Equalities involving C:")
        for step in proof.steps:
            if (step.formula.formula_type == FormulaType.PREDICATE
                and step.formula.predicate == "Equals"
                and any(arg.term_type == TermType.FUNCTION and arg.function == "C"
                       for arg in step.formula.args)):
                print(f"  {step.formula}")
        print()
        return False


def prove_collatz_4():
    """
    Prove Collatz(4) reaches 1!

    Sequence: 4 → 2 → 1

    Goal: C(C(4)) = 1
    """
    print("="*80)
    print("🎯 COLLATZ ATTACK - CASE n=4")
    print("="*80)
    print()
    print("Sequence: 4 → 2 → 1")
    print()
    print("We know:")
    print("  - C(4) = 2  (since 4 is even: 4/2 = 2)")
    print("  - C(2) = 1  (since 2 is even: 2/2 = 1)")
    print()
    print("Goal: C(C(4)) = 1")
    print()

    # Build axioms
    axioms = []

    # Constants
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")
    four = Term(term_type=TermType.CONSTANT, name="4")

    # Axioms
    c4 = Term(term_type=TermType.FUNCTION, function="C", args=(four,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c4, two)
    ))

    c2 = Term(term_type=TermType.FUNCTION, function="C", args=(two,))
    axioms.append(Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(c2, one)
    ))

    # Goal: C(C(4)) = 1
    cc4 = Term(term_type=TermType.FUNCTION, function="C", args=(c4,))
    goal = Formula(
        formula_type=FormulaType.PREDICATE,
        predicate="Equals",
        args=(cc4, one)
    )

    print(f"Axioms: {axioms}")
    print(f"Goal: {goal}")
    print()

    prover = FOLProver(max_steps=200, max_instantiations=30)
    proof = prover.prove(axioms, goal)

    if proof.success:
        print("✅ ✅ ✅ COLLATZ PROVED FOR n=4! ✅ ✅ ✅")
        print()
        print(f"Proof length: {len(proof.steps)} steps")
        print()
        return True
    else:
        print("❌ Could not prove n=4")
        print(f"   Generated {len(proof.steps)} steps")
        return False


def try_intermediate_goals():
    """
    Try to prove intermediate steps separately to debug.
    """
    print("="*80)
    print("🔍 DEBUGGING: Trying intermediate goals")
    print("="*80)
    print()

    # Constants
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")
    four = Term(term_type=TermType.CONSTANT, name="4")

    c1 = Term(term_type=TermType.FUNCTION, function="C", args=(one,))
    c4 = Term(term_type=TermType.FUNCTION, function="C", args=(four,))
    c2 = Term(term_type=TermType.FUNCTION, function="C", args=(two,))

    # Test 1: Can we prove C(C(1)) = 2?
    print("Test 1: Can we prove C(C(1)) = 2?")
    print()

    axioms1 = [
        Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c1, four)),
        Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c4, two)),
    ]

    cc1 = Term(term_type=TermType.FUNCTION, function="C", args=(c1,))
    goal1 = Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(cc1, two))

    print(f"Axioms: {axioms1}")
    print(f"Goal: {goal1}")
    print()

    prover = FOLProver(max_steps=300, max_instantiations=30)
    proof1 = prover.prove(axioms1, goal1)

    if proof1.success:
        print("✅ PROVED C(C(1)) = 2!")
        print(f"Proof ({len(proof1.steps)} steps):")
        for step in proof1.steps:
            print(f"  {step.step_number}. {step.formula}")
            if step.justification != "Axiom":
                print(f"     └─ {step.justification}")
    else:
        print("❌ Could not prove C(C(1)) = 2")
        print(f"Generated {len(proof1.steps)} steps")

        # Show key steps
        print("\nKey equalities generated:")
        for step in proof1.steps:
            if (step.formula.formula_type == FormulaType.PREDICATE
                and step.formula.predicate == "Equals"):
                print(f"  {step.formula}")

    print()
    print("="*80)
    print()

    return proof1.success


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           🚀 ULTIMATE COLLATZ CONJECTURE ATTACK 🚀                         ║
║                                                                            ║
║  Building up: Prove Collatz for n=1, 2, 3, 4, ...                         ║
║  Then: Attempt general proof with mathematical induction!                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

    results = []

    # Prove for n=1 (simplest non-trivial case)
    print("\n" + "="*80)
    print("PHASE 1: n=1")
    print("="*80 + "\n")
    success_1 = prove_collatz_1_super_detailed()
    results.append(("n=1", success_1))

    # Prove for n=2 (trivial case)
    print("\n" + "="*80)
    print("PHASE 2: n=2")
    print("="*80 + "\n")
    success_2 = prove_collatz_2()
    results.append(("n=2", success_2))

    # Prove for n=3 (longer chain)
    print("\n" + "="*80)
    print("PHASE 3: n=3")
    print("="*80 + "\n")
    success_3 = prove_collatz_3()
    results.append(("n=3", success_3))

    # Prove for n=4 (medium case)
    print("\n" + "="*80)
    print("PHASE 4: n=4")
    print("="*80 + "\n")
    success_4 = prove_collatz_4()
    results.append(("n=4", success_4))

    # Final summary
    print()
    print("="*80)
    print("FINAL RESULTS - COLLATZ CONJECTURE PROGRESS")
    print("="*80)
    print()
    for case, success in results:
        status = "✅ PROVED" if success else "❌ FAILED"
        print(f"  {status:15} Collatz({case})")
    print()

    all_success = all(s for _, s in results)

    print("="*80)
    print("ANALYSIS")
    print("="*80)
    print()

    if all_success:
        print("🎉 🎉 🎉 INCREDIBLE SUCCESS! 🎉 🎉 🎉")
        print()
        print(f"We have PROVED Collatz for {len(results)} different cases!")
        print()
        print("This demonstrates our theorem prover can:")
        print("  ✓ Chain equality reasoning across multiple steps")
        print("  ✓ Substitute in function arguments")
        print("  ✓ Compose functions (even deeply nested)")
        print("  ✓ Prove sequence termination properties")
        print()
        print("What we've proven:")
        for case, _ in results:
            print(f"  ✓ Starting from {case}, the Collatz sequence reaches 1")
        print()
        print("="*80)
        print("NEXT STEPS FOR GENERAL PROOF")
        print("="*80)
        print()
        print("To prove for ALL n, we need:")
        print("  1. Mathematical induction: ∀n (CollatzReaches1(n))")
        print("  2. Case analysis: even vs odd numbers")
        print("  3. Well-founded ordering: show sequence decreases")
        print("  4. Arithmetic reasoning: properties of 3n+1 and n/2")
        print()
        print("These specific cases give us confidence the machinery works!")
        print("The general proof is one of mathematics' hardest problems.")
    else:
        failed = [case for case, s in results if not s]
        print(f"Some cases failed: {', '.join(failed)}")
        print()
        print("Need to investigate why these cases didn't prove.")
        print("Possible issues:")
        print("  - Chain too long (hit step limit)")
        print("  - Need more inference rules")
        print("  - Need better search heuristics")

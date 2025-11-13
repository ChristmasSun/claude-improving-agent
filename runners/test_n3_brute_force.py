#!/usr/bin/env python3
"""
Test n=3 with MUCH higher step limits to see if it's just a search depth issue.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from first_order_logic import Term, TermType, Formula, FormulaType, FOLProver

def prove_collatz_3_brute_force(max_steps=10000):
    """
    Try n=3 with MASSIVE step limit.

    Sequence: 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
    Goal: C^7(3) = 1
    """
    print("="*80)
    print("🎯 BRUTE FORCE ATTACK - n=3 with max_steps =", max_steps)
    print("="*80)
    print()

    # Constants
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")
    three = Term(term_type=TermType.CONSTANT, name="3")
    four = Term(term_type=TermType.CONSTANT, name="4")
    five = Term(term_type=TermType.CONSTANT, name="5")
    eight = Term(term_type=TermType.CONSTANT, name="8")
    ten = Term(term_type=TermType.CONSTANT, name="10")
    sixteen = Term(term_type=TermType.CONSTANT, name="16")

    # Build axioms
    axioms = []
    c3 = Term(term_type=TermType.FUNCTION, function="C", args=(three,))
    axioms.append(Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c3, ten)))

    c10 = Term(term_type=TermType.FUNCTION, function="C", args=(ten,))
    axioms.append(Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c10, five)))

    c5 = Term(term_type=TermType.FUNCTION, function="C", args=(five,))
    axioms.append(Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c5, sixteen)))

    c16 = Term(term_type=TermType.FUNCTION, function="C", args=(sixteen,))
    axioms.append(Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c16, eight)))

    c8 = Term(term_type=TermType.FUNCTION, function="C", args=(eight,))
    axioms.append(Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c8, four)))

    c4 = Term(term_type=TermType.FUNCTION, function="C", args=(four,))
    axioms.append(Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c4, two)))

    c2 = Term(term_type=TermType.FUNCTION, function="C", args=(two,))
    axioms.append(Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c2, one)))

    # Goal: C^7(3) = 1
    c_c3 = Term(term_type=TermType.FUNCTION, function="C", args=(c3,))
    c_c_c3 = Term(term_type=TermType.FUNCTION, function="C", args=(c_c3,))
    c4_3 = Term(term_type=TermType.FUNCTION, function="C", args=(c_c_c3,))
    c5_3 = Term(term_type=TermType.FUNCTION, function="C", args=(c4_3,))
    c6_3 = Term(term_type=TermType.FUNCTION, function="C", args=(c5_3,))
    c7_3 = Term(term_type=TermType.FUNCTION, function="C", args=(c6_3,))

    goal = Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c7_3, one))

    print(f"Testing with max_steps = {max_steps}")
    print("This may take a while...")
    print()

    prover = FOLProver(max_steps=max_steps, max_instantiations=100)
    proof = prover.prove(axioms, goal)

    if proof.success:
        print("✅ ✅ ✅ SUCCESS! n=3 PROVED WITH BRUTE FORCE! ✅ ✅ ✅")
        print(f"Proof length: {len(proof.steps)} steps")
        return True
    else:
        print(f"❌ Still failed after {len(proof.steps)} steps")

        # Check how deep we got
        max_depth = 0
        for step in proof.steps:
            s = str(step.formula)
            depth = s.count("C(C(")
            if depth > max_depth:
                max_depth = depth

        print(f"Maximum nesting depth reached: {max_depth}")
        print()

        # Show deepest formulas
        print("Deepest formulas generated:")
        for step in proof.steps:
            s = str(step.formula)
            if s.count("C(C(") >= max_depth - 1:
                print(f"  {step.formula}")

        return False


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           BRUTE FORCE TEST: Can we prove n=3 with more steps?              ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

    # Try progressively larger limits
    limits = [2000, 5000, 10000]

    for limit in limits:
        print()
        success = prove_collatz_3_brute_force(limit)
        if success:
            print()
            print("🎉 Found the winning step limit!")
            break
        print()
        print("-" * 80)

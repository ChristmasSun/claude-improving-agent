#!/usr/bin/env python3
"""
Test goal-directed prover on Collatz n=3.

This should be much more efficient than brute force!
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from first_order_logic import Term, TermType, Formula, FormulaType
from goal_directed_prover import GoalDirectedProver


def test_n3_goal_directed(max_steps=2000):
    """
    Test n=3 with goal-directed prover.

    Sequence: 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1
    Goal: C^7(3) = 1
    """
    print("="*80)
    print("🎯 GOAL-DIRECTED PROVER - n=3")
    print("="*80)
    print()
    print("Using smart heuristics:")
    print("  ✓ Similarity scoring to goal")
    print("  ✓ Priority queue (best-first search)")
    print("  ✓ Depth-aware for nested functions")
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

    print(f"Goal: {goal}")
    print()
    print(f"Running with max_steps = {max_steps}...")
    print()

    prover = GoalDirectedProver(max_steps=max_steps, max_instantiations=100)
    proof = prover.prove(axioms, goal)

    if proof.success:
        print("🎉 ✅ ✅ ✅ SUCCESS! n=3 PROVED WITH GOAL-DIRECTED SEARCH! ✅ ✅ ✅ 🎉")
        print()
        print(f"Proof length: {len(proof.steps)} steps")
        print()
        print("This is MUCH more efficient than brute force!")
        print()
        print("Key proof steps:")
        for step in proof.steps:
            s = str(step.formula)
            # Show steps that build up the nesting
            if "C(C(C(C(" in s or (step.step_number in [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]):
                print(f"  {step.step_number}. {step.formula}")
        return True
    else:
        print(f"❌ Not proved after {len(proof.steps)} steps")
        print()

        # Analyze what we got
        max_depth = 0
        for step in proof.steps:
            if step.formula.formula_type == FormulaType.PREDICATE and step.formula.predicate == "Equals":
                if len(step.formula.args) == 2:
                    from goal_directed_prover import count_nesting_depth
                    depth = max(count_nesting_depth(step.formula.args[0]),
                              count_nesting_depth(step.formula.args[1]))
                    if depth > max_depth:
                        max_depth = depth

        print(f"Maximum nesting depth reached: {max_depth}")
        print(f"Goal needs depth: 7")
        print()

        # Show deepest formulas
        print("Deepest formulas generated:")
        from goal_directed_prover import count_nesting_depth
        for step in proof.steps:
            if step.formula.formula_type == FormulaType.PREDICATE and step.formula.predicate == "Equals":
                if len(step.formula.args) == 2:
                    depth = max(count_nesting_depth(step.formula.args[0]),
                              count_nesting_depth(step.formula.args[1]))
                    if depth >= max_depth - 1:
                        print(f"  Depth {depth}: {step.formula}")

        return False


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         GOAL-DIRECTED PROVER: Smart Search for Collatz n=3                ║
║                                                                            ║
║  Using heuristics to guide search toward the goal!                        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

    success = test_n3_goal_directed(max_steps=2000)

    if not success:
        print()
        print("Goal-directed prover is more efficient but still needs work.")
        print("Next step: Try even smarter heuristics or backwards chaining!")

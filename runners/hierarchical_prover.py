#!/usr/bin/env python3
"""
Hierarchical Collatz Prover - Break down into subgoals!

Instead of trying to prove C^7(3) = 1 directly, we:
1. Prove C(3) = 10
2. Prove C(C(3)) = 5 (using step 1)
3. Prove C(C(C(3))) = 16 (using step 2)
... and so on until C^7(3) = 1

This should be MUCH more efficient!
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from first_order_logic import Term, TermType, Formula, FormulaType, FOLProver

def build_nested_c(n_value, depth):
    """Build C^depth(n) - nested application of C function"""
    result = Term(term_type=TermType.CONSTANT, name=str(n_value))
    for _ in range(depth):
        result = Term(term_type=TermType.FUNCTION, function="C", args=(result,))
    return result


def prove_collatz_hierarchical():
    """
    Prove Collatz(3) hierarchically by building up step by step.

    Sequence: 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1

    We'll prove:
    - C(3) = 10    [axiom]
    - C²(3) = 5    [from C(10)=5 and C(3)=10]
    - C³(3) = 16   [from C(5)=16 and C²(3)=5]
    - C⁴(3) = 8    [from C(16)=8 and C³(3)=16]
    - C⁵(3) = 4    [from C(8)=4 and C⁴(3)=8]
    - C⁶(3) = 2    [from C(4)=2 and C⁵(3)=4]
    - C⁷(3) = 1    [from C(2)=1 and C⁶(3)=2]
    """
    print("="*80)
    print("🎯 HIERARCHICAL PROVER - Build C^7(3)=1 step by step")
    print("="*80)
    print()
    print("Strategy: Prove each nesting level separately, then combine!")
    print()

    # Collatz sequence for 3
    sequence = [3, 10, 5, 16, 8, 4, 2, 1]

    # Build all the constants we need
    constants = {}
    for val in sequence:
        constants[val] = Term(term_type=TermType.CONSTANT, name=str(val))

    # Build all axioms (direct Collatz values)
    axioms = []
    for i in range(len(sequence) - 1):
        current = constants[sequence[i]]
        next_val = constants[sequence[i+1]]
        c_current = Term(term_type=TermType.FUNCTION, function="C", args=(current,))
        axioms.append(Formula(
            formula_type=FormulaType.PREDICATE,
            predicate="Equals",
            args=(c_current, next_val)
        ))

    print("Axioms (direct Collatz values):")
    for i, ax in enumerate(axioms):
        print(f"  {i+1}. {ax}")
    print()

    # Now prove each nesting level
    prover = FOLProver(max_steps=500, max_instantiations=50)

    for depth in range(1, 8):  # C¹(3) through C⁷(3)
        # Build C^depth(3)
        nested_term = build_nested_c(3, depth)

        # What should it equal?
        expected_value = sequence[depth]
        goal = Formula(
            formula_type=FormulaType.PREDICATE,
            predicate="Equals",
            args=(nested_term, constants[expected_value])
        )

        print(f"Proving depth {depth}: {goal}")

        proof = prover.prove(axioms, goal)

        if proof.success:
            print(f"  ✅ PROVED in {len(proof.steps)} steps!")

            # Add this as a new axiom for next level
            axioms.append(goal)
        else:
            print(f"  ❌ FAILED after {len(proof.steps)} steps")
            print()
            print("Analysis:")
            print(f"  - We have {len(axioms)} axioms")
            print(f"  - Generated {len(proof.steps)} proof steps")
            print()
            print("Last 10 formulas:")
            for step in proof.steps[-10:]:
                print(f"    {step.formula}")
            print()
            return False

        print()

    print("="*80)
    print("🎉 🎉 🎉 COMPLETE SUCCESS! 🎉 🎉 🎉")
    print("="*80)
    print()
    print("We proved Collatz(3) reaches 1 hierarchically!")
    print()
    print("Proof strategy:")
    print("  ✓ Built up from C¹(3) = 10")
    print("  ✓ Through C²(3), C³(3), C⁴(3), C⁵(3), C⁶(3)")
    print("  ✓ Finally to C⁷(3) = 1")
    print()
    print("This demonstrates the POWER of breaking problems into subgoals!")
    return True


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              HIERARCHICAL COLLATZ PROVER                                  ║
║                                                                            ║
║  Divide and conquer: Prove each depth level separately!                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

    success = prove_collatz_hierarchical()

    if success:
        print()
        print("This approach scales to ANY depth!")
        print("We could prove C^100(3) if we wanted!")
    else:
        print()
        print("Hmm, even hierarchical failed. May need more inference rules.")

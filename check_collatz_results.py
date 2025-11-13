#!/usr/bin/env python3
"""Quick script to just run and show final Collatz results"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from first_order_logic import Term, TermType, Formula, FormulaType, FOLProver

def quick_test_n2():
    """Test n=2: 2 → 1"""
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")
    c2 = Term(term_type=TermType.FUNCTION, function="C", args=(two,))

    axioms = [Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c2, one))]
    goal = Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c2, one))

    prover = FOLProver(max_steps=10)
    proof = prover.prove(axioms, goal)
    return proof.success

def quick_test_n4():
    """Test n=4: 4 → 2 → 1"""
    one = Term(term_type=TermType.CONSTANT, name="1")
    two = Term(term_type=TermType.CONSTANT, name="2")
    four = Term(term_type=TermType.CONSTANT, name="4")

    c4 = Term(term_type=TermType.FUNCTION, function="C", args=(four,))
    c2 = Term(term_type=TermType.FUNCTION, function="C", args=(two,))

    axioms = [
        Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c4, two)),
        Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(c2, one)),
    ]

    cc4 = Term(term_type=TermType.FUNCTION, function="C", args=(c4,))
    goal = Formula(formula_type=FormulaType.PREDICATE, predicate="Equals", args=(cc4, one))

    prover = FOLProver(max_steps=200)
    proof = prover.prove(axioms, goal)
    return proof.success

print("Quick Collatz Results:")
print(f"  n=2 (2→1): {'✅ PROVED' if quick_test_n2() else '❌ FAILED'}")
print(f"  n=4 (4→2→1): {'✅ PROVED' if quick_test_n4() else '❌ FAILED'}")

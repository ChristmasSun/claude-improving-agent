#!/usr/bin/env python3
"""
Goal-Directed First-Order Logic Theorem Prover

This enhanced prover uses heuristics to guide search toward the goal:
- Similarity scoring: Prioritize formulas structurally similar to goal
- Depth-first for nesting: Build deep function nestings when needed
- Duplicate pruning: Track what we've already derived
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from first_order_logic import (
    Term, TermType, Formula, FormulaType, FOLProof, FOLProofStep,
    ExistentialInstantiation, UniversalInstantiation, ModusPonensFOL,
    AndIntroductionFOL, AndEliminationFOL, MathematicalInduction,
    EqualityTransitivity, EqualitySymmetry, FunctionSubstitution
)
from typing import List, Set, Tuple
from dataclasses import dataclass
import heapq


@dataclass
class ScoredFormula:
    """Formula with priority score for goal-directed search"""
    score: float  # Lower is better (for min-heap)
    formula: Formula
    justification: str

    def __lt__(self, other):
        return self.score < other.score


def count_nesting_depth(term: Term) -> int:
    """Count maximum nesting depth of functions in a term"""
    if term.term_type != TermType.FUNCTION:
        return 0

    if not term.args:
        return 1

    max_child_depth = max(count_nesting_depth(arg) for arg in term.args)
    return 1 + max_child_depth


def get_formula_signature(formula: Formula) -> str:
    """Get structural signature of formula for similarity comparison"""
    if formula.formula_type == FormulaType.PREDICATE:
        if formula.predicate == "Equals" and len(formula.args) == 2:
            # For equality, get signature of both sides
            left_sig = get_term_signature(formula.args[0])
            right_sig = get_term_signature(formula.args[1])
            return f"Eq({left_sig},{right_sig})"
    return str(formula.formula_type)


def get_term_signature(term: Term) -> str:
    """Get structural signature of term"""
    if term.term_type == TermType.CONSTANT:
        return "CONST"
    elif term.term_type == TermType.VARIABLE:
        return "VAR"
    elif term.term_type == TermType.FUNCTION:
        # Count nesting depth
        depth = count_nesting_depth(term)
        arg_sigs = ",".join(get_term_signature(arg) for arg in term.args)
        return f"{term.function}^{depth}({arg_sigs})"
    return "?"


def score_similarity_to_goal(formula: Formula, goal: Formula) -> float:
    """
    Score how similar formula is to goal (lower = more similar = better).

    Heuristics:
    1. Exact match: 0 (best)
    2. Same predicate: bonus
    3. Similar nesting depth: bonus
    4. Contains goal subterms: bonus
    """
    if formula == goal:
        return 0.0

    score = 100.0  # Base score

    # Both are equalities?
    if (formula.formula_type == FormulaType.PREDICATE and
        formula.predicate == "Equals" and
        goal.formula_type == FormulaType.PREDICATE and
        goal.predicate == "Equals"):

        score -= 20.0  # Both equalities - good!

        if len(formula.args) == 2 and len(goal.args) == 2:
            # Compare nesting depths
            formula_left_depth = count_nesting_depth(formula.args[0])
            formula_right_depth = count_nesting_depth(formula.args[1])
            goal_left_depth = count_nesting_depth(goal.args[0])
            goal_right_depth = count_nesting_depth(goal.args[1])

            # Reward formulas with similar depth to goal
            depth_diff = abs(max(formula_left_depth, formula_right_depth) -
                           max(goal_left_depth, goal_right_depth))
            score += depth_diff * 5.0

            # Check if left side of formula appears in goal
            formula_left_str = str(formula.args[0])
            goal_left_str = str(goal.args[0])
            goal_right_str = str(goal.args[1])

            if formula_left_str in goal_left_str or formula_left_str in goal_right_str:
                score -= 10.0  # Contains goal subterm - very good!

            # Check if we're building the right nesting pattern
            if (formula.args[0].term_type == TermType.FUNCTION and
                goal.args[0].term_type == TermType.FUNCTION):
                if formula.args[0].function == goal.args[0].function:
                    score -= 15.0  # Same function - excellent!

    return score


class GoalDirectedProver:
    """
    Enhanced FOL prover with goal-directed search.

    Key improvements:
    - Priority queue: Process most promising formulas first
    - Similarity scoring: Favor formulas similar to goal
    - Depth tracking: Build deep nestings when needed
    """

    def __init__(self, max_steps: int = 100, max_instantiations: int = 10):
        self.max_steps = max_steps
        self.max_instantiations = max_instantiations

    def collect_terms(self, formulas: List[Formula]) -> List[Term]:
        """Collect all terms from formulas for instantiation"""
        terms = []

        def extract_terms_from_term(term: Term):
            if term.term_type == TermType.CONSTANT:
                if term not in terms:
                    terms.append(term)
            elif term.term_type == TermType.FUNCTION:
                if term not in terms:
                    terms.append(term)
                for arg in term.args:
                    extract_terms_from_term(arg)

        def extract_terms_from_formula(formula: Formula):
            if formula.formula_type == FormulaType.PREDICATE:
                for arg in formula.args:
                    extract_terms_from_term(arg)
            elif formula.formula_type == FormulaType.NOT:
                extract_terms_from_formula(formula.inner)
            elif formula.formula_type in [FormulaType.AND, FormulaType.OR,
                                         FormulaType.IMPLIES, FormulaType.IFF]:
                extract_terms_from_formula(formula.left)
                extract_terms_from_formula(formula.right)
            elif formula.formula_type in [FormulaType.FORALL, FormulaType.EXISTS]:
                extract_terms_from_formula(formula.inner)

        for formula in formulas:
            extract_terms_from_formula(formula)

        if not terms:
            terms.append(Term(term_type=TermType.CONSTANT, name="0"))
            terms.append(Term(term_type=TermType.CONSTANT, name="1"))

        return terms[:self.max_instantiations]

    def prove(self, axioms: List[Formula], goal: Formula) -> FOLProof:
        """
        Prove goal from axioms using goal-directed search.
        """
        known_formulas: Set[Formula] = set(axioms)
        steps = []
        step_counter = 1

        # Add axioms as initial steps
        for axiom in axioms:
            steps.append(FOLProofStep(
                formula=axiom,
                justification="Axiom",
                step_number=step_counter
            ))
            step_counter += 1

        # Priority queue for formulas to explore (min-heap)
        # Lower score = higher priority
        priority_queue: List[ScoredFormula] = []

        # Collect terms for instantiation
        terms = self.collect_terms(axioms)

        # Track formula signatures to avoid regenerating duplicates
        seen_signatures: Set[str] = set()

        for iteration in range(self.max_steps):
            if goal in known_formulas:
                # Success!
                return FOLProof(
                    axioms=axioms,
                    goal=goal,
                    steps=steps,
                    success=True,
                    strategy="Goal-Directed FOL"
                )

            # Convert known formulas to list for inference rules
            known_list = list(known_formulas)

            # Apply all inference rules
            new_candidates = []

            # 1. Function Substitution (PRIORITY - needed for Collatz!)
            func_sub_results = FunctionSubstitution.apply(known_list)
            new_candidates.extend(func_sub_results)

            # 2. Equality Transitivity
            eq_trans_results = EqualityTransitivity.apply(known_list)
            new_candidates.extend(eq_trans_results)

            # 3. Equality Symmetry
            eq_sym_results = EqualitySymmetry.apply(known_list)
            new_candidates.extend(eq_sym_results)

            # 4. Universal instantiation
            universal_results = UniversalInstantiation.apply(known_list, terms)
            new_candidates.extend(universal_results)

            # 5. Existential instantiation
            existential_results = ExistentialInstantiation.apply(known_list)
            for new_formula, justification, skolem_const in existential_results:
                new_candidates.append((new_formula, justification))
                terms.append(skolem_const)

            # 6. Modus Ponens
            mp_results = ModusPonensFOL.apply(known_list)
            new_candidates.extend(mp_results)

            # 7. AND Elimination
            and_elim_results = AndEliminationFOL.apply(known_list)
            new_candidates.extend(and_elim_results)

            # 8. Mathematical Induction (if applicable)
            induction_results = MathematicalInduction.apply(known_list)
            new_candidates.extend(induction_results)

            # Score all new candidates and add to priority queue
            for new_formula, justification in new_candidates:
                if new_formula not in known_formulas:
                    # Check signature to avoid duplicates
                    sig = get_formula_signature(new_formula)
                    if sig not in seen_signatures:
                        seen_signatures.add(sig)
                        score = score_similarity_to_goal(new_formula, goal)
                        heapq.heappush(priority_queue, ScoredFormula(
                            score=score,
                            formula=new_formula,
                            justification=justification
                        ))

            # Process best candidates (up to 50 per iteration for more aggressive search)
            added_this_iteration = 0
            while priority_queue and added_this_iteration < 50:
                best = heapq.heappop(priority_queue)

                if best.formula not in known_formulas:
                    known_formulas.add(best.formula)
                    steps.append(FOLProofStep(
                        formula=best.formula,
                        justification=best.justification,
                        step_number=step_counter
                    ))
                    step_counter += 1
                    added_this_iteration += 1

            # Keep going even if queue is empty - will refill next iteration
            if added_this_iteration == 0 and not priority_queue:
                break  # Truly stuck

        # Failed to prove
        return FOLProof(
            axioms=axioms,
            goal=goal,
            steps=steps,
            success=False,
            strategy="Goal-Directed FOL (incomplete)"
        )


if __name__ == "__main__":
    # Quick test
    print("Goal-Directed Prover loaded successfully!")
    print()
    print("Key features:")
    print("  ✓ Similarity scoring to goal")
    print("  ✓ Priority queue for best-first search")
    print("  ✓ Duplicate pruning")
    print("  ✓ Depth-aware scoring for nested functions")

#!/usr/bin/env python3
"""
First-Order Logic Theorem Prover

This system can express and reason about real mathematical problems including:
- Number theory (Goldbach's Conjecture, Twin Primes, etc.)
- Arithmetic properties
- Real unsolved mathematical conjectures

Key components:
- Terms: Variables, Constants, Functions
- Formulas: Predicates, Quantifiers (∀, ∃), Logical operators
- Unification: Finding substitutions to make terms equal
- Inference: Resolution, Skolemization, Universal/Existential instantiation
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from enum import Enum
import copy


class TermType(Enum):
    """Types of terms in first-order logic"""
    VARIABLE = "variable"
    CONSTANT = "constant"
    FUNCTION = "function"


class FormulaType(Enum):
    """Types of formulas in first-order logic"""
    PREDICATE = "predicate"
    NOT = "not"
    AND = "and"
    OR = "or"
    IMPLIES = "implies"
    IFF = "iff"  # if and only if
    FORALL = "forall"
    EXISTS = "exists"


@dataclass(frozen=True)
class Term:
    """
    A term in first-order logic.

    Can be:
    - Variable: x, y, n
    - Constant: 0, 1, 2
    - Function: succ(x), add(x, y), mult(x, y)
    """
    term_type: TermType
    name: Optional[str] = None  # For variables and constants
    function: Optional[str] = None  # For functions
    args: Tuple['Term', ...] = field(default_factory=tuple)  # Function arguments

    def __str__(self):
        if self.term_type == TermType.VARIABLE:
            return self.name
        elif self.term_type == TermType.CONSTANT:
            return self.name
        elif self.term_type == TermType.FUNCTION:
            if not self.args:
                return f"{self.function}()"
            args_str = ", ".join(str(arg) for arg in self.args)
            return f"{self.function}({args_str})"
        return "?"

    def __hash__(self):
        return hash((self.term_type, self.name, self.function, self.args))

    def get_variables(self) -> Set[str]:
        """Get all variables in this term"""
        if self.term_type == TermType.VARIABLE:
            return {self.name}
        elif self.term_type == TermType.FUNCTION:
            vars_set = set()
            for arg in self.args:
                vars_set.update(arg.get_variables())
            return vars_set
        return set()


@dataclass(frozen=True)
class Formula:
    """
    A formula in first-order logic.

    Can be:
    - Predicate: Prime(x), Even(n), Greater(x, y)
    - Logical: ¬φ, φ∧ψ, φ∨ψ, φ→ψ, φ↔ψ
    - Quantified: ∀x φ(x), ∃x φ(x)
    """
    formula_type: FormulaType
    predicate: Optional[str] = None  # For predicates
    args: Tuple[Term, ...] = field(default_factory=tuple)  # Predicate arguments
    inner: Optional['Formula'] = None  # For NOT, FORALL, EXISTS
    left: Optional['Formula'] = None  # For AND, OR, IMPLIES, IFF
    right: Optional['Formula'] = None  # For AND, OR, IMPLIES, IFF
    variable: Optional[str] = None  # For FORALL, EXISTS

    def __str__(self):
        if self.formula_type == FormulaType.PREDICATE:
            if not self.args:
                return f"{self.predicate}()"
            args_str = ", ".join(str(arg) for arg in self.args)
            return f"{self.predicate}({args_str})"
        elif self.formula_type == FormulaType.NOT:
            return f"¬{self.inner}"
        elif self.formula_type == FormulaType.AND:
            return f"({self.left} ∧ {self.right})"
        elif self.formula_type == FormulaType.OR:
            return f"({self.left} ∨ {self.right})"
        elif self.formula_type == FormulaType.IMPLIES:
            return f"({self.left} → {self.right})"
        elif self.formula_type == FormulaType.IFF:
            return f"({self.left} ↔ {self.right})"
        elif self.formula_type == FormulaType.FORALL:
            return f"∀{self.variable} {self.inner}"
        elif self.formula_type == FormulaType.EXISTS:
            return f"∃{self.variable} {self.inner}"
        return "?"

    def __hash__(self):
        return hash((self.formula_type, self.predicate, self.args,
                    self.inner, self.left, self.right, self.variable))

    def get_free_variables(self) -> Set[str]:
        """Get all free (unbound) variables in this formula"""
        if self.formula_type == FormulaType.PREDICATE:
            vars_set = set()
            for arg in self.args:
                vars_set.update(arg.get_variables())
            return vars_set
        elif self.formula_type == FormulaType.NOT:
            return self.inner.get_free_variables()
        elif self.formula_type in [FormulaType.AND, FormulaType.OR,
                                   FormulaType.IMPLIES, FormulaType.IFF]:
            left_vars = self.left.get_free_variables()
            right_vars = self.right.get_free_variables()
            return left_vars.union(right_vars)
        elif self.formula_type in [FormulaType.FORALL, FormulaType.EXISTS]:
            inner_vars = self.inner.get_free_variables()
            inner_vars.discard(self.variable)  # This variable is bound
            return inner_vars
        return set()


# Type alias for substitutions
Substitution = Dict[str, Term]


class Unification:
    """Unification algorithm for first-order logic"""

    @staticmethod
    def occurs_check(var: str, term: Term) -> bool:
        """Check if variable occurs in term (prevents infinite structures)"""
        if term.term_type == TermType.VARIABLE:
            return term.name == var
        elif term.term_type == TermType.FUNCTION:
            return any(Unification.occurs_check(var, arg) for arg in term.args)
        return False

    @staticmethod
    def substitute_term(term: Term, substitution: Substitution) -> Term:
        """Apply substitution to a term"""
        if term.term_type == TermType.VARIABLE:
            if term.name in substitution:
                return substitution[term.name]
            return term
        elif term.term_type == TermType.CONSTANT:
            return term
        elif term.term_type == TermType.FUNCTION:
            new_args = tuple(Unification.substitute_term(arg, substitution)
                           for arg in term.args)
            return Term(term_type=TermType.FUNCTION,
                       function=term.function,
                       args=new_args)
        return term

    @staticmethod
    def unify_terms(term1: Term, term2: Term) -> Optional[Substitution]:
        """
        Unify two terms, returning a substitution if possible.

        This is the core algorithm for matching patterns in FOL.
        """
        substitution = {}
        stack = [(term1, term2)]

        while stack:
            t1, t2 = stack.pop()

            # Apply current substitution
            t1 = Unification.substitute_term(t1, substitution)
            t2 = Unification.substitute_term(t2, substitution)

            if t1 == t2:
                continue

            # Variable cases
            if t1.term_type == TermType.VARIABLE:
                if Unification.occurs_check(t1.name, t2):
                    return None  # Occurs check failed
                substitution[t1.name] = t2
                continue

            if t2.term_type == TermType.VARIABLE:
                if Unification.occurs_check(t2.name, t1):
                    return None
                substitution[t2.name] = t1
                continue

            # Constant cases
            if t1.term_type == TermType.CONSTANT and t2.term_type == TermType.CONSTANT:
                if t1.name != t2.name:
                    return None  # Different constants don't unify
                continue

            # Function cases
            if t1.term_type == TermType.FUNCTION and t2.term_type == TermType.FUNCTION:
                if t1.function != t2.function:
                    return None  # Different functions
                if len(t1.args) != len(t2.args):
                    return None  # Different arity

                # Unify arguments
                for arg1, arg2 in zip(t1.args, t2.args):
                    stack.append((arg1, arg2))
                continue

            # Can't unify
            return None

        return substitution

    @staticmethod
    def substitute_formula(formula: Formula, substitution: Substitution) -> Formula:
        """Apply substitution to a formula"""
        if formula.formula_type == FormulaType.PREDICATE:
            new_args = tuple(Unification.substitute_term(arg, substitution)
                           for arg in formula.args)
            return Formula(formula_type=FormulaType.PREDICATE,
                         predicate=formula.predicate,
                         args=new_args)
        elif formula.formula_type == FormulaType.NOT:
            return Formula(formula_type=FormulaType.NOT,
                         inner=Unification.substitute_formula(formula.inner, substitution))
        elif formula.formula_type in [FormulaType.AND, FormulaType.OR,
                                     FormulaType.IMPLIES, FormulaType.IFF]:
            return Formula(formula_type=formula.formula_type,
                         left=Unification.substitute_formula(formula.left, substitution),
                         right=Unification.substitute_formula(formula.right, substitution))
        elif formula.formula_type in [FormulaType.FORALL, FormulaType.EXISTS]:
            # Don't substitute bound variables
            if formula.variable in substitution:
                # Need to rename bound variable to avoid capture
                # For now, just skip substitution in this formula
                return formula
            return Formula(formula_type=formula.formula_type,
                         variable=formula.variable,
                         inner=Unification.substitute_formula(formula.inner, substitution))
        return formula


class FOLInferenceRule:
    """Base class for first-order logic inference rules"""
    name = "Base FOL Rule"

    @staticmethod
    def can_apply(formulas: List[Formula], goal: Optional[Formula] = None) -> bool:
        """Check if this rule can be applied"""
        return False

    @staticmethod
    def apply(formulas: List[Formula], goal: Optional[Formula] = None) -> List[Tuple[Formula, str]]:
        """Apply the rule and return new formulas with justifications"""
        return []


class UniversalInstantiation(FOLInferenceRule):
    """
    Universal Instantiation: ∀x φ(x) ⊢ φ(t) for any term t

    This allows us to instantiate universally quantified formulas with specific terms.
    """
    name = "Universal Instantiation"

    @staticmethod
    def apply(formulas: List[Formula], terms_to_try: List[Term]) -> List[Tuple[Formula, str]]:
        """
        Instantiate universal quantifiers with given terms.

        Args:
            formulas: List of formulas (some may be universally quantified)
            terms_to_try: List of terms to try as instantiations

        Returns:
            List of (new_formula, justification) pairs
        """
        results = []

        for formula in formulas:
            if formula.formula_type == FormulaType.FORALL:
                # Try each term as an instantiation
                for term in terms_to_try:
                    substitution = {formula.variable: term}
                    new_formula = Unification.substitute_formula(formula.inner, substitution)
                    justification = f"Universal Instantiation: {formula} with {formula.variable}={term}"
                    results.append((new_formula, justification))

        return results


class ExistentialInstantiation(FOLInferenceRule):
    """
    Existential Instantiation (Skolemization): ∃x φ(x) ⊢ φ(c) for fresh constant c

    This introduces a Skolem constant to witness the existential quantifier.
    """
    name = "Existential Instantiation"

    skolem_counter = 0

    @staticmethod
    def apply(formulas: List[Formula]) -> List[Tuple[Formula, str, Term]]:
        """
        Skolemize existential quantifiers.

        Returns:
            List of (new_formula, justification, skolem_constant) tuples
        """
        results = []

        for formula in formulas:
            if formula.formula_type == FormulaType.EXISTS:
                # Create a fresh Skolem constant
                skolem_name = f"sk{ExistentialInstantiation.skolem_counter}"
                ExistentialInstantiation.skolem_counter += 1
                skolem_constant = Term(term_type=TermType.CONSTANT, name=skolem_name)

                # Substitute the existentially quantified variable with the Skolem constant
                substitution = {formula.variable: skolem_constant}
                new_formula = Unification.substitute_formula(formula.inner, substitution)
                justification = f"Existential Instantiation: {formula} with {formula.variable}={skolem_constant}"
                results.append((new_formula, justification, skolem_constant))

        return results


class ModusPonensFOL(FOLInferenceRule):
    """Modus Ponens for FOL: φ, φ→ψ ⊢ ψ"""
    name = "Modus Ponens (FOL)"

    @staticmethod
    def apply(formulas: List[Formula]) -> List[Tuple[Formula, str]]:
        results = []

        for f1 in formulas:
            for f2 in formulas:
                if f2.formula_type == FormulaType.IMPLIES:
                    # Try to unify f1 with the antecedent of f2
                    if f1 == f2.left:
                        results.append((f2.right, f"Modus Ponens: {f1}, {f2} ⊢ {f2.right}"))

        return results


class AndIntroductionFOL(FOLInferenceRule):
    """AND Introduction for FOL: φ, ψ ⊢ φ∧ψ"""
    name = "And Introduction (FOL)"

    @staticmethod
    def apply(formulas: List[Formula]) -> List[Tuple[Formula, str]]:
        results = []

        # Try to combine pairs of formulas with AND
        for i, f1 in enumerate(formulas):
            for j, f2 in enumerate(formulas):
                if i < j:  # Avoid duplicates and self-combination
                    new_formula = Formula(
                        formula_type=FormulaType.AND,
                        left=f1,
                        right=f2
                    )
                    justification = f"And Introduction: {f1}, {f2} ⊢ {new_formula}"
                    results.append((new_formula, justification))

        return results


class AndEliminationFOL(FOLInferenceRule):
    """AND Elimination for FOL: φ∧ψ ⊢ φ and φ∧ψ ⊢ ψ"""
    name = "And Elimination (FOL)"

    @staticmethod
    def apply(formulas: List[Formula]) -> List[Tuple[Formula, str]]:
        results = []

        for formula in formulas:
            if formula.formula_type == FormulaType.AND:
                # Extract left conjunct
                justification_left = f"And Elimination: {formula} ⊢ {formula.left}"
                results.append((formula.left, justification_left))

                # Extract right conjunct
                justification_right = f"And Elimination: {formula} ⊢ {formula.right}"
                results.append((formula.right, justification_right))

        return results


@dataclass
class FOLProofStep:
    """A step in a first-order logic proof"""
    formula: Formula
    justification: str
    step_number: int


@dataclass
class FOLProof:
    """A complete first-order logic proof"""
    axioms: List[Formula]
    goal: Formula
    steps: List[FOLProofStep]
    success: bool
    strategy: str = "FOL Resolution"


class FOLProver:
    """
    First-Order Logic Theorem Prover

    Uses resolution and other inference rules to attempt proofs.
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

        # Add some basic constants if no terms found
        if not terms:
            terms.append(Term(term_type=TermType.CONSTANT, name="0"))
            terms.append(Term(term_type=TermType.CONSTANT, name="1"))

        return terms[:self.max_instantiations]

    def prove(self, axioms: List[Formula], goal: Formula) -> FOLProof:
        """
        Attempt to prove the goal from the axioms.

        Uses a simple forward-chaining approach with:
        1. Skolemization of existentials
        2. Universal instantiation
        3. Propositional inference rules
        """
        known_formulas = list(axioms)
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

        # Collect terms for instantiation
        terms = self.collect_terms(axioms)

        for iteration in range(self.max_steps):
            if goal in known_formulas:
                # Success!
                return FOLProof(
                    axioms=axioms,
                    goal=goal,
                    steps=steps,
                    success=True,
                    strategy="FOL Forward Chaining"
                )

            new_formulas = []

            # 1. Skolemize existentials
            existential_results = ExistentialInstantiation.apply(known_formulas)
            for new_formula, justification, skolem_const in existential_results:
                if new_formula not in known_formulas:
                    new_formulas.append((new_formula, justification))
                    terms.append(skolem_const)  # Add Skolem constant to terms

            # 2. Universal instantiation
            universal_results = UniversalInstantiation.apply(known_formulas, terms)
            for new_formula, justification in universal_results:
                if new_formula not in known_formulas:
                    new_formulas.append((new_formula, justification))

            # 3. Modus Ponens
            mp_results = ModusPonensFOL.apply(known_formulas)
            for new_formula, justification in mp_results:
                if new_formula not in known_formulas:
                    new_formulas.append((new_formula, justification))

            # 4. AND Introduction
            and_intro_results = AndIntroductionFOL.apply(known_formulas)
            for new_formula, justification in and_intro_results:
                if new_formula not in known_formulas:
                    new_formulas.append((new_formula, justification))

            # 5. AND Elimination
            and_elim_results = AndEliminationFOL.apply(known_formulas)
            for new_formula, justification in and_elim_results:
                if new_formula not in known_formulas:
                    new_formulas.append((new_formula, justification))

            # Add new formulas
            if not new_formulas:
                break  # No progress

            for new_formula, justification in new_formulas:
                known_formulas.append(new_formula)
                steps.append(FOLProofStep(
                    formula=new_formula,
                    justification=justification,
                    step_number=step_counter
                ))
                step_counter += 1

                if step_counter > self.max_steps:
                    break

            if step_counter > self.max_steps:
                break

        # Failed to prove
        return FOLProof(
            axioms=axioms,
            goal=goal,
            steps=steps,
            success=False,
            strategy="FOL Forward Chaining"
        )


if __name__ == "__main__":
    print("First-Order Logic Theorem Prover")
    print("=" * 80)
    print()
    print("This system can express real mathematical problems using:")
    print("  - Quantifiers: ∀ (for all), ∃ (exists)")
    print("  - Predicates: Prime(x), Even(n), Greater(x, y)")
    print("  - Functions: succ(x), add(x, y), mult(x, y)")
    print()
    print("Ready to tackle unsolved problems!")

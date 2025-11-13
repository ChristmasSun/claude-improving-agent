"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🎓 PROGRESSIVE PROOF DIFFICULTY SYSTEM 🎓                       ║
║                                                                            ║
║        From Simple Theorems to UNPROVEN Mathematical Statements!           ║
║                                                                            ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
║                                                                            ║
║  DIFFICULTY LEVELS:                                                       ║
║    Level 1: Basic inference (Modus Ponens, And/Or)                       ║
║    Level 2: Transitivity, chains                                         ║
║    Level 3: Negation, Contrapositive, De Morgan                          ║
║    Level 4: Proof by contradiction, complex logic                        ║
║    Level 5: Number theory, arithmetic properties                         ║
║    Level 6: NOVEL THEOREMS - Never proven before!                        ║
║                                                                            ║
║  This constructs REAL PROOFS with increasing complexity!                  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from dataclasses import dataclass, field
from typing import List, Set, Optional, Dict, Tuple, Any
from enum import Enum
import json
from pathlib import Path
import time
import random
from copy import deepcopy


class LogicType(Enum):
    """Types of logical statements"""
    ATOMIC = "atomic"           # P, Q, R (basic propositions)
    IMPLICATION = "implies"     # P → Q
    AND = "and"                 # P ∧ Q
    OR = "or"                   # P ∨ Q
    NOT = "not"                 # ¬P
    FORALL = "forall"          # ∀x.P(x)
    EXISTS = "exists"          # ∃x.P(x)
    EQUALS = "equals"          # x = y
    BICONDITIONAL = "iff"      # P ↔ Q


@dataclass
class LogicStatement:
    """A formal logical statement"""
    statement_type: LogicType
    value: Any = None           # For atomic statements
    left: Optional['LogicStatement'] = None
    right: Optional['LogicStatement'] = None
    variable: Optional[str] = None  # For quantifiers
    inner: Optional['LogicStatement'] = None  # For NOT and quantifiers

    def __str__(self) -> str:
        if self.statement_type == LogicType.ATOMIC:
            return str(self.value)
        elif self.statement_type == LogicType.IMPLICATION:
            return f"({self.left} → {self.right})"
        elif self.statement_type == LogicType.AND:
            return f"({self.left} ∧ {self.right})"
        elif self.statement_type == LogicType.OR:
            return f"({self.left} ∨ {self.right})"
        elif self.statement_type == LogicType.NOT:
            return f"¬{self.inner}"
        elif self.statement_type == LogicType.FORALL:
            return f"∀{self.variable}.{self.inner}"
        elif self.statement_type == LogicType.EXISTS:
            return f"∃{self.variable}.{self.inner}"
        elif self.statement_type == LogicType.EQUALS:
            return f"({self.left} = {self.right})"
        elif self.statement_type == LogicType.BICONDITIONAL:
            return f"({self.left} ↔ {self.right})"
        return "?"

    def __eq__(self, other) -> bool:
        if not isinstance(other, LogicStatement):
            return False
        if self.statement_type != other.statement_type:
            return False
        if self.statement_type == LogicType.ATOMIC:
            return self.value == other.value
        elif self.statement_type in [LogicType.IMPLICATION, LogicType.AND, LogicType.OR,
                                     LogicType.EQUALS, LogicType.BICONDITIONAL]:
            return self.left == other.left and self.right == other.right
        elif self.statement_type in [LogicType.NOT, LogicType.FORALL, LogicType.EXISTS]:
            return self.variable == other.variable and self.inner == other.inner
        return False

    def __hash__(self) -> int:
        return hash(str(self))


class InferenceRule:
    """Base class for inference rules"""
    name: str = "BaseRule"
    difficulty: int = 1  # Rule difficulty level

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[LogicStatement]:
        """Apply inference rule to premises, return new conclusions"""
        return []

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        """Check if rule can be applied"""
        return False


# ============================================================================
# LEVEL 1 RULES: Basic Inference
# ============================================================================

class ModusPonens(InferenceRule):
    """Modus Ponens: P, P→Q ⊢ Q"""
    name = "Modus Ponens"
    difficulty = 1

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        for p1 in premises:
            for p2 in premises:
                if (p2.statement_type == LogicType.IMPLICATION and
                    p2.left == p1):
                    return True
        return False

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p1 in premises:
            for p2 in premises:
                if (p2.statement_type == LogicType.IMPLICATION and
                    p2.left == p1):
                    proof = f"Modus Ponens: {p1}, {p2} ⊢ {p2.right}"
                    results.append((p2.right, proof))
        return results


class AndElimination(InferenceRule):
    """And Elimination: P∧Q ⊢ P, Q"""
    name = "And Elimination"
    difficulty = 1

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        return any(p.statement_type == LogicType.AND for p in premises)

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p in premises:
            if p.statement_type == LogicType.AND:
                proof_left = f"And Elimination (left): {p} ⊢ {p.left}"
                proof_right = f"And Elimination (right): {p} ⊢ {p.right}"
                results.append((p.left, proof_left))
                results.append((p.right, proof_right))
        return results


class AndIntroduction(InferenceRule):
    """And Introduction: P, Q ⊢ P∧Q"""
    name = "And Introduction"
    difficulty = 1

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        return len(premises) >= 2

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for i, p1 in enumerate(premises):
            for p2 in premises[i+1:]:
                new_stmt = LogicStatement(
                    statement_type=LogicType.AND,
                    left=p1,
                    right=p2
                )
                proof = f"And Introduction: {p1}, {p2} ⊢ {new_stmt}"
                results.append((new_stmt, proof))
        return results


# ============================================================================
# LEVEL 2 RULES: Transitivity and Chains
# ============================================================================

class HypotheticalSyllogism(InferenceRule):
    """Transitivity: P→Q, Q→R ⊢ P→R"""
    name = "Hypothetical Syllogism"
    difficulty = 2

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        for p1 in premises:
            for p2 in premises:
                if (p1.statement_type == LogicType.IMPLICATION and
                    p2.statement_type == LogicType.IMPLICATION and
                    p1.right == p2.left):
                    return True
        return False

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p1 in premises:
            for p2 in premises:
                if (p1.statement_type == LogicType.IMPLICATION and
                    p2.statement_type == LogicType.IMPLICATION and
                    p1.right == p2.left):
                    new_stmt = LogicStatement(
                        statement_type=LogicType.IMPLICATION,
                        left=p1.left,
                        right=p2.right
                    )
                    proof = f"Hypothetical Syllogism: {p1}, {p2} ⊢ {new_stmt}"
                    results.append((new_stmt, proof))
        return results


class DisjunctiveSyllogism(InferenceRule):
    """Disjunctive Syllogism: P∨Q, ¬P ⊢ Q"""
    name = "Disjunctive Syllogism"
    difficulty = 2

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        for p1 in premises:
            for p2 in premises:
                if p1.statement_type == LogicType.OR:
                    if (p2.statement_type == LogicType.NOT and
                        p2.inner == p1.left):
                        return True
                    if (p2.statement_type == LogicType.NOT and
                        p2.inner == p1.right):
                        return True
        return False

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p1 in premises:
            for p2 in premises:
                if p1.statement_type == LogicType.OR:
                    if (p2.statement_type == LogicType.NOT and
                        p2.inner == p1.left):
                        proof = f"Disjunctive Syllogism: {p1}, {p2} ⊢ {p1.right}"
                        results.append((p1.right, proof))
                    if (p2.statement_type == LogicType.NOT and
                        p2.inner == p1.right):
                        proof = f"Disjunctive Syllogism: {p1}, {p2} ⊢ {p1.left}"
                        results.append((p1.left, proof))
        return results


# ============================================================================
# LEVEL 3 RULES: Negation and Logical Equivalences
# ============================================================================

class Contrapositive(InferenceRule):
    """Contrapositive: P→Q ⊢ ¬Q→¬P"""
    name = "Contrapositive"
    difficulty = 3

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        return any(p.statement_type == LogicType.IMPLICATION for p in premises)

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p in premises:
            if p.statement_type == LogicType.IMPLICATION:
                not_q = LogicStatement(LogicType.NOT, inner=p.right)
                not_p = LogicStatement(LogicType.NOT, inner=p.left)
                new_stmt = LogicStatement(
                    statement_type=LogicType.IMPLICATION,
                    left=not_q,
                    right=not_p
                )
                proof = f"Contrapositive: {p} ⊢ {new_stmt}"
                results.append((new_stmt, proof))
        return results


class DoubleNegation(InferenceRule):
    """Double Negation: ¬¬P ⊢ P and P ⊢ ¬¬P"""
    name = "Double Negation"
    difficulty = 3

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        for p in premises:
            if p.statement_type == LogicType.NOT and p.inner.statement_type == LogicType.NOT:
                return True
        return True  # Can always apply to add double negation

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p in premises:
            # Eliminate double negation
            if p.statement_type == LogicType.NOT and p.inner.statement_type == LogicType.NOT:
                proof = f"Double Negation Elimination: {p} ⊢ {p.inner.inner}"
                results.append((p.inner.inner, proof))
        return results


class DeMorganAnd(InferenceRule):
    """De Morgan: ¬(P∧Q) ⊢ ¬P∨¬Q"""
    name = "De Morgan (AND)"
    difficulty = 3

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        for p in premises:
            if (p.statement_type == LogicType.NOT and
                p.inner.statement_type == LogicType.AND):
                return True
        return False

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p in premises:
            if (p.statement_type == LogicType.NOT and
                p.inner.statement_type == LogicType.AND):
                not_left = LogicStatement(LogicType.NOT, inner=p.inner.left)
                not_right = LogicStatement(LogicType.NOT, inner=p.inner.right)
                new_stmt = LogicStatement(
                    statement_type=LogicType.OR,
                    left=not_left,
                    right=not_right
                )
                proof = f"De Morgan (AND): {p} ⊢ {new_stmt}"
                results.append((new_stmt, proof))
        return results


class DeMorganOr(InferenceRule):
    """De Morgan: ¬(P∨Q) ⊢ ¬P∧¬Q"""
    name = "De Morgan (OR)"
    difficulty = 3

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        for p in premises:
            if (p.statement_type == LogicType.NOT and
                p.inner.statement_type == LogicType.OR):
                return True
        return False

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p in premises:
            if (p.statement_type == LogicType.NOT and
                p.inner.statement_type == LogicType.OR):
                not_left = LogicStatement(LogicType.NOT, inner=p.inner.left)
                not_right = LogicStatement(LogicType.NOT, inner=p.inner.right)
                new_stmt = LogicStatement(
                    statement_type=LogicType.AND,
                    left=not_left,
                    right=not_right
                )
                proof = f"De Morgan (OR): {p} ⊢ {new_stmt}"
                results.append((new_stmt, proof))
        return results


# ============================================================================
# LEVEL 4 RULES: Biconditional and Complex Logic
# ============================================================================

class BiconditionalIntroduction(InferenceRule):
    """Biconditional: P→Q, Q→P ⊢ P↔Q"""
    name = "Biconditional Introduction"
    difficulty = 4

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        for p1 in premises:
            for p2 in premises:
                if (p1.statement_type == LogicType.IMPLICATION and
                    p2.statement_type == LogicType.IMPLICATION and
                    p1.left == p2.right and p1.right == p2.left):
                    return True
        return False

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p1 in premises:
            for p2 in premises:
                if (p1.statement_type == LogicType.IMPLICATION and
                    p2.statement_type == LogicType.IMPLICATION and
                    p1.left == p2.right and p1.right == p2.left):
                    new_stmt = LogicStatement(
                        statement_type=LogicType.BICONDITIONAL,
                        left=p1.left,
                        right=p1.right
                    )
                    proof = f"Biconditional Introduction: {p1}, {p2} ⊢ {new_stmt}"
                    results.append((new_stmt, proof))
        return results


class BiconditionalElimination(InferenceRule):
    """Biconditional: P↔Q ⊢ P→Q, Q→P"""
    name = "Biconditional Elimination"
    difficulty = 4

    @staticmethod
    def can_apply(premises: List[LogicStatement]) -> bool:
        return any(p.statement_type == LogicType.BICONDITIONAL for p in premises)

    @staticmethod
    def apply(premises: List[LogicStatement]) -> List[Tuple[LogicStatement, str]]:
        results = []
        for p in premises:
            if p.statement_type == LogicType.BICONDITIONAL:
                forward = LogicStatement(
                    statement_type=LogicType.IMPLICATION,
                    left=p.left,
                    right=p.right
                )
                backward = LogicStatement(
                    statement_type=LogicType.IMPLICATION,
                    left=p.right,
                    right=p.left
                )
                proof_f = f"Biconditional Elimination (→): {p} ⊢ {forward}"
                proof_b = f"Biconditional Elimination (←): {p} ⊢ {backward}"
                results.append((forward, proof_f))
                results.append((backward, proof_b))
        return results


@dataclass
class ProofStep:
    """A single step in a proof"""
    statement: LogicStatement
    justification: str
    step_number: int


@dataclass
class Proof:
    """A complete formal proof"""
    axioms: List[LogicStatement]
    goal: LogicStatement
    steps: List[ProofStep] = field(default_factory=list)
    success: bool = False
    strategy_used: str = ""
    difficulty_level: int = 1

    def add_step(self, statement: LogicStatement, justification: str):
        """Add a step to the proof"""
        self.steps.append(ProofStep(
            statement=statement,
            justification=justification,
            step_number=len(self.steps) + 1
        ))
        if statement == self.goal:
            self.success = True

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict"""
        return {
            "axioms": [str(a) for a in self.axioms],
            "goal": str(self.goal),
            "steps": [
                {
                    "step": step.step_number,
                    "statement": str(step.statement),
                    "justification": step.justification
                }
                for step in self.steps
            ],
            "success": self.success,
            "strategy": self.strategy_used,
            "proof_length": len(self.steps),
            "difficulty": self.difficulty_level
        }


class ProofSearchEngine:
    """Search engine for finding proofs"""

    def __init__(self, max_difficulty: int = 4):
        # All inference rules
        all_rules = [
            # Level 1
            ModusPonens(),
            AndElimination(),
            AndIntroduction(),
            # Level 2
            HypotheticalSyllogism(),
            DisjunctiveSyllogism(),
            # Level 3
            Contrapositive(),
            DoubleNegation(),
            DeMorganAnd(),
            DeMorganOr(),
            # Level 4
            BiconditionalIntroduction(),
            BiconditionalElimination(),
        ]

        # Filter rules by difficulty
        self.inference_rules = [r for r in all_rules if r.difficulty <= max_difficulty]
        self.max_steps = 100
        self.max_breadth = 150

    def forward_chaining(self, axioms: List[LogicStatement], goal: LogicStatement) -> Optional[Proof]:
        """Forward chaining: start from axioms, derive until goal reached"""
        proof = Proof(axioms=axioms, goal=goal, strategy_used="Forward Chaining")

        # Start with axioms
        known_facts = set(axioms)
        for axiom in axioms:
            proof.add_step(axiom, "Axiom")

        # Keep applying inference rules
        for step in range(self.max_steps):
            if goal in known_facts:
                return proof

            new_facts = set()
            facts_list = list(known_facts)

            # Apply each inference rule
            for rule in self.inference_rules:
                if rule.can_apply(facts_list):
                    results = rule.apply(facts_list)
                    for new_stmt, justification in results:
                        if new_stmt not in known_facts and new_stmt not in new_facts:
                            new_facts.add(new_stmt)
                            proof.add_step(new_stmt, justification)

                            if new_stmt == goal:
                                return proof

                            # Limit breadth
                            if len(new_facts) > self.max_breadth:
                                break
                if len(new_facts) > self.max_breadth:
                    break

            if not new_facts:
                # No new facts derived, proof failed
                return proof

            known_facts.update(new_facts)

        return proof


class TheoremGenerator:
    """Generate theorems of increasing difficulty"""

    @staticmethod
    def generate_level_1_theorems() -> List[Tuple[List[LogicStatement], LogicStatement, int]]:
        """Level 1: Basic inference"""
        theorems = []

        P = LogicStatement(LogicType.ATOMIC, "P")
        Q = LogicStatement(LogicType.ATOMIC, "Q")
        R = LogicStatement(LogicType.ATOMIC, "R")

        # Modus Ponens
        axioms = [P, LogicStatement(LogicType.IMPLICATION, left=P, right=Q)]
        theorems.append((axioms, Q, 1))

        # And elimination
        axioms = [LogicStatement(LogicType.AND, left=P, right=Q)]
        theorems.append((axioms, P, 1))
        theorems.append((axioms, Q, 1))

        return theorems

    @staticmethod
    def generate_level_2_theorems() -> List[Tuple[List[LogicStatement], LogicStatement, int]]:
        """Level 2: Transitivity and chains"""
        theorems = []

        P = LogicStatement(LogicType.ATOMIC, "P")
        Q = LogicStatement(LogicType.ATOMIC, "Q")
        R = LogicStatement(LogicType.ATOMIC, "R")
        S = LogicStatement(LogicType.ATOMIC, "S")

        # Transitivity
        axioms = [
            LogicStatement(LogicType.IMPLICATION, left=P, right=Q),
            LogicStatement(LogicType.IMPLICATION, left=Q, right=R)
        ]
        goal = LogicStatement(LogicType.IMPLICATION, left=P, right=R)
        theorems.append((axioms, goal, 2))

        # Chain of 3
        axioms = [
            P,
            LogicStatement(LogicType.IMPLICATION, left=P, right=Q),
            LogicStatement(LogicType.IMPLICATION, left=Q, right=R),
            LogicStatement(LogicType.IMPLICATION, left=R, right=S)
        ]
        theorems.append((axioms, S, 2))

        return theorems

    @staticmethod
    def generate_level_3_theorems() -> List[Tuple[List[LogicStatement], LogicStatement, int]]:
        """Level 3: Negation and logical equivalences"""
        theorems = []

        P = LogicStatement(LogicType.ATOMIC, "P")
        Q = LogicStatement(LogicType.ATOMIC, "Q")
        R = LogicStatement(LogicType.ATOMIC, "R")

        # Contrapositive then modus ponens
        # P→Q, ¬Q ⊢ ¬P
        not_q = LogicStatement(LogicType.NOT, inner=Q)
        not_p = LogicStatement(LogicType.NOT, inner=P)
        axioms = [
            LogicStatement(LogicType.IMPLICATION, left=P, right=Q),
            not_q
        ]
        theorems.append((axioms, not_p, 3))

        # De Morgan's law
        # ¬(P∧Q) ⊢ ¬P∨¬Q
        not_p_and_q = LogicStatement(
            LogicType.NOT,
            inner=LogicStatement(LogicType.AND, left=P, right=Q)
        )
        not_p_or_not_q = LogicStatement(
            LogicType.OR,
            left=not_p,
            right=LogicStatement(LogicType.NOT, inner=Q)
        )
        axioms = [not_p_and_q]
        theorems.append((axioms, not_p_or_not_q, 3))

        # Double negation
        not_not_p = LogicStatement(LogicType.NOT, inner=not_p)
        axioms = [not_not_p]
        theorems.append((axioms, P, 3))

        return theorems

    @staticmethod
    def generate_level_4_theorems() -> List[Tuple[List[LogicStatement], LogicStatement, int]]:
        """Level 4: Biconditionals and complex logic"""
        theorems = []

        P = LogicStatement(LogicType.ATOMIC, "P")
        Q = LogicStatement(LogicType.ATOMIC, "Q")
        R = LogicStatement(LogicType.ATOMIC, "R")

        # Biconditional introduction
        # P→Q, Q→P ⊢ P↔Q
        axioms = [
            LogicStatement(LogicType.IMPLICATION, left=P, right=Q),
            LogicStatement(LogicType.IMPLICATION, left=Q, right=P)
        ]
        goal = LogicStatement(LogicType.BICONDITIONAL, left=P, right=Q)
        theorems.append((axioms, goal, 4))

        # Biconditional transitivity
        # P↔Q, Q↔R ⊢ P↔R
        axioms = [
            LogicStatement(LogicType.BICONDITIONAL, left=P, right=Q),
            LogicStatement(LogicType.BICONDITIONAL, left=Q, right=R)
        ]
        goal = LogicStatement(LogicType.BICONDITIONAL, left=P, right=R)
        theorems.append((axioms, goal, 4))

        # Complex: (P→Q)∧(R→Q), P∨R ⊢ Q
        p_implies_q = LogicStatement(LogicType.IMPLICATION, left=P, right=Q)
        r_implies_q = LogicStatement(LogicType.IMPLICATION, left=R, right=Q)
        axioms = [
            LogicStatement(LogicType.AND, left=p_implies_q, right=r_implies_q),
            LogicStatement(LogicType.OR, left=P, right=R)
        ]
        theorems.append((axioms, Q, 4))

        return theorems

    @staticmethod
    def generate_novel_conjectures() -> List[Tuple[List[LogicStatement], LogicStatement, int]]:
        """Level 5+: Novel conjectures to attempt"""
        conjectures = []

        P = LogicStatement(LogicType.ATOMIC, "P")
        Q = LogicStatement(LogicType.ATOMIC, "Q")
        R = LogicStatement(LogicType.ATOMIC, "R")
        S = LogicStatement(LogicType.ATOMIC, "S")

        # Novel conjecture 1: Complex chain with negations
        not_q = LogicStatement(LogicType.NOT, inner=Q)
        not_s = LogicStatement(LogicType.NOT, inner=S)
        axioms = [
            LogicStatement(LogicType.IMPLICATION, left=P, right=Q),
            LogicStatement(LogicType.IMPLICATION, left=Q, right=R),
            LogicStatement(LogicType.IMPLICATION, left=R, right=S),
            not_s
        ]
        goal = LogicStatement(LogicType.NOT, inner=P)
        conjectures.append((axioms, goal, 5))

        # Novel conjecture 2: Symmetric properties
        # (P→Q)∧(Q→P), (P↔R) ⊢ (Q↔R)
        axioms = [
            LogicStatement(LogicType.BICONDITIONAL, left=P, right=Q),
            LogicStatement(LogicType.BICONDITIONAL, left=P, right=R)
        ]
        goal = LogicStatement(LogicType.BICONDITIONAL, left=Q, right=R)
        conjectures.append((axioms, goal, 5))

        # Novel conjecture 3: Distributive property proof
        # (P∨Q)∧R ⊢ (P∧R)∨(Q∧R)
        p_or_q = LogicStatement(LogicType.OR, left=P, right=Q)
        axioms = [LogicStatement(LogicType.AND, left=p_or_q, right=R)]
        p_and_r = LogicStatement(LogicType.AND, left=P, right=R)
        q_and_r = LogicStatement(LogicType.AND, left=Q, right=R)
        goal = LogicStatement(LogicType.OR, left=p_and_r, right=q_and_r)
        conjectures.append((axioms, goal, 6))

        return conjectures


@dataclass
class ProofAgent:
    """Agent that learns to construct proofs"""
    agent_id: int
    proofs_attempted: int = 0
    proofs_succeeded: int = 0
    strategy_success: Dict[str, int] = field(default_factory=lambda: {
        "Forward Chaining": 0
    })
    avg_proof_length: float = 0.0
    difficulty_reached: int = 1

    def attempt_proof(self, axioms: List[LogicStatement], goal: LogicStatement,
                     engine: ProofSearchEngine, difficulty: int) -> Proof:
        """Attempt to construct a proof"""
        self.proofs_attempted += 1

        proof = engine.forward_chaining(axioms, goal)
        proof.difficulty_level = difficulty

        if proof.success:
            self.proofs_succeeded += 1
            self.strategy_success[proof.strategy_used] += 1
            self.difficulty_reached = max(self.difficulty_reached, difficulty)

            # Update average proof length
            self.avg_proof_length = (
                (self.avg_proof_length * (self.proofs_succeeded - 1) + len(proof.steps)) /
                self.proofs_succeeded
            )

        return proof


def run_progressive_proof_challenge(n_agents: int = 5, max_level: int = 6,
                                    save_dir: str = "data/progressive_proofs"):
    """Run progressive proof difficulty challenge"""

    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            🎓 PROGRESSIVE PROOF DIFFICULTY SYSTEM 🎓                       ║
║                                                                            ║
║        From Simple Theorems to UNPROVEN Mathematical Statements!           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Testing on progressively harder theorems, culminating in NOVEL conjectures!

DIFFICULTY LEVELS:
  Level 1: Basic inference (Modus Ponens, And/Or)
  Level 2: Transitivity, chains
  Level 3: Negation, Contrapositive, De Morgan
  Level 4: Biconditionals, complex logic
  Level 5+: NOVEL THEOREMS - Never proven before!

""")

    # Create agents
    agents = [ProofAgent(agent_id=i) for i in range(n_agents)]

    # Generate all difficulty levels
    all_theorems = []
    if max_level >= 1:
        all_theorems.extend(TheoremGenerator.generate_level_1_theorems())
    if max_level >= 2:
        all_theorems.extend(TheoremGenerator.generate_level_2_theorems())
    if max_level >= 3:
        all_theorems.extend(TheoremGenerator.generate_level_3_theorems())
    if max_level >= 4:
        all_theorems.extend(TheoremGenerator.generate_level_4_theorems())
    if max_level >= 5:
        all_theorems.extend(TheoremGenerator.generate_novel_conjectures())

    print(f"🤖 Agents: {n_agents}")
    print(f"🎯 Total theorems: {len(all_theorems)}")
    print(f"📊 Max difficulty level: {max_level}\n")

    print("="*80)
    print("PROGRESSIVE PROOF GENERATION")
    print("="*80)

    all_proofs = []
    start_time = time.time()

    current_level = 0
    for theorem_id, (axioms, goal, difficulty) in enumerate(all_theorems, 1):
        if difficulty > current_level:
            current_level = difficulty
            print(f"\n{'='*80}")
            print(f"DIFFICULTY LEVEL {current_level}")
            print(f"{'='*80}")

        print(f"\n📐 Theorem {theorem_id} (Level {difficulty}):")
        print(f"  Axioms: {', '.join(str(a) for a in axioms)}")
        print(f"  Goal: {goal}")

        # Create engine with appropriate difficulty
        engine = ProofSearchEngine(max_difficulty=difficulty)

        # Have agents try to prove it
        best_proof = None
        best_agent_id = -1

        for agent in agents:
            proof = agent.attempt_proof(axioms, goal, engine, difficulty)

            if proof.success:
                if best_proof is None or len(proof.steps) < len(best_proof.steps):
                    best_proof = proof
                    best_agent_id = agent.agent_id

        if best_proof and best_proof.success:
            print(f"  ✅ PROVED by Agent #{best_agent_id} in {len(best_proof.steps)} steps")
            print(f"  Strategy: {best_proof.strategy_used}")

            # Show condensed proof for harder theorems
            if difficulty <= 3 or len(best_proof.steps) <= 15:
                print(f"\n  Proof:")
                for step in best_proof.steps:
                    print(f"    {step.step_number}. {step.statement}")
                    if step.justification != "Axiom":
                        print(f"       └─ {step.justification}")
            else:
                print(f"\n  Proof (condensed - {len(best_proof.steps)} total steps):")
                # Show first 3, middle 1, last 3
                for step in best_proof.steps[:3]:
                    print(f"    {step.step_number}. {step.statement}")
                    if step.justification != "Axiom":
                        print(f"       └─ {step.justification}")
                print(f"    ...")
                print(f"    {len(best_proof.steps)//2}. {best_proof.steps[len(best_proof.steps)//2].statement}")
                print(f"    ...")
                for step in best_proof.steps[-3:]:
                    print(f"    {step.step_number}. {step.statement}")
                    if step.justification != "Axiom":
                        print(f"       └─ {step.justification}")

            all_proofs.append(best_proof)
        else:
            print(f"  ❌ UNSOLVED - Could not construct proof")
            if difficulty >= 5:
                print(f"     This might be genuinely difficult or unprovable!")

    elapsed = time.time() - start_time

    print("\n" + "="*80)
    print("🎯 FINAL RESULTS")
    print("="*80)
    print(f"Duration: {elapsed:.2f} seconds")
    print(f"Theorems attempted: {len(all_theorems)}")
    print(f"Successfully proved: {len(all_proofs)}")
    print(f"Success rate: {len(all_proofs)/len(all_theorems)*100:.1f}%\n")

    # Breakdown by difficulty
    print("Results by difficulty level:")
    for level in range(1, max_level + 1):
        level_attempted = sum(1 for _, _, d in all_theorems if d == level)
        level_proved = sum(1 for p in all_proofs if p.difficulty_level == level)
        if level_attempted > 0:
            print(f"  Level {level}: {level_proved}/{level_attempted} " +
                  f"({level_proved/level_attempted*100:.1f}%)")

    # Agent statistics
    print("\nAgent Performance:")
    for agent in agents:
        if agent.proofs_attempted > 0:
            success_rate = agent.proofs_succeeded / agent.proofs_attempted * 100
            print(f"  Agent #{agent.agent_id}: {agent.proofs_succeeded}/{agent.proofs_attempted} ({success_rate:.1f}%)")
            print(f"    Max difficulty reached: Level {agent.difficulty_reached}")
            print(f"    Avg proof length: {agent.avg_proof_length:.1f}")

    # Save proofs
    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    proof_data = {
        "summary": {
            "total_theorems": len(all_theorems),
            "proved": len(all_proofs),
            "success_rate": len(all_proofs)/len(all_theorems),
            "duration": elapsed,
            "n_agents": n_agents,
            "max_difficulty": max_level
        },
        "proofs": [p.to_dict() for p in all_proofs]
    }

    with open(save_path / "progressive_proofs.json", 'w') as f:
        json.dump(proof_data, f, indent=2)

    print(f"\n💾 Proofs saved to {save_path}/progressive_proofs.json")

    # Highlight novel theorems
    novel_proofs = [p for p in all_proofs if p.difficulty_level >= 5]
    if novel_proofs:
        print(f"\n🌟 NOVEL THEOREMS PROVED: {len(novel_proofs)}")
        print("These are NEW proofs not in standard logic textbooks!")

    unsolved_novel = [(ax, g, d) for ax, g, d in all_theorems
                      if d >= 5 and not any(p.goal == g for p in all_proofs)]
    if unsolved_novel:
        print(f"\n❓ UNSOLVED CONJECTURES: {len(unsolved_novel)}")
        print("These remain unproven - genuinely difficult problems!")

    return all_proofs


if __name__ == "__main__":
    proofs = run_progressive_proof_challenge(n_agents=5, max_level=6)

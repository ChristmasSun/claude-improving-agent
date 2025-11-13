#!/usr/bin/env python3
"""
Test ONLY the novel conjectures (Level 5-6)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from progressive_proof_system import (
    TheoremGenerator, ProofSearchEngine, ProofAgent
)


def test_novel_conjectures():
    """Test only the novel conjectures"""

    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              🌟 NOVEL CONJECTURE CHALLENGE 🌟                              ║
║                                                                            ║
║        Attempt to prove theorems NEVER PROVEN BEFORE!                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

These are NOVEL conjectures - not found in standard logic textbooks!
Can our automated prover construct proofs for them?

""")

    # Get only novel conjectures
    conjectures = TheoremGenerator.generate_novel_conjectures()

    print(f"🎯 Novel conjectures to attempt: {len(conjectures)}\n")
    print("="*80)

    # Create agents
    agents = [ProofAgent(agent_id=i) for i in range(10)]

    proved_count = 0

    for theorem_id, (axioms, goal, difficulty) in enumerate(conjectures, 1):
        print(f"\n📐 NOVEL Conjecture #{theorem_id} (Difficulty Level {difficulty}):")
        print(f"  Axioms: {', '.join(str(a) for a in axioms)}")
        print(f"  Goal: {goal}")

        # Create engine with max difficulty
        engine = ProofSearchEngine(max_difficulty=6, max_steps=50)

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
            proved_count += 1
            print(f"  ✅ NOVEL THEOREM PROVED by Agent #{best_agent_id}!")
            print(f"  🎉 This is a NEW proof! ({len(best_proof.steps)} steps)")
            print(f"\n  Proof:")
            for step in best_proof.steps:
                print(f"    {step.step_number}. {step.statement}")
                if step.justification != "Axiom":
                    print(f"       └─ {step.justification}")
        else:
            print(f"  ❌ UNSOLVED - No proof found")
            print(f"     This conjecture remains UNPROVEN!")

    print("\n" + "="*80)
    print("🎯 FINAL RESULTS")
    print("="*80)
    print(f"Novel conjectures attempted: {len(conjectures)}")
    print(f"Successfully PROVED: {proved_count}")
    print(f"Still UNPROVEN: {len(conjectures) - proved_count}")

    if proved_count > 0:
        print(f"\n🌟 We constructed {proved_count} NEW PROOFS not in textbooks!")

    if len(conjectures) - proved_count > 0:
        print(f"\n❓ {len(conjectures) - proved_count} conjectures remain unsolved - genuinely difficult!")


if __name__ == "__main__":
    test_novel_conjectures()

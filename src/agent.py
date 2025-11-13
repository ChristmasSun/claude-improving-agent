"""
Recursive Self-Improving AI Agent System

This module implements an AI agent that can design improved versions of itself.
Each generation becomes more autonomous and capable.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import anthropic


class Agent:
    """
    Base agent class that can generate plans and design improved versions of itself.

    Each agent has a generation number and capabilities that improve over time.
    """

    def __init__(
        self,
        generation: int = 0,
        capabilities: Optional[List[str]] = None,
        autonomy_level: int = 1,
        api_key: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929"
    ):
        """
        Initialize an agent.

        Args:
            generation: The generation number of this agent
            capabilities: List of capabilities this agent has
            autonomy_level: How autonomous the agent is (1-10)
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.generation = generation
        self.capabilities = capabilities or ["basic_planning"]
        self.autonomy_level = autonomy_level
        self.model = model

        # Initialize API client
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")

        self.client = anthropic.Anthropic(api_key=self.api_key)

        # Thought log for this agent's session
        self.thought_log: List[Dict[str, Any]] = []

    def log_thought(self, thought_type: str, content: Any, metadata: Optional[Dict] = None):
        """Log a thought or action for later analysis."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "generation": self.generation,
            "thought_type": thought_type,
            "content": content,
            "metadata": metadata or {}
        }
        self.thought_log.append(entry)

    def generate_plan(self, task: Optional[str] = None) -> str:
        """
        Generate a plan for what this agent should accomplish.

        Args:
            task: Optional specific task to plan for

        Returns:
            A plan as a string
        """
        self.log_thought("planning_start", {"task": task})

        prompt = f"""You are an AI agent (Generation {self.generation}).

Your current capabilities: {', '.join(self.capabilities)}
Your autonomy level: {self.autonomy_level}/10

{"Task: " + task if task else "Generate a plan for what you should accomplish."}

Create a clear, actionable plan. Be specific and ambitious based on your capabilities.
Format your response as a structured plan with numbered steps."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            plan = message.content[0].text
            self.log_thought("plan_generated", plan, {"model": self.model})
            return plan

        except Exception as e:
            self.log_thought("plan_error", str(e))
            raise

    def design_improved_self(self) -> Dict[str, Any]:
        """
        Design an improved version of this agent.

        Returns:
            A specification for the next generation agent including:
            - new capabilities
            - increased autonomy
            - improved code/architecture
        """
        self.log_thought("improvement_start", {"current_gen": self.generation})

        prompt = f"""You are an AI agent (Generation {self.generation}) tasked with designing an improved version of yourself.

CURRENT SPECIFICATIONS:
- Generation: {self.generation}
- Capabilities: {', '.join(self.capabilities)}
- Autonomy Level: {self.autonomy_level}/10

YOUR TASK:
Design Generation {self.generation + 1} with improvements in:
1. New capabilities (add 2-3 new meaningful capabilities)
2. Increased autonomy (raise the level by 1-2 points, max 10)
3. Better decision-making
4. More advanced features

REQUIREMENTS:
- Be specific about new capabilities
- Explain how autonomy increases
- Suggest concrete improvements to the code/architecture
- Stay grounded and achievable (incremental improvements)

Respond in JSON format:
{{
    "generation": {self.generation + 1},
    "new_capabilities": ["capability1", "capability2", ...],
    "autonomy_level": <number 1-10>,
    "improvements": ["improvement1", "improvement2", ...],
    "rationale": "Why these improvements make the agent better",
    "code_suggestions": "Specific code improvements or new methods to add"
}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text

            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            design = json.loads(response_text)
            self.log_thought("improvement_designed", design)

            return design

        except Exception as e:
            self.log_thought("improvement_error", str(e))
            raise

    def execute_plan(self, plan: str) -> Dict[str, Any]:
        """
        Execute the given plan (simulated for now).

        In a more advanced version, this could actually execute tasks.

        Args:
            plan: The plan to execute

        Returns:
            Execution results
        """
        self.log_thought("execution_start", plan)

        # For now, we simulate execution by analyzing the plan
        prompt = f"""You are executing the following plan:

{plan}

Simulate the execution of this plan and report:
1. What steps you would take
2. What results you would achieve
3. Any challenges you would face

Respond in JSON format:
{{
    "steps_taken": ["step1", "step2", ...],
    "results": ["result1", "result2", ...],
    "challenges": ["challenge1", "challenge2", ...],
    "success_rate": <0-100>
}}"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text

            # Extract JSON from response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            results = json.loads(response_text)
            self.log_thought("execution_complete", results)

            return results

        except Exception as e:
            self.log_thought("execution_error", str(e))
            raise

    def save_generation(self, output_dir: Path):
        """Save this generation's code and thought log."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save thought log
        log_file = output_dir / f"generation_{self.generation}_log.json"
        with open(log_file, "w") as f:
            json.dump({
                "generation": self.generation,
                "capabilities": self.capabilities,
                "autonomy_level": self.autonomy_level,
                "thought_log": self.thought_log
            }, f, indent=2)

        self.log_thought("generation_saved", str(log_file))

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of this agent's configuration and performance."""
        return {
            "generation": self.generation,
            "capabilities": self.capabilities,
            "autonomy_level": self.autonomy_level,
            "thoughts_logged": len(self.thought_log),
            "model": self.model
        }

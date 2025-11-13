"""
Tests for the AgentRunner class
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, call
from src.runner import AgentRunner
from src.agent import Agent


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def runner(mock_api_key, tmp_path):
    """Create a test runner."""
    import os
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
        return AgentRunner(
            max_generations=3,
            output_dir=str(tmp_path / "test_generations"),
            api_key=mock_api_key
        )


class TestRunnerInitialization:
    """Test runner initialization."""

    def test_runner_creation(self, runner):
        """Test creating a runner."""
        assert runner.max_generations == 3
        assert runner.output_dir.exists()
        assert len(runner.generations) == 0
        assert len(runner.run_log) == 0

    def test_runner_creates_output_dir(self, tmp_path, mock_api_key):
        """Test that runner creates output directory."""
        output_dir = tmp_path / "new_dir"
        assert not output_dir.exists()

        import os
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
            runner = AgentRunner(output_dir=str(output_dir), api_key=mock_api_key)

        assert output_dir.exists()


class TestAgentCreation:
    """Test agent creation methods."""

    def test_create_initial_agent(self, runner):
        """Test creating the initial agent."""
        agent = runner.create_initial_agent()

        assert agent.generation == 0
        assert "basic_planning" in agent.capabilities
        assert agent.autonomy_level == 1
        assert len(runner.run_log) > 0

    def test_create_next_generation(self, runner):
        """Test creating next generation from design."""
        design = {
            "generation": 1,
            "new_capabilities": ["planning", "execution", "analysis"],
            "autonomy_level": 3,
            "improvements": ["test"],
            "rationale": "test",
            "code_suggestions": "test"
        }

        agent = runner.create_next_generation(design)

        assert agent.generation == 1
        assert agent.capabilities == ["planning", "execution", "analysis"]
        assert agent.autonomy_level == 3

    def test_create_next_generation_caps_autonomy(self, runner):
        """Test that autonomy level is capped at 10."""
        design = {
            "generation": 5,
            "new_capabilities": ["advanced"],
            "autonomy_level": 15,  # Over the limit
            "improvements": ["test"],
            "rationale": "test",
            "code_suggestions": "test"
        }

        agent = runner.create_next_generation(design)

        assert agent.autonomy_level == 10  # Should be capped


class TestRunGeneration:
    """Test running a single generation."""

    @patch.object(Agent, "generate_plan")
    @patch.object(Agent, "execute_plan")
    @patch.object(Agent, "design_improved_self")
    @patch.object(Agent, "save_generation")
    def test_run_generation_full_cycle(
        self,
        mock_save,
        mock_design,
        mock_execute,
        mock_plan,
        runner
    ):
        """Test running a full generation cycle."""
        # Setup mocks
        mock_plan.return_value = "Test plan"
        mock_execute.return_value = {
            "steps_taken": ["step1"],
            "results": ["result1"],
            "challenges": [],
            "success_rate": 95
        }
        mock_design.return_value = {
            "generation": 1,
            "new_capabilities": ["advanced"],
            "autonomy_level": 2,
            "improvements": ["test"],
            "rationale": "test",
            "code_suggestions": "test"
        }

        agent = runner.create_initial_agent()
        results = runner.run_generation(agent)

        # Verify all methods were called
        mock_plan.assert_called_once()
        mock_execute.assert_called_once_with("Test plan")
        mock_design.assert_called_once()
        mock_save.assert_called_once()

        # Verify results structure
        assert results["generation"] == 0
        assert results["plan"] == "Test plan"
        assert results["execution"]["success_rate"] == 95
        assert results["improvement_design"]["generation"] == 1

    @patch.object(Agent, "generate_plan")
    @patch.object(Agent, "execute_plan")
    @patch.object(Agent, "design_improved_self")
    @patch.object(Agent, "save_generation")
    def test_run_generation_skips_design_for_last_gen(
        self,
        mock_save,
        mock_design,
        mock_execute,
        mock_plan,
        runner
    ):
        """Test that last generation doesn't design improvement."""
        mock_plan.return_value = "Final plan"
        mock_execute.return_value = {
            "steps_taken": ["step1"],
            "results": ["result1"],
            "challenges": [],
            "success_rate": 100
        }

        # Create agent for last generation
        import os
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            agent = Agent(
                generation=runner.max_generations - 1,
                api_key="test-key"
            )

        results = runner.run_generation(agent)

        # Design should not be called
        mock_design.assert_not_called()
        assert results["improvement_design"] is None


class TestFullRun:
    """Test the complete run cycle."""

    @patch.object(Agent, "generate_plan")
    @patch.object(Agent, "execute_plan")
    @patch.object(Agent, "design_improved_self")
    @patch.object(Agent, "save_generation")
    def test_run_complete_cycle(
        self,
        mock_save,
        mock_design,
        mock_execute,
        mock_plan,
        runner,
        tmp_path
    ):
        """Test running the complete improvement cycle."""
        # Setup mocks for 3 generations
        mock_plan.return_value = "Test plan"
        mock_execute.return_value = {
            "steps_taken": ["step1"],
            "results": ["result1"],
            "challenges": [],
            "success_rate": 90
        }

        # Mock design to return increasing capabilities
        def design_side_effect():
            gen = mock_design.call_count
            return {
                "generation": gen,
                "new_capabilities": [f"cap{gen}a", f"cap{gen}b"],
                "autonomy_level": gen + 2,
                "improvements": ["test"],
                "rationale": "test",
                "code_suggestions": "test"
            }

        mock_design.side_effect = design_side_effect

        # Run the cycle
        results = runner.run(task="Test task")

        # Verify we got results for all generations
        assert len(results) == 3

        # Verify progression
        assert results[0]["generation"] == 0
        assert results[1]["generation"] == 1
        assert results[2]["generation"] == 2

        # Verify agents were created and improved
        assert len(runner.generations) == 3
        assert runner.generations[0].generation == 0
        assert runner.generations[1].generation == 1
        assert runner.generations[2].generation == 2

        # Verify autonomy increased
        assert runner.generations[1].autonomy_level > runner.generations[0].autonomy_level

    def test_run_saves_summary(self, runner, tmp_path):
        """Test that run saves a summary file."""
        with patch.object(Agent, "generate_plan", return_value="Plan"):
            with patch.object(Agent, "execute_plan", return_value={"success_rate": 90}):
                with patch.object(Agent, "design_improved_self", return_value={
                    "generation": 1,
                    "new_capabilities": ["test"],
                    "autonomy_level": 2,
                    "improvements": [],
                    "rationale": "",
                    "code_suggestions": ""
                }):
                    with patch.object(Agent, "save_generation"):
                        runner.run()

        summary_file = runner.output_dir / "run_summary.json"
        assert summary_file.exists()

        with open(summary_file) as f:
            summary = json.load(f)

        assert "generations" in summary
        assert "run_log" in summary
        assert summary["max_generations"] == 3


class TestRunnerUtilities:
    """Test runner utility methods."""

    def test_log_event(self, runner):
        """Test logging an event."""
        runner.log_event("test_event", {"key": "value"})

        assert len(runner.run_log) == 1
        assert runner.run_log[0]["event_type"] == "test_event"
        assert runner.run_log[0]["data"] == {"key": "value"}

    def test_get_generation_summary(self, runner):
        """Test getting a generation summary."""
        agent = runner.create_initial_agent()
        runner.generations.append(agent)

        summary = runner.get_generation_summary(0)

        assert summary is not None
        assert summary["generation"] == 0

    def test_get_generation_summary_invalid(self, runner):
        """Test getting summary for non-existent generation."""
        summary = runner.get_generation_summary(99)
        assert summary is None

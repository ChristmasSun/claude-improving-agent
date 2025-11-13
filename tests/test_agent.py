"""
Tests for the Agent class
"""

import json
import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src.agent import Agent


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def agent(mock_api_key):
    """Create a test agent."""
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
        return Agent(generation=0, capabilities=["test"], autonomy_level=1)


@pytest.fixture
def mock_anthropic_client():
    """Mock the Anthropic client."""
    with patch("src.agent.anthropic.Anthropic") as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance

        # Mock message response
        mock_response = Mock()
        mock_response.content = [Mock(text="Test response")]
        mock_instance.messages.create.return_value = mock_response

        yield mock_instance


class TestAgentInitialization:
    """Test agent initialization."""

    def test_agent_creation_with_defaults(self, mock_api_key):
        """Test creating an agent with default parameters."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
            agent = Agent()

            assert agent.generation == 0
            assert agent.capabilities == ["basic_planning"]
            assert agent.autonomy_level == 1
            assert agent.model == "claude-sonnet-4-5-20250929"
            assert len(agent.thought_log) == 0

    def test_agent_creation_with_custom_params(self, mock_api_key):
        """Test creating an agent with custom parameters."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
            agent = Agent(
                generation=3,
                capabilities=["planning", "execution", "learning"],
                autonomy_level=7
            )

            assert agent.generation == 3
            assert agent.capabilities == ["planning", "execution", "learning"]
            assert agent.autonomy_level == 7

    def test_agent_requires_api_key(self):
        """Test that agent requires an API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY must be set"):
                Agent()


class TestAgentLogging:
    """Test agent logging functionality."""

    def test_log_thought(self, agent):
        """Test logging a thought."""
        agent.log_thought("test_type", "test content", {"key": "value"})

        assert len(agent.thought_log) == 1
        assert agent.thought_log[0]["thought_type"] == "test_type"
        assert agent.thought_log[0]["content"] == "test content"
        assert agent.thought_log[0]["metadata"] == {"key": "value"}
        assert agent.thought_log[0]["generation"] == 0
        assert "timestamp" in agent.thought_log[0]

    def test_log_multiple_thoughts(self, agent):
        """Test logging multiple thoughts."""
        agent.log_thought("type1", "content1")
        agent.log_thought("type2", "content2")
        agent.log_thought("type3", "content3")

        assert len(agent.thought_log) == 3
        assert agent.thought_log[0]["thought_type"] == "type1"
        assert agent.thought_log[1]["thought_type"] == "type2"
        assert agent.thought_log[2]["thought_type"] == "type3"


class TestAgentPlanning:
    """Test agent planning functionality."""

    @patch("src.agent.anthropic.Anthropic")
    def test_generate_plan_without_task(self, mock_anthropic, mock_api_key):
        """Test generating a plan without a specific task."""
        # Setup mock
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock(text="1. Analyze environment\n2. Set goals\n3. Execute")]
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
            agent = Agent(generation=0)
            plan = agent.generate_plan()

            assert plan == "1. Analyze environment\n2. Set goals\n3. Execute"
            assert len(agent.thought_log) >= 2  # planning_start and plan_generated

    @patch("src.agent.anthropic.Anthropic")
    def test_generate_plan_with_task(self, mock_anthropic, mock_api_key):
        """Test generating a plan with a specific task."""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        mock_response = Mock()
        mock_response.content = [Mock(text="Custom plan for task")]
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
            agent = Agent()
            plan = agent.generate_plan(task="Build a web scraper")

            # Verify the prompt included the task
            call_args = mock_client.messages.create.call_args
            assert "Build a web scraper" in call_args[1]["messages"][0]["content"]


class TestAgentImprovement:
    """Test agent self-improvement functionality."""

    @patch("src.agent.anthropic.Anthropic")
    def test_design_improved_self(self, mock_anthropic, mock_api_key):
        """Test designing an improved version."""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        improvement_design = {
            "generation": 1,
            "new_capabilities": ["planning", "execution", "learning"],
            "autonomy_level": 3,
            "improvements": ["Better analysis", "Faster execution"],
            "rationale": "These improvements increase effectiveness",
            "code_suggestions": "Add caching layer"
        }

        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps(improvement_design))]
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
            agent = Agent(generation=0)
            design = agent.design_improved_self()

            assert design["generation"] == 1
            assert len(design["new_capabilities"]) == 3
            assert design["autonomy_level"] == 3

    @patch("src.agent.anthropic.Anthropic")
    def test_design_improved_self_handles_markdown(self, mock_anthropic, mock_api_key):
        """Test that design handles JSON in markdown code blocks."""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        improvement_design = {
            "generation": 1,
            "new_capabilities": ["advanced"],
            "autonomy_level": 2,
            "improvements": ["test"],
            "rationale": "test",
            "code_suggestions": "test"
        }

        # Response wrapped in markdown
        markdown_response = f"```json\n{json.dumps(improvement_design)}\n```"

        mock_response = Mock()
        mock_response.content = [Mock(text=markdown_response)]
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
            agent = Agent()
            design = agent.design_improved_self()

            assert design["generation"] == 1


class TestAgentExecution:
    """Test agent execution functionality."""

    @patch("src.agent.anthropic.Anthropic")
    def test_execute_plan(self, mock_anthropic, mock_api_key):
        """Test plan execution."""
        mock_client = Mock()
        mock_anthropic.return_value = mock_client

        execution_results = {
            "steps_taken": ["step1", "step2"],
            "results": ["result1", "result2"],
            "challenges": ["challenge1"],
            "success_rate": 85
        }

        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps(execution_results))]
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": mock_api_key}):
            agent = Agent()
            results = agent.execute_plan("Test plan")

            assert results["success_rate"] == 85
            assert len(results["steps_taken"]) == 2


class TestAgentPersistence:
    """Test agent persistence functionality."""

    def test_save_generation(self, agent, tmp_path):
        """Test saving a generation."""
        agent.log_thought("test", "content")

        agent.save_generation(tmp_path)

        log_file = tmp_path / "generation_0_log.json"
        assert log_file.exists()

        with open(log_file) as f:
            data = json.load(f)

        assert data["generation"] == 0
        assert len(data["thought_log"]) >= 1

    def test_get_summary(self, agent):
        """Test getting an agent summary."""
        agent.log_thought("test1", "content1")
        agent.log_thought("test2", "content2")

        summary = agent.get_summary()

        assert summary["generation"] == 0
        assert summary["autonomy_level"] == 1
        assert summary["thoughts_logged"] == 2
        assert "capabilities" in summary

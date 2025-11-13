# Recursive Self-Improving AI Agent System

A fascinating experiment in AI evolution where each generation of agent designs a better, more autonomous version of itself.

## 🔥 **NEWEST**: CODE-EVOLVING AGENTS!

**THE MOST REVOLUTIONARY FEATURE**: Agents that write **ACTUAL EXECUTABLE CODE** that evolves and improves across generations!

```bash
python run_code_evolution.py
```

**WE JUST RAN THIS!** Code evolved from basic (75.2 score) to production-ready (98.9 score)!
- Real Python code written by agents
- Actually executed and tested
- Measurable improvement each generation
- 9 evolved code files saved

See [CODE_EVOLUTION.md](CODE_EVOLUTION.md) for the full story of how we evolved code from basic loops to cached, type-safe, production-ready functions!

## 🌍 Multi-Agent Evolution Ecosystem

**Multiple AI lineages evolve simultaneously**, competing, cooperating, and learning from each other!

```bash
# Run the ecosystem demo
python demo_ecosystem.py

# Run live with API key
python run_ecosystem.py --lineages 3 --generations 3
```

See [ECOSYSTEM.md](ECOSYSTEM.md) for full documentation!

## Overview

This system implements two modes:

### Single Agent Mode (Original)
1. **Generation 0** starts with basic capabilities
2. Each generation generates a plan and executes it
3. Each generation designs an improved version of itself
4. The system spawns the new generation with enhanced capabilities
5. Process repeats, creating increasingly sophisticated agents

### Ecosystem Mode (NEW! 🔥)
1. **Multiple lineages** evolve simultaneously
2. Agents **observe and learn** from successful peers
3. **Capability marketplace** enables knowledge trading
4. **Competition** drives faster innovation
5. **Real-time leaderboard** tracks fitness rankings
6. **Emergent behaviors** arise from interaction

### Key Features

- **Recursive Self-Improvement**: Each agent designs its successor
- **Multi-Agent Ecosystem**: Multiple lineages evolving together (NEW!)
- **Peer Learning**: Agents observe and learn from each other (NEW!)
- **Capability Trading**: Marketplace for sharing knowledge (NEW!)
- **Increasing Autonomy**: Agents become more autonomous over generations
- **Comprehensive Logging**: Every thought and decision is logged
- **Full Test Coverage**: Thoroughly tested with pytest
- **Flexible Configuration**: Customize generations, tasks, and models
- **Beautiful Visualization**: Real-time progress and leaderboards (NEW!)

## Installation

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd claude-improving-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

## Usage

### Basic Usage

Run with default settings (5 generations):

```bash
python main.py
```

### Advanced Usage

Specify number of generations:

```bash
python main.py --generations 7
```

Provide a specific task:

```bash
python main.py --task "Analyze and optimize a Python codebase"
```

Use a different model:

```bash
python main.py --model claude-sonnet-4-5-20250929 --generations 3
```

Customize output directory:

```bash
python main.py --output results/experiment_1/
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--generations N` | Number of generations to run | 5 |
| `--task "..."` | Specific task for agents | None |
| `--model MODEL` | Claude model to use | claude-sonnet-4-5-20250929 |
| `--output DIR` | Output directory | generations/ |

## Architecture

### Components

#### Agent (`src/agent.py`)

The core agent class with capabilities:

- **Plan Generation**: Creates structured plans using Claude API
- **Self-Design**: Designs improved versions of itself
- **Plan Execution**: Executes plans (simulated for safety)
- **Thought Logging**: Logs every decision and thought

#### AgentRunner (`src/runner.py`)

Orchestrates the recursive improvement loop:

- **Generation Management**: Creates and tracks generations
- **Evolution Control**: Manages the improvement cycle
- **Data Persistence**: Saves all generation data
- **Summary Reporting**: Generates comprehensive reports

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    AgentRunner                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Generation 0 (Autonomy: 1)                           │  │
│  │    ├─ Generate Plan                                   │  │
│  │    ├─ Execute Plan                                    │  │
│  │    └─ Design Generation 1                             │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                │
│                            ▼                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Generation 1 (Autonomy: 3)                           │  │
│  │    ├─ Generate Plan (more sophisticated)              │  │
│  │    ├─ Execute Plan (better execution)                 │  │
│  │    └─ Design Generation 2                             │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                │
│                            ▼                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Generation N (Autonomy: 9)                           │  │
│  │    ├─ Generate Plan (highly advanced)                 │  │
│  │    ├─ Execute Plan (autonomous)                       │  │
│  │    └─ Final Report                                    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Output Structure

After running, you'll find:

```
generations/
├── generation_0_log.json      # Gen 0 thought log
├── generation_1_log.json      # Gen 1 thought log
├── generation_N_log.json      # Gen N thought log
└── run_summary.json           # Complete run summary
```

### Log File Format

Each generation log contains:

```json
{
  "generation": 0,
  "capabilities": ["planning", "execution"],
  "autonomy_level": 3,
  "thought_log": [
    {
      "timestamp": "2025-11-13T10:30:00",
      "thought_type": "planning_start",
      "content": "...",
      "metadata": {}
    }
  ]
}
```

### Run Summary Format

The `run_summary.json` includes:

- Complete timeline of all generations
- Evolution of capabilities
- Performance metrics
- All thought logs combined

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_agent.py -v
```

## Development

### Project Structure

```
claude-improving-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py           # Core Agent class
│   └── runner.py          # AgentRunner orchestration
├── tests/
│   ├── __init__.py
│   ├── test_agent.py      # Agent tests
│   └── test_runner.py     # Runner tests
├── main.py                # CLI entry point
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

### Adding New Capabilities

To add new capabilities to agents:

1. Edit `src/agent.py` to add new methods
2. Update the capability list in prompts
3. Add tests in `tests/test_agent.py`
4. Update documentation

### Extending the System

Ideas for extensions:

- **Real Execution**: Implement actual plan execution
- **Multi-Agent**: Run multiple lineages in parallel
- **Capability Marketplace**: Agents share capabilities
- **Performance Metrics**: Track success rates over generations
- **Visualization**: Graph the evolution over time

## Example Output

When you run the system, you'll see output like:

```
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           RECURSIVE SELF-IMPROVING AI AGENT SYSTEM                         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Configuration:
  Generations: 5
  Model: claude-sonnet-4-5-20250929
  Task: General self-improvement

################################################################################
STARTING GENERATION 0
Capabilities: basic_planning, self_analysis
Autonomy Level: 1/10
################################################################################

================================================================================
GENERATION 0 - PLANNING PHASE
================================================================================

Plan:
1. Analyze current environment and constraints
2. Identify key improvement areas
3. Design next generation architecture
...

FINAL SUMMARY
Evolution of Capabilities:

  Generation 0:
    Autonomy Level: 1/10
    Capabilities: basic_planning, self_analysis

  Generation 1:
    Autonomy Level: 3/10
    Capabilities: planning, execution, learning

  ...
```

## Safety Considerations

This system is designed for research and exploration:

- **Simulated Execution**: Plans are analyzed, not executed on your system
- **No External Access**: Agents don't access networks or filesystems
- **Controlled Environment**: All operations are logged and contained
- **Rate Limiting**: Respects API rate limits

## Contributing

Contributions welcome! Areas of interest:

- Enhanced autonomy mechanisms
- Better self-improvement algorithms
- Visualization tools
- Performance optimizations

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with:
- [Anthropic Claude API](https://www.anthropic.com/)
- Python 3.8+
- pytest for testing

## FAQ

### Q: Will the agents actually execute code?

A: No, execution is simulated for safety. Agents analyze what they would do, but don't actually execute.

### Q: How much does this cost to run?

A: Costs depend on your API usage. Each generation makes 2-3 API calls. With 5 generations, expect ~15 API calls.

### Q: Can I run this continuously?

A: Yes, but set reasonable limits with `--generations` to control costs and time.

### Q: What's the maximum autonomy level?

A: The autonomy scale is 1-10, with 10 being fully autonomous (theoretical limit).

### Q: How are improvements validated?

A: Each generation logs its reasoning. Review the thought logs to see how agents evolve their capabilities.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Review the thought logs in `generations/`
- Check the test suite for examples

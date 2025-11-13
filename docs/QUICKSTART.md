# Quick Start Guide

Get up and running with the Recursive Self-Improving AI Agent System in 5 minutes!

## Prerequisites

- Python 3.8+
- Anthropic API key ([get one here](https://console.anthropic.com/))

## Installation (3 steps)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your API key

Create a `.env` file:

```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```

Or use the automated setup:

```bash
bash setup.sh
```

### 3. Run it!

```bash
python main.py
```

That's it! The system will:
1. Create Generation 0 with basic capabilities
2. Each generation will plan, execute, and design improvements
3. Spawn increasingly autonomous agents
4. Save all logs to `generations/` directory

## Example Runs

### Basic Run (5 generations)

```bash
python main.py
```

### Custom Task

```bash
python main.py --task "Design a system for analyzing large codebases"
```

### More Generations

```bash
python main.py --generations 10
```

### Full Configuration

```bash
python main.py \
  --generations 7 \
  --task "Build an automated testing framework" \
  --output results/experiment_1/
```

## What You'll See

When running, you'll see output like:

```
╔════════════════════════════════════════════════════════════════════════════╗
║           RECURSIVE SELF-IMPROVING AI AGENT SYSTEM                         ║
╚════════════════════════════════════════════════════════════════════════════╝

################################################################################
STARTING GENERATION 0
Capabilities: basic_planning, self_analysis
Autonomy Level: 1/10
################################################################################

================================================================================
GENERATION 0 - PLANNING PHASE
================================================================================

Plan:
1. Analyze current environment and available resources
2. Identify key areas for capability expansion
3. Design a more autonomous architecture
...
```

## Analyzing Results

After a run, analyze the results:

```bash
python analyze_run.py
```

This will show:
- Evolution of capabilities over generations
- Autonomy progression
- Thought patterns and decision-making
- Key insights from the run

Export a detailed report:

```bash
python analyze_run.py --export
```

## Understanding the Output

### Directory Structure

After running, you'll have:

```
generations/
├── generation_0_log.json      # First generation's thoughts
├── generation_1_log.json      # Second generation's thoughts
├── ...
└── run_summary.json           # Complete summary
```

### Log File Contents

Each `generation_N_log.json` contains:

```json
{
  "generation": 0,
  "capabilities": ["planning", "execution"],
  "autonomy_level": 3,
  "thought_log": [
    {
      "timestamp": "2025-11-13T10:30:00",
      "thought_type": "planning_start",
      "content": "Starting to plan...",
      "metadata": {}
    }
  ]
}
```

### Run Summary

The `run_summary.json` includes:
- All generations' data
- Complete evolution timeline
- Performance metrics
- Full thought logs

## Example: Specific Task

Let's run with a specific task:

```bash
python main.py \
  --generations 5 \
  --task "Design a system that can automatically refactor Python code"
```

Each generation will:
1. **Plan** how to approach the task
2. **Execute** the plan (simulated)
3. **Design** a better agent for the next iteration

You'll see capabilities evolve from basic planning to advanced code analysis, refactoring strategies, and autonomous decision-making.

## Understanding Evolution

### Generation 0
- **Autonomy**: 1/10
- **Capabilities**: `basic_planning`, `self_analysis`
- **Behavior**: Simple, reactive

### Generation 2
- **Autonomy**: 4/10
- **Capabilities**: `planning`, `execution`, `learning`, `code_analysis`
- **Behavior**: More sophisticated reasoning

### Generation 5
- **Autonomy**: 8/10
- **Capabilities**: `advanced_planning`, `autonomous_execution`, `meta_learning`, `code_generation`, `optimization`, `self_modification`
- **Behavior**: Highly autonomous, complex decision-making

## Tips

### Cost Management

Each generation makes ~2-3 API calls. Estimate costs:
- 5 generations ≈ 15 API calls
- 10 generations ≈ 30 API calls

### Rate Limits

The system includes 1-second delays between generations to respect rate limits.

### Customization

Edit `src/agent.py` to customize:
- Initial capabilities
- Planning prompts
- Improvement criteria

### Debugging

If something goes wrong:
1. Check `.env` has your API key
2. Look at the most recent generation log
3. Run tests: `pytest tests/ -v`

## Next Steps

1. **Experiment** with different tasks
2. **Analyze** the evolution patterns
3. **Customize** the agent capabilities
4. **Extend** with real execution (carefully!)

## Common Issues

### "ANTHROPIC_API_KEY must be set"

Solution: Create `.env` file with your API key

### Tests failing

If API-dependent tests fail without a key, that's expected. Unit tests should still pass.

### Rate limits

If you hit rate limits, reduce `--generations` or add delays in `src/runner.py`

## Learn More

- Full documentation: [README.md](README.md)
- Architecture details: [src/agent.py](src/agent.py)
- Test examples: [tests/](tests/)

## Support

Questions or issues?
- Check the thought logs in `generations/`
- Review test suite for examples
- Open an issue on GitHub

Happy experimenting with recursive self-improvement!

#!/bin/bash
# Setup script for Recursive Self-Improving AI Agent System

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║  Recursive Self-Improving AI Agent System - Setup                 ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 is installed"
echo ""

# Create virtual environment (optional)
read -p "Create a virtual environment? (recommended) [Y/n]: " create_venv
create_venv=${create_venv:-Y}

if [[ $create_venv =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv

    if [ $? -eq 0 ]; then
        echo "✓ Virtual environment created"
        echo ""
        echo "To activate it, run:"
        echo "  source venv/bin/activate  # On Linux/Mac"
        echo "  venv\\Scripts\\activate     # On Windows"
        echo ""

        # Ask if user wants to activate now
        read -p "Activate virtual environment now? [Y/n]: " activate_now
        activate_now=${activate_now:-Y}

        if [[ $activate_now =~ ^[Yy]$ ]]; then
            source venv/bin/activate
            echo "✓ Virtual environment activated"
        fi
    else
        echo "❌ Failed to create virtual environment"
    fi
fi

echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Setup environment file
if [ ! -f .env ]; then
    echo "Setting up environment file..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    read -p "Enter your Anthropic API key (or press Enter to skip): " api_key

    if [ ! -z "$api_key" ]; then
        echo "ANTHROPIC_API_KEY=$api_key" > .env
        echo "✓ API key saved to .env"
    else
        echo "⚠️  Remember to add your API key to .env before running"
    fi
else
    echo "✓ .env file already exists"
fi

echo ""

# Run tests
read -p "Run tests to verify installation? [Y/n]: " run_tests
run_tests=${run_tests:-Y}

if [[ $run_tests =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running tests..."
    pytest -v

    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ All tests passed!"
    else
        echo ""
        echo "⚠️  Some tests failed (this might be due to missing API key for integration tests)"
    fi
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║  Setup Complete!                                                   ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Ensure your ANTHROPIC_API_KEY is set in .env"
echo "2. Run the system:"
echo "   python main.py --generations 5"
echo ""
echo "3. Analyze results:"
echo "   python analyze_run.py"
echo ""
echo "For help:"
echo "   python main.py --help"
echo ""

# Gamma Coder - Generation 1
# Strategy: robust
# Score: 90.71253967285156

# Generation 1 - Enhanced with robust approach

def process(data: list) -> list:
    """Process data with improved efficiency."""
    return [item * 2 for item in data if isinstance(item, (int, float)) and item % 2 == 0]
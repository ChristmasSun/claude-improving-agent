# Gamma Coder - Generation 0
# Strategy: robust
# Score: 89.47276306152344

def process(data):
    """Process data robustly."""
    try:
        result = []
        if not isinstance(data, list):
            return []
        for item in data:
            if isinstance(item, (int, float)) and item % 2 == 0:
                result.append(item * 2)
        return result
    except Exception as e:
        return []
# Alpha Coder - Generation 0
# Strategy: efficient
# Score: 82.23570251464844

def process(data):
    """Process data efficiently."""
    result = []
    for item in data:
        if item % 2 == 0:
            result.append(item * 2)
    return result
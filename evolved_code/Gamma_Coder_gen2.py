# Gamma Coder - Generation 2
# Strategy: robust
# Score: 98.56948852539062

# Generation 2 - Enhanced with robust approach

from functools import lru_cache
from typing import List, Union

@lru_cache(maxsize=128)
def _cached_double(item: Union[int, float]) -> Union[int, float]:
    """Cache doubled values for efficiency."""
    return item * 2

def process(data: List[Union[int, float]]) -> List[Union[int, float]]:
    """Process data with caching and type safety."""
    if not isinstance(data, list):
        return []
    return [_cached_double(item) for item in data if isinstance(item, (int, float)) and item % 2 == 0]
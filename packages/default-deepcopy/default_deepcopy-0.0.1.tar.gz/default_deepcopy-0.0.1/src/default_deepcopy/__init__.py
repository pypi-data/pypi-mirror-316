from copy import deepcopy
from typing import Any

def default_deepcopy(
    value: Any,
    default: Any = None        
) -> Any:
    """
    deepcopy, but if there are exceptions, return a default value

    Args:
        value (Any): value to deep copy
        default (Any): default value to return if exception happens during deepcopy
    
    Returns:
        (Any) deepcopied value 
    """
    try:
        return deepcopy(value)
    except:
        return default

""" An example Python module """
from typing import List

def total(xs:List[float]) -> float:
    """ Total returns the sum of xs. """
    result: float = 0.0
    # For each x float in xs, add it to result
    for x in xs:
        result += x
    return result

def join(xs:List[int], delimiter: str) -> str:
    """Given list of integers and delimiter returns string of integers 
    from a list concatenated with delimiter"""
    result: str = ""
    if len(xs) == 1:
        return str(xs[0])
    elif len(xs) > 1:
        for x in xs:
            result += str(x) + delimiter
    return result.rstrip(delimiter)
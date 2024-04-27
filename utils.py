"""
Just some simple utiliy functions.

We compute and cache some factorials and powers of 6 for fast retrieval.
"""

FACTORIALS_ = [prev_ := 1 if not i else i * prev_ for i in range(14)]

def factorial(n):
    """Return the factorial of n (up to n = 13)."""
    return FACTORIALS_[n]

POWERS_6_ = [prev_ := 1 if not i else 6 * prev_ for i in range(9)]

def power_6(n):
    """Return 6^n (up to n = 8)."""
    return POWERS_6_[n]

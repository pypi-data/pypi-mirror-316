from typing import List, Callable, Any, Dict
import cmath  # For handling complex numbers in case of negative numbers
import math


def divide_list(data: List[Any], conditions: Dict[str, Callable[[Any], bool]]) -> Dict[str, List[Any]]:
    """
    Divides a list into multiple groups based on user-defined conditions.

    Args:
        data: The input list of items.
        conditions: A dictionary where the keys are the names of the conditions and the values are the condition functions.

    Returns:
        A dictionary where keys are the condition names, and values are lists of items that satisfy the respective condition.

    Raises:
        ValueError: If no conditions are provided.
    """
    if not conditions:
        raise ValueError("At least one condition must be provided.")
    
    # Initialize groups for each condition
    groups = {name: [] for name in conditions}
    ungrouped = []

    for item in data:
        matched = False
        # Check each condition for the current item
        for name, condition in conditions.items():
            if condition(item):  # If the condition is met
                groups[name].append(item)  # Add item to the respective group
                matched = True

        # If no condition matched, add the item to 'Ungrouped'
        if not matched:
            ungrouped.append(item)

    # Ensure the 'Ungrouped' key exists even if it's empty
    if ungrouped:
        groups["Ungrouped"] = ungrouped
    else:
        groups["Ungrouped"] = []

    return groups


# Predefined condition functions with user input
def is_greater_than(user_number: int):
    """Returns a function that checks if a number is greater than the user's number."""
    def check_greater(x):
        return x > user_number
    return check_greater

def is_divisible_by(user_number: int):
    """Returns a function that checks if a number is divisible by the user's number."""
    def check_divisibility(x):
        return x % user_number == 0
    return check_divisibility

def is_multiple_of(user_number: int):
    """Returns a function that checks if a number is a multiple of the user's number."""
    def check_multiple(x):
        return x % user_number == 0
    return check_multiple

def is_power_of_x(user_number: int):
    """Returns a function that checks if a number is a power of the user's number."""
    def check_power_of(x):
        if user_number == 1:
            return x == 1  # Any number to the power of 0 is 1, so for base 1, x should be 1.
        if user_number == 0:
            return x == 0  # Power of 0 is 0
        return x > 0 and (pow(user_number, int(round(cmath.log(x, user_number).real))) == x)
    return check_power_of


# Predefined condition functions
def is_even(x):
    """Returns True if x is an even number."""
    if not isinstance(x, (int, float)):  # Ensure it's numeric
        return False
    return x % 2 == 0

def is_odd(x):
    """Returns True if x is an odd number."""
    return x % 2 != 0

def is_positive(x):
    """Returns True if x is a positive number."""
    return x > 0

def is_negative(x):
    """Returns True if x is a negative number."""
    return x < 0


def is_prime(x):
    """Returns True if x is a prime number."""
    if not isinstance(x, int):  # Ensure it's an integer
        return False
    if x <= 1:
        return False
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            return False
    return True

def is_perfect_square(x):
    """Returns True if x is a perfect square."""
    if isinstance(x, complex):  # Handle complex numbers separately
        return False
    
    if x < 0:  # Negative numbers cannot be perfect squares in the real number system
        return False
    
    sqrt_x = math.sqrt(x)  # Use math.sqrt for non-negative real numbers
    return sqrt_x.is_integer()  # Check if the square root is an integer


def is_perfect_cube(x):
    if isinstance(x, complex):
        return False  # Complex numbers can't be perfect cubes in real terms
    if x == 0:
        return True
    if x < 0:
        cube_root = cmath.exp(cmath.log(abs(x)) / 3)
        return round(-cube_root.real) ** 3 == x
    else:
        cube_root = cmath.exp(cmath.log(x) / 3)
        return round(cube_root.real) ** 3 == x


def is_fibonacci(x):
    """Returns True if x is a Fibonacci number."""
    if isinstance(x, complex):  # Ignore complex numbers
        return False
    if x < 0:
        return False
    # A number is Fibonacci if one of 5*n^2 + 4 or 5*n^2 - 4 is a perfect square
    return is_perfect_square(5*x**2 + 4) or is_perfect_square(5*x**2 - 4)


def is_even_length(x):
    """Returns True if the length of the number (as a string) is even."""
    return len(str(abs(x))) % 2 == 0

def is_odd_length(x):
    """Returns True if the length of the number (as a string) is odd."""
    return len(str(abs(x))) % 2 != 0

def is_integer(x):
    """Returns True if x is an integer."""
    return isinstance(x, int)

def is_float(x):
    """Returns True if x is a float."""
    return isinstance(x, float)

def is_zero(n):
    return n == 0 and isinstance(n, int)


def is_palindrome(x):
    """Returns True if the number is a palindrome (same forward and backward)."""
    return str(x) == str(x)[::-1]

def is_ascending_digits(x):
    """Returns True if the digits of the number are in ascending order."""
    digits = str(abs(x))
    return all(digits[i] <= digits[i+1] for i in range(len(digits)-1))


# Additional condition functions
def is_less_than(user_number: int):
    """Returns a function that checks if a number is less than the user's number."""
    def check_less(x):
        return x < user_number
    return check_less

def is_equal_to(user_number: int):
    """Returns a function that checks if a number is equal to the user's number."""
    def check_equal(x):
        return x == user_number
    return check_equal

def is_not_equal_to(user_number: int):
    """Returns a function that checks if a number is not equal to the user's number."""
    def check_not_equal(x):
        return x != user_number
    return check_not_equal

def is_between_range(min_value: int, max_value: int):
    """Returns a function that checks if a number is between a given range (inclusive)."""
    def check_range(x):
        return min_value <= x <= max_value
    return check_range


def is_multiple_of_any(numbers: List[int]):
    """Returns a function that checks if a number is divisible by any of the given numbers."""
    def check_multiple_any(x):
        return any(x % num == 0 for num in numbers)
    return check_multiple_any

def is_square_root_integer(x):
    """Returns True if the square root of x is an integer and x is a real number."""
    if isinstance(x, complex):  # Ignore complex numbers
        return False
    if x < 0:  # Check if the number is negative
        return False  # Negative numbers can't have integer square roots in the real number system
    return int(x**0.5) ** 2 == x  # For non-negative real numbers, check if the square root is an integer



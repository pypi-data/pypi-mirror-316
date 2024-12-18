import unittest
from logicchunks.lists import *
import time

class TestLogicChunks(unittest.TestCase):

    def test_divide_list(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8]
        
        # Define conditions
        conditions = {
            "Greater than 3": is_greater_than(3),
            "Divisible by 2": is_divisible_by(2),
            "Even": is_even,
            "Odd": is_odd
        }

        # Call the function
        result = divide_list(data, conditions)
        
        # Test if the grouping is correct
        self.assertIn("Greater than 3", result)
        self.assertIn("Divisible by 2", result)
        self.assertIn("Even", result)
        self.assertIn("Odd", result)
        self.assertIn("Ungrouped", result)  # Ungrouped items should always exist
        
        # Test specific conditions
        self.assertEqual(len(result["Greater than 3"]), 5)
        self.assertEqual(len(result["Divisible by 2"]), 4)
        self.assertEqual(len(result["Even"]), 4)
        self.assertEqual(len(result["Odd"]), 4)
        
        # Test ungrouped items (those that do not meet any condition)
        self.assertEqual(result["Ungrouped"], [])

    def test_is_greater_than(self):
        condition = is_greater_than(5)
        self.assertTrue(condition(6))
        self.assertFalse(condition(5))
        self.assertFalse(condition(4))

    def test_is_divisible_by(self):
        condition = is_divisible_by(3)
        self.assertTrue(condition(9))
        self.assertFalse(condition(10))

    def test_is_even(self):
        self.assertTrue(is_even(2))
        self.assertFalse(is_even(3))

    def test_is_odd(self):
        self.assertFalse(is_odd(2))
        self.assertTrue(is_odd(3))

    def test_is_prime(self):
        self.assertTrue(is_prime(5))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(-7))

    def test_is_perfect_square(self):
        self.assertTrue(is_perfect_square(16))
        self.assertFalse(is_perfect_square(20))
        self.assertFalse(is_perfect_square(-4))

    def test_is_perfect_cube(self):
        self.assertTrue(is_perfect_cube(8))
        self.assertFalse(is_perfect_cube(10))

    def test_is_fibonacci(self):
        self.assertTrue(is_fibonacci(5))
        self.assertFalse(is_fibonacci(6))

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome(121))
        self.assertFalse(is_palindrome(123))

    def test_is_ascending_digits(self):
        self.assertTrue(is_ascending_digits(123))
        self.assertFalse(is_ascending_digits(321))

    def test_is_integer(self):
        self.assertTrue(is_integer(3))
        self.assertFalse(is_integer(3.5))

    def test_is_float(self):
        self.assertTrue(is_float(3.5))
        self.assertFalse(is_float(3))

    def test_is_zero(self):
        self.assertTrue(is_zero(0))
        self.assertFalse(is_zero(1))

    def test_is_less_than(self):
        condition = is_less_than(5)
        self.assertTrue(condition(4))
        self.assertFalse(condition(6))

    def test_is_equal_to(self):
        condition = is_equal_to(5)
        self.assertTrue(condition(5))
        self.assertFalse(condition(6))

    def test_is_not_equal_to(self):
        condition = is_not_equal_to(5)
        self.assertTrue(condition(6))
        self.assertFalse(condition(5))

    def test_is_between_range(self):
        condition = is_between_range(3, 7)
        self.assertTrue(condition(5))
        self.assertFalse(condition(2))
        self.assertFalse(condition(8))

    def test_is_multiple_of_any(self):
        condition = is_multiple_of_any([2, 3])
        self.assertTrue(condition(6))
        self.assertFalse(condition(7))

    def test_is_square_root_integer(self):
        self.assertTrue(is_square_root_integer(16))
        self.assertFalse(is_square_root_integer(18))
        self.assertFalse(is_square_root_integer(-4))


    def test_divide_list_empty(self):
        data = []
        conditions = {
            "Greater than 3": is_greater_than(3),
            "Divisible by 2": is_divisible_by(2)
        }

        result = divide_list(data, conditions)
        
        self.assertIn("Greater than 3", result)
        self.assertIn("Divisible by 2", result)
        self.assertIn("Ungrouped", result)
        self.assertEqual(result["Greater than 3"], [])
        self.assertEqual(result["Divisible by 2"], [])
        self.assertEqual(result["Ungrouped"], [])

    def test_is_less_than_boundary(self):
        condition = is_less_than(5)
        self.assertTrue(condition(4))
        self.assertFalse(condition(5))
        self.assertFalse(condition(6))

    def test_is_between_range_boundary(self):
        condition = is_between_range(3, 7)
        self.assertTrue(condition(3))
        self.assertTrue(condition(7))
        self.assertFalse(condition(2))
        self.assertFalse(condition(8))

    def test_performance_divide_list_large(self):
        data = list(range(1, 10**6))
        conditions = {
            "Greater than 500,000": is_greater_than(500000),
            "Divisible by 2": is_divisible_by(2),
            "Even": is_even,
            "Odd": is_odd
        }

        start_time = time.time()
        result = divide_list(data, conditions)
        end_time = time.time()

        self.assertIn("Greater than 500,000", result)
        self.assertIn("Divisible by 2", result)
        self.assertIn("Even", result)
        self.assertIn("Odd", result)
        self.assertIn("Ungrouped", result)

        self.assertTrue(end_time - start_time < 2)

    def test_is_perfect_square_complex(self):
        self.assertFalse(is_perfect_square(4 + 3j))

    def test_is_perfect_cube_complex(self):
        self.assertFalse(is_perfect_cube(4 + 3j))

    def test_is_fibonacci_complex(self):
        self.assertFalse(is_fibonacci(4 + 3j))

    def test_is_square_root_integer_complex(self):
        self.assertFalse(is_square_root_integer(4 + 3j))

    def test_is_even_with_string(self):
        self.assertFalse(is_even("hello"))

    def test_is_prime_with_string(self):
        self.assertFalse(is_prime("hello"))

    def test_is_zero_with_float(self):
        self.assertFalse(is_zero(0.0))

    def test_is_prime_zero(self):
        self.assertFalse(is_prime(0))

    def test_is_prime_negative(self):
        self.assertFalse(is_prime(-5))

    def test_is_square_root_integer_zero(self):
        self.assertTrue(is_square_root_integer(0))

    def test_is_square_root_integer_negative(self):
        self.assertFalse(is_square_root_integer(-16))

    def test_is_ascending_digits_negative(self):
        self.assertFalse(is_ascending_digits(-321))

if __name__ == '__main__':
    unittest.main()

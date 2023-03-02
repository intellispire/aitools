import sys
sys.path.append('..')

import unittest
from aitools.utils import create_prompt_from_string, create_prompt_from_file, create_prompt, estimate_tokens

class TestEstimateTokens(unittest.TestCase):
    def test_estimate_tokens(self):
        text = "This is a test sentence."
        expected_token_count = 6
        self.assertEqual(estimate_tokens(text), expected_token_count)

        text = "This is another test sentence with more tokens."
        expected_token_count = 9
        self.assertEqual(estimate_tokens(text), expected_token_count)

        text = "And a third test, for good measure."
        expected_token_count = 9
        self.assertEqual(estimate_tokens(text), expected_token_count)

class TestCreatePrompt(unittest.TestCase):

    def test_create_prompt_from_file_replaces_values(self):
        # Define test data
        template = "hello"
        data = {"name": "John"}

        # Call the function
        result = create_prompt_from_file(template, data)

        # Check the result
        self.assertEqual(result, "Hello John!\n")

    def test_create_prompt_from_file_replaces_values_local(self):
        # Define test data
        template = "hello_local"
        data = {"name": "John"}

        # Call the function
        result = create_prompt(template, data)

        # Check the result
        self.assertEqual(result, "Hello John!\n")

    def test_create_prompt_replaces_values_string(self):
        # Define test data
        template = "Hello <<NAME>>!"
        data = {"name": "John"}

        # Call the function
        result = create_prompt(template, data)

        # Check the result
        self.assertEqual(result, "Hello John!")

    def test_create_prompt_replaces_values(self):
        # Define test data
        template = "Hello <<NAME>>!"
        data = {"name": "John"}

        # Call the function
        result = create_prompt_from_string(template, data)

        # Check the result
        self.assertEqual(result, "Hello John!")

    def test_create_prompt_handles_missing_values(self):
        # Define test data
        template = "Hello <<NAME>>! You are <<AGE>> years old."
        data = {"name": "John"}

        # Call the function
        result = create_prompt_from_string(template, data)

        # Check the result
        self.assertEqual(result, "Hello John! You are <<AGE>> years old.")

    def test_create_prompt_handles_extra_values(self):
        # Define test data
        template = "Hello <<NAME>>!"
        data = {"name": "John", "age": 30}

        # Call the function
        result = create_prompt_from_string(template, data)

        # Check the result
        self.assertEqual(result, "Hello John!")


if __name__ == '__main__':
    unittest.main()

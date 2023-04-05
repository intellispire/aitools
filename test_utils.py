import sys
sys.path.append('..')

import unittest
from aitools.utils import create_prompt_from_string, create_prompt_from_file, create_prompt, estimate_tokens, parse_prompt, estimate_tokens_real

class TestEstimateTokens(unittest.TestCase):
    def test_estimate_tokens_real(self):
        text = "This is a test sentence."
        expected_token_count = 6
        self.assertEqual(estimate_tokens_real(text), expected_token_count)

        text = "This is another test sentence with more tokens."
        expected_token_count = 9
        self.assertEqual(estimate_tokens_real(text), expected_token_count)

        text = "And a third test, for good measure."
        expected_token_count = 9
        self.assertEqual(estimate_tokens_real(text), expected_token_count)

    def test_estimate_tokens(self):
        text = "This is a test sentence."
        expected_token_count = 7
        self.assertEqual(estimate_tokens(text), expected_token_count)

        text = "This is another test sentence with more tokens."
        expected_token_count = 10
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
        template = "hello.txt"
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


    def test_split_chatgpt_prompt(self):
        prompt1 = "Lorem ipsum dolor sit amet,\n\nconsectetur adipiscing elit.\n\nSed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        result1 = parse_prompt(prompt1)
        assert result1 == {'full_document': prompt1, 'system': '', 'prompt': prompt1}, f"Test case 1 failed: expected {result1}, but got {split_chatgpt_prompt(prompt1)}"

        prompt3 = "SYSTEM: This is the system text.\n\nLorem ipsum dolor sit amet,\n\nconsectetur adipiscing elit.\n\nSed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        document3 = prompt3.replace("SYSTEM:", "").lstrip()
        result3 = parse_prompt(prompt3)
        expected_result3 = {'full_document': document3, 'system': 'This is the system text.', 'prompt': prompt3.replace("SYSTEM: This is the system text.\n\n", '')}
        assert result3 == expected_result3, f"Test case 3 failed: expected {expected_result3}, but got {result3}"

#         prompt4 = "SYSTEM:\n\nLorem ipsum dolor sit amet,\n\nconsectetur adipiscing elit.\n\nSed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
#         result4 = split_chatgpt_prompt(prompt4)
#         expected_result4 = {'full_document': prompt1, 'system': '', 'prompt': prompt1}
#         expected_result4['full_document'] = result4['full_document']
#         expected_result4['prompt'] = result4['prompt']
#         assert result4 == expected_result4, f"Test case 4 failed: expected {expected_result4}, but got {result4}"

        prompt5 = "Lorem ipsum dolor sit amet,\n\nconsectetur adipiscing elit.\n\nSed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n\n"
        result5 = parse_prompt(prompt5)
        assert result5 == {'full_document': prompt5.strip(), 'system': '', 'prompt': prompt5.strip()}, f"Test case 5 failed: expected {result5}, but got {split_chatgpt_prompt(prompt5)}"

        prompt6 = "SYSTEM: This is the system text.\nwhich continues on\nmultiple lines.\n\nAnd this is the actual prompt text."
        result6 = parse_prompt(prompt6)
        expected_result6 = {'full_document': "This is the system text.\nwhich continues on\nmultiple lines.\n\nAnd this is the actual prompt text.", 'system': 'This is the system text.\nwhich continues on\nmultiple lines.', 'prompt': 'And this is the actual prompt text.'}
        assert result6 == expected_result6, f"Test case 6 failed: expected {expected_result6}, but got {result6}"

        print("All test cases pass")


if __name__ == '__main__':
    unittest.main()

import sys
sys.path.append('..')

import unittest
from aitools.pdf2txt import convert_pdf_to_txt

class TestProcessPDF(unittest.TestCase):
    def test_process_pdf_empty_file(self):
        # Create an empty PDF file for testing
        pdf_file = 'data/hello-world.pdf'

        # Call the process_pdf function with the empty PDF file
        result = convert_pdf_to_txt(pdf_file)

        # Check that the result is an empty string
        self.assertEqual(result, 'hello world\n\n\x0c')

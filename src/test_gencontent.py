import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_extract_heading(self):
        md = """
# Heading
dummy text
"""
        extracted = extract_title(md)
        self.assertEqual(extracted, "Heading")
        
    def test_no_heading(self):
        md = """
text with no heading to be found
"""
        extracted = extract_title(md)
        with self.assertRaises(ValueError):
            extract_title(md)
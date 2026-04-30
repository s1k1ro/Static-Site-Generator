import unittest

from gencontent import extract_title


class TestGenContent(unittest.TestCase):

    def test_ET_one_heading(self):
        markdown = "# Hello"
        result = extract_title(markdown)
        self.assertEqual(result, "Hello")
    
    def test_ET_exception_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("no heading here")
    
    def test_ET_H1_not_on_first_line(self):
        md = """
This is not a heading
# The Heading
"""
        result = extract_title(md)
        self.assertEqual(result, "The Heading")

if __name__ == "__main__":
    unittest.main()


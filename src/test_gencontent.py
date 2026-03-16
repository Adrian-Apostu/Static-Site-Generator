import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_with_multiple_words(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_markdown_no_title(self):
        markdown = "## Hello World"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()
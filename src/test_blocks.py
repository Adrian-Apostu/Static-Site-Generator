import unittest
from markdown_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("Just one paragraph"), ["Just one paragraph"])

    def test_strips_whitespace(self):
        md = "  hello  \n\n  world  "
        self.assertEqual(markdown_to_blocks(md), ["hello", "world"])

    def test_excess_newlines(self):
        md = "block one\n\n\n\nblock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["block one", "block two"])

    def test_only_whitespace_blocks_removed(self):
        md = "first\n\n   \n\nsecond"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["first", "second"])

    def test_headings_and_paragraphs(self):
        md = "# Heading\n\nSome text\n\n## Subheading"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading", "Some text", "## Subheading"])

if __name__ == "__main__":
    unittest.main()
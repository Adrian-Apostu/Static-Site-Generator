import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

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

class TestBlockToBlockType(unittest.TestCase):

    # Headings
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Hello"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Hello"), BlockType.HEADING)

    def test_heading_7_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Hello"), BlockType.PARAGRAPH)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#Hello"), BlockType.PARAGRAPH)

    # Code
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('hi')\n```"), BlockType.CODE)

    def test_code_block_multiline(self):
        self.assertEqual(block_to_block_type("```\nline 1\nline 2\n```"), BlockType.CODE)

    # Quote
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type(">line 1\n>line 2"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)

    def test_quote_missing_on_one_line(self):
        self.assertEqual(block_to_block_type(">line 1\nline 2"), BlockType.PARAGRAPH)

    # Unordered list
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)

    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- only item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)

    # Ordered list
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. only item"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        self.assertEqual(block_to_block_type("2. first\n3. second"), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_order(self):
        self.assertEqual(block_to_block_type("1. first\n3. second"), BlockType.PARAGRAPH)

    # Paragraph
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just some text"), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

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


    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_codeblock_structure(self):
        md = """```
hello
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<pre><code>", html)

    def test_ordered_list_must_start_at_one(self):
        """A list starting at 2 is not valid — should fall back to paragraph."""
        block = "2. first\n3. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_only_dash(self):
        """Only '- ' is supported as a list marker, not '* '."""
        block = "* item one\n* item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_blockquote_no_space_after_arrow(self):
        """>text with no space should still be treated as a quote."""
        md = ">no space"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>no space</blockquote></div>")

    def test_heading_with_inline_markdown(self):
        md = "# Hello **world**"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>Hello <b>world</b></h1></div>")

    def test_all_heading_levels_html_output(self):
        for level in range(1, 7):
            md = f"{'#' * level} Heading {level}"
            html = markdown_to_html_node(md).to_html()
            self.assertIn(f"<h{level}>Heading {level}</h{level}>", html)

    def test_heading_no_space_is_paragraph(self):
        md = "#nospace"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<p>", html)
        self.assertNotIn("<h1>", html)

    def test_unordered_list_inline_markdown(self):
        md = "- item with **bold**\n- plain item"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<b>bold</b>", html)

    def test_ordered_list_inline_markdown(self):
        md = "1. item with _italic_\n2. plain item"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<i>italic</i>", html)

    def test_single_item_unordered_list(self):
        md = "- only item"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ul><li>only item</li></ul></div>")

    def test_single_item_ordered_list(self):
        md = "1. only item"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><ol><li>only item</li></ol></div>")

    def test_blockquote_multiline_inline_markdown(self):
        md = "> some **bold** text\n> more text"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("more text", html)

    def test_blockquote_strip_behavior_consistent(self):
        """> text and >text should both produce the same inner content."""
        html_spaced = markdown_to_html_node("> hello").to_html()
        html_nospace = markdown_to_html_node(">hello").to_html()
        self.assertEqual(html_spaced, html_nospace)


    def test_single_line_code_fence_is_paragraph(self):
        """```code``` on one line — no newline inside, treat as paragraph."""
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_extra_blank_lines_full_pipeline(self):
        md = "paragraph one\n\n\n\nparagraph two"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><p>paragraph one</p><p>paragraph two</p></div>")

    def test_all_block_types_integration(self):
        md = """# Heading

A paragraph with **bold**.

```
code here
```

> a quote

- item one
- item two

1. first
2. second"""
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn("<p>A paragraph with <b>bold</b>.</p>", html)
        self.assertIn("<pre><code>code here\n</code></pre>", html)
        self.assertIn("<blockquote>a quote</blockquote>", html)
        self.assertIn("<ul><li>item one</li><li>item two</li></ul>", html)
        self.assertIn("<ol><li>first</li><li>second</li></ol>", html)

    def test_seven_hashes_is_paragraph(self):
        """####### is not a valid heading level — must fall back to paragraph."""
        block = "####### not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_six_hashes_is_valid_heading(self):
        block = "###### h6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

if __name__ == '__main__':
    unittest.main()
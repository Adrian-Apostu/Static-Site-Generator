import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextType, TextNode

class TestInlineMarkdown(unittest.TestCase):

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])


    def test_split_nodes_delimiter_multiple(self):
        node1 = TextNode("This is `code` here", TextType.TEXT)
        node2 = TextNode("And `more code` there", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("And ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" there", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_mixed(self):
        node1 = TextNode("Already bold", TextType.BOLD)
        node2 = TextNode("Text with `code` block", TextType.TEXT)
        
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        
        expected = [
            node1,
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_excludes_images(self):
        text = "This is a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://boot.dev")], matches)

    


if __name__ == "__main__":
    unittest.main()
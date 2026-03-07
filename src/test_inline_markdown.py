import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images(
            "This is text with an image"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        # Images
    def test_split_images_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("Just plain text", TextType.TEXT)], new_nodes)

    def test_split_images_single(self):
        node = TextNode("![alt](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_split_images_trailing_text(self):
        node = TextNode("![img](https://example.com/a.png) and some tail", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://example.com/a.png"),
                TextNode(" and some tail", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("Hello ![a](https://x.com/1.png) world", TextType.TEXT),
            TextNode("No images here", TextType.TEXT),
            TextNode("![b](https://x.com/2.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://x.com/1.png"),
                TextNode(" world", TextType.TEXT),
                TextNode("No images here", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "https://x.com/2.png"),
            ],
            new_nodes,
        )

    # Links
    def test_split_links(self):
        node = TextNode(
            "This has a [link](https://boot.dev) and [another](https://example.com) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This has a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.LINK, "https://example.com"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("No links at all", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("No links at all", TextType.TEXT)], new_nodes)

    def test_split_links_single(self):
        node = TextNode("[click](https://boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("click", TextType.LINK, "https://boot.dev")],
            new_nodes,
        )

    def test_split_links_trailing_text(self):
        node = TextNode("[go](https://x.com) then read more", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("go", TextType.LINK, "https://x.com"),
                TextNode(" then read more", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("A [link](https://a.com) B", TextType.TEXT),
            TextNode("Plain text", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("A ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://a.com"),
                TextNode(" B", TextType.TEXT),
                TextNode("Plain text", TextType.TEXT),
            ],
            new_nodes,
        )
    


if __name__ == "__main__":
    unittest.main()
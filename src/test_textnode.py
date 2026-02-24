import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "BOLD")
        node2 = TextNode("This is a text node", "BOLD")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "BOLD")
        node2 = TextNode("This is another text node", "BOLD", "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", "BOLD")
        self.assertEqual(repr(node), "TextNode(This is a text node, **Bold text**, None)")


if __name__ == "__main__":
    unittest.main()
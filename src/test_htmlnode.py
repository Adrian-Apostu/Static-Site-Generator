import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_repr_(self):
        node = HtmlNode("div", "This is a div", None, {"class": "test"})
        self.assertEqual(repr(node), "div, This is a div, None, {'class': 'test'}")

    def test_to_html_raises(self):
        node = HtmlNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HtmlNode(None, None, None, {"class": "test", "href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' class="test" href="https://www.boot.dev"')

    def test_repr_with_props(self):
        node = HtmlNode("div", "This is a div", None, {"class": "test"})
        self.assertEqual(repr(node), "div, This is a div, None, {'class': 'test'}")

    def test_repr_with_children(self):
        children = [HtmlNode("div", "This is a child div", None, {"class": "child"}), HtmlNode("p", "This is a child p", None, {"class": "child"})]
        node = HtmlNode("div", "This is a div", children=children)
        self.assertEqual(repr(node), f'div, This is a div, {children}, None')

if __name__ == "__main__":
    unittest.main()
import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "p, Hello, world!, None")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_no_tag(self):
        child_node = LeafNode(None, "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_plain_text_child(self):
        child1 = LeafNode("span", "child1")
        child2 = LeafNode("span", "child2")
        child3 = LeafNode(None, "child3")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span>child3</div>")

if __name__ == "__main__":
    unittest.main()
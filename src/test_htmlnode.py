import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_eq_false(self):
        node = HTMLNode("a", "Text")
        self.assertNotEqual(node.tag, "p")
        self.assertNotEqual(node.value, "Test")

    def test_prop_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode("a", "Paragraph text", [HTMLNode()], {"href": "https://www.google.com"})
        self.assertEqual(node.__repr__(), "HTMLNode(a, Paragraph text, [HTMLNode(None, None, None, None)], {'href': 'https://www.google.com'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_url(self):
        node = LeafNode("a", "Click!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(node.to_html(), "Hello")

    def test_parent_to_html_p_b_a(self):
        node = ParentNode(
            "p",[
                LeafNode("b", "Bold text"),
                LeafNode("a", "Click!", {"href": "https://www.google.com"}),
            ],
            )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b><a href="https://www.google.com">Click!</a></p>')

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_a_p_prop(self):
        node = ParentNode(
            "a",
            [
                LeafNode("p", "Hello!"),
            ],
            {"href": "https://www.google.com"},
            )
        self.assertEqual(node.to_html(), '<a href="https://www.google.com"><p>Hello!</p></a>')




if __name__ == "__main__":
    unittest.main()

    
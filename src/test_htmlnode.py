import unittest
from htmlnode import HTMLNode, LeafNode

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


if __name__ == "__main__":
    unittest.main()

    
import unittest
from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplit(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("Text is **bold** now", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        return self.assertEqual([
            TextNode("Text is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" now", TextType.TEXT)
        ], new_nodes)
    
    def test_split_multi_code(self):
        node = TextNode("Text `code` here, then `more code` there, it is `coding` everywhere", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        return self.assertEqual([
            TextNode("Text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here, then ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" there, it is ", TextType.TEXT),
            TextNode("coding", TextType.CODE),
            TextNode(" everywhere", TextType.TEXT)
        ], new_nodes)
    
    def test_split_multinodes(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        node2 = TextNode("Also _italic_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        return self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
                TextNode("Also ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" here", TextType.TEXT)
            ], new_nodes)
    
    def test_bold_first_ita_last(self):
        node = TextNode("**bold** text _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        next_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        return self.assertEqual([
            TextNode("bold", TextType.BOLD),
            TextNode(" text ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ], next_nodes)


if __name__ == "__main__":
    unittest.main()
 
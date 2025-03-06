import unittest
from markdown_blocknodes import markdown_to_blocks, block_to_blocktype, BlockType


class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype(self):
        block = "# heading"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
        block = "## heading2"
        self.assertEqual(block_to_blocktype(block), BlockType.HEADING)
        block = "```\ncode\ncode\n```"
        self.assertEqual(block_to_blocktype(block), BlockType.CODE)
        block = "> quote\n> another quote"
        self.assertEqual(block_to_blocktype(block), BlockType.QUOTE)
        block = "- ul\n- ul2"
        self.assertEqual(block_to_blocktype(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. list2"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)
        block = "1. list\n2. list2\n3. a\n4. b\n5. c\n6. d\n7. e\n8. e\n9. f\n10. g"
        self.assertEqual(block_to_blocktype(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_blocktype(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
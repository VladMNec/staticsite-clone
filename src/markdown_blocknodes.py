from enum import Enum
from htmlnode import LeafNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_blocktype(block):
    ordered_start = 1
    lines = block.split("\n")
    gen_par = tuple(["#" * i + " " for i in range(1, 7)])
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # Check ul block
    if lines[0].startswith("- "):
        for line in lines[1:]:
            if line.startswith("- "):
                continue
            return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    # Check quote block
    if lines[0].startswith("> "):
        for line in lines[1:]:
            if line.startswith("> "):
                continue
            return BlockType.PARAGRAPH
        return BlockType.QUOTE
    # Check if it's a complete code block
    if lines[0].startswith("```") and lines[-1] == "```" and len(lines) > 1:
            return BlockType.CODE
    # Check if ordered list in incremental order
    if lines[0].startswith(f"{ordered_start}. "):
        for line in lines[1:]:
            ordered_start += 1
            if line.startswith(f"{ordered_start}. "):
                continue
            return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    if len(markdown) == 0:
        raise Exception("empty string, nothing to convert")
    # Split string into markdown blocks and strip empty spaces at the start and end
    split_block = markdown.split("\n\n")
    split_block = [block.strip() for block in split_block if len(block.strip())]
    return split_block

from markdown_blocknodes import BlockType, markdown_to_blocks, block_to_blocktype
from htmlnode import ParentNode
from splitnodes import text_to_textnodes
from textnode import TextNode, TextType


# 1. convert markdown to block
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children).to_html()
    
# 2. check type of block
def block_to_html_node(block):
    if block_to_blocktype(block) == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_to_blocktype(block) == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_to_blocktype(block) == BlockType.UNORDERED_LIST:
        return ul_to_html_node(block)
    
# 3. make text into html nodes    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node.text_node_to_html_node()
        children.append(html_node)
    return children

# 4. paragraph func
def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

# 5. heading func
def heading_to_html_node(block):
    count = 0
    for mark in block:
        if mark == "#":
            count += 1
        else:
            break
    children = text_to_children(block.strip("# "))
    return ParentNode(f"h{count}", children)

# 6. unordered list func    
def ul_to_html_node(block):
    lines = block.split("\n")
    children = [ParentNode("li", text_to_children(line.strip("- "))) for line in lines]
    return ParentNode("ul", children)

# 7. ordered list func
# 8. quote func

# working test
# md = """
# - a
# - b
# """
# print(markdown_to_html_node(md))
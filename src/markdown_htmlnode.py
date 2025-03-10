from markdown_blocknodes import BlockType, markdown_to_blocks, block_to_blocktype
from htmlnode import ParentNode
from splitnodes import text_to_textnodes
from textnode import TextNode, TextType
import re


# 1. convert markdown to block
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
    
# 2. check type of block
def block_to_html_node(block):
    if block_to_blocktype(block) == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_to_blocktype(block) == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_to_blocktype(block) == BlockType.UNORDERED_LIST:
        return ul_to_html_node(block)
    if block_to_blocktype(block) == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_to_blocktype(block) == BlockType.CODE:
        return code_to_html_node(block)
    if block_to_blocktype(block) == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block")
    
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

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = raw_text_node.text_node_to_html_node()
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


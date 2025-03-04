from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = []
            current = node.text.split(delimiter)
            if len(current) % 2 == 0:
                raise Exception("missing delimiter")
            for i in range(len(current)):
                if i % 2 == 0 and current[i] != "":
                    split_node.append(TextNode(current[i], TextType.TEXT))
                elif i % 2 != 0 and current[i] != "":
                    split_node.append(TextNode(current[i], text_type))
            new_nodes.extend(split_node)
    return new_nodes


def extract_markdown_images(text):
    alt_matches = re.findall(r"\!\[(.*?)\]", text)
    src_matches = re.findall(r"\((.*?)\)", text)
    return list(zip(alt_matches, src_matches))

def extract_markdown_links(text):
    anchor_matches = re.findall(r"\[(.*?)\]", text)
    link_matches = re.findall(r"\((.*?)\)", text)
    return list(zip(anchor_matches, link_matches))



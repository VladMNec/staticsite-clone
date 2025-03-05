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
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Check if node is text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted_img = extract_markdown_images(node.text)

        # Check if there are any image markdowns
        if not extracted_img:
            new_nodes.append(node)
            continue
        alt_img, src_img = extracted_img[0]
        split_node = []

        # Split the text at first image
        splitting = node.text.split(f"![{alt_img}]({src_img})", 1)
        if len(splitting) != 2:
                raise ValueError("invalid markdown, image section not closed")
        # Check if there's text before the image
        if splitting[0].strip():
            split_node.append(TextNode(splitting[0], TextType.TEXT))
        split_node.append(TextNode(alt_img, TextType.IMAGE, src_img))

        # Recursively go over remaining text if there is any left
        remaining_node = splitting[1]
        if remaining_node:
            split_node.extend(split_nodes_image([TextNode(remaining_node, TextType.TEXT)]))
        new_nodes.extend(split_node)
    return new_nodes



def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        split_node = []
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            new_nodes.append(node)
            continue
        link_text, link_url = extracted_links[0]
        splitting = node.text.split(f"[{link_text}]({link_url})", 1)
        if len(splitting) != 2:
                raise ValueError("invalid markdown, link section not closed")
        if splitting[0].strip():
            split_node.append(TextNode(splitting[0], TextType.TEXT))
        split_node.append(TextNode(link_text, TextType.LINK, link_url))
        remaining_node = splitting[1]
        if remaining_node:
            split_node.extend(split_nodes_link([TextNode(remaining_node, TextType.TEXT)]))
        new_nodes.extend(split_node)
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_node = split_nodes_delimiter(new_node, "_", TextType.ITALIC)
    new_node = split_nodes_delimiter(new_node, "`", TextType.CODE)
    new_node = split_nodes_image(new_node)
    new_node = split_nodes_link(new_node)
    return new_node
    
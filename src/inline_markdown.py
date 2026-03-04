import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        node_strings = old_node.text.split(delimiter)
        if len(node_strings) % 2 == 0:
            raise Exception("Missing closing delimiter!")

        current_node_subnodes = []
        for i in range(len(node_strings)):
            if node_strings[i] == "":
                continue
            if i % 2 == 0:
                current_node_subnodes.append(TextNode(node_strings[i], TextType.TEXT))
            else:
                current_node_subnodes.append(TextNode(node_strings[i], text_type))
        new_nodes.extend(current_node_subnodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
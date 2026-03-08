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

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if images == []:
            new_nodes.append(old_node)
            continue

        for image in images:
            image_alt = image[0]
            image_link = image[1]
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if links == []:
            new_nodes.append(old_node)
            continue

        for link in links:
            link_alt = link[0]
            link_url = link[1]
            sections = original_text.split(f"[{link_alt}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    initial_node = [TextNode(text, TextType.TEXT)]
    result = split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(initial_node, "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)
        ))
    return result
import re
from enum import Enum
from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            filtered_blocks.append(block)
    return filtered_blocks

def is_ordered_list(lines):
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            return False
    return True

def block_to_block_type(block):
    lines = block.split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```") and "\n" in block:
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST

    if is_ordered_list(lines):
        return BlockType.OLIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        content = " ".join(block.split("\n"))
        return ParentNode("p", text_to_children(content))
    
    if block_type == BlockType.HEADING:
        level = len(re.match(r"^(#+) ", block).group(1))
        content = block[level + 1:]
        children = text_to_children(content)
        return ParentNode(f"h{level}", children)

    if block_type == BlockType.CODE:
        if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("invalid code block")
        text = block[4:-3]
        raw_text_node = TextNode(text, TextType.TEXT)
        child = text_node_to_html_node(raw_text_node)
        code = ParentNode("code", [child])
        return ParentNode("pre", [code])

    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        return ParentNode("blockquote", children)

    if block_type == BlockType.ULIST:
        items = []
        for line in block.split("\n"):
            content = line[2:]
            items.append(ParentNode("li", text_to_children(content)))
        return ParentNode("ul", items)

    if block_type == BlockType.OLIST:
        items = []
        for i, line in enumerate(block.split("\n")):
            content = line[len(f"{i + 1}. "):]
            items.append(ParentNode("li", text_to_children(content)))
        return ParentNode("ol", items)

    raise ValueError(f"Unknown block type: {block_type}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)

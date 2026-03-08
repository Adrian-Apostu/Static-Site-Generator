def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if len(block) > 0:
            filtered_blocks.append(block)
    return filtered_blocks
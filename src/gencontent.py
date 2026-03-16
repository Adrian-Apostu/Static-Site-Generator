def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            split_line = (line.split(" ", 1))
            return split_line[1]
    raise Exception("no title found")

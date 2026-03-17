import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            split_line = (line.split(" ", 1))
            return split_line[1]
    raise Exception("no title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown_content = file.read()
    with open(template_path) as file:
        template_content = file.read()
    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path): 
    for item in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, item)
        if os.path.isfile(current_path) and (Path(current_path).suffix == ".md"):
            new_path = Path(current_path).with_suffix(".html")
            generate_page(current_path, template_path, os.path.join(dest_dir_path, new_path.name))
        elif not os.path.isfile(current_path):
            new_dst = os.path.join(dest_dir_path, item)
            generate_pages_recursive(current_path, template_path, new_dst)

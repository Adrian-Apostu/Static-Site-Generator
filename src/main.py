import os
import shutil
from textnode import TextNode, TextType

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    for item in os.listdir(src):
        current_path=os.path.join(src, item)
        if os.path.isfile(current_path):
            shutil.copy(current_path, dst)
        else:
            new_dst = os.path.join(dst, item)
            copy_static(current_path, new_dst)

def main():
    copy_static("static", "public")


if __name__ == "__main__":
    main()
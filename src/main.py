import os
import shutil
from generate_page import generate_pages_recursively
from copystatic import copy_files_recursive
import sys


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
base_path = sys.argv[0]


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_pages_recursively(dir_path_content, "template.html", dir_path_public, base_path)


main()
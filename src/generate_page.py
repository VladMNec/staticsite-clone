from markdown_htmlnode import markdown_to_html_node
import os
import shutil

def extract_title(md):
    title = ""
    start_idx = md.find("<h1>")
    if start_idx != -1:
        end_idx = md.find("</h1>", start_idx)
        if end_idx != -1:
            title = "".join(md[start_idx+len("<h1>"):end_idx])
            return title
    raise Exception("missing title")
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from{from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_path_contents = "".join(f.readlines())
        f.close()
    with open(template_path, "r") as f:
        from_template_contents = "".join(f.readlines())
        f.close()
    from_path_to_html = markdown_to_html_node(from_path_contents).to_html()
    title = extract_title(from_path_to_html)
    from_template_contents = from_template_contents.replace("{{ Title }}", f"{ title }").replace("{{ Content }}", f"{from_path_to_html}")
    with open(dest_path, "a") as f:
        f.write(from_template_contents)

def generate_pages_recursively(dir_path_content, template_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_path)
        generate_page(from_path, template_path, dest_path)




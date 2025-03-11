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
    

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from{from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        from_path_contents = "".join(f.readlines())
        f.close()
    with open(template_path, "r") as f:
        from_template_contents = "".join(f.readlines())
        f.close()
    from_path_to_html = markdown_to_html_node(from_path_contents).to_html()
    title = extract_title(from_path_to_html)
    from_template_contents = from_template_contents.replace("{{ Title }}", f"{ title }").replace("{{ Content }}", f"{from_path_to_html}").replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(dest_path, "a") as f:
        f.write(from_template_contents)

def generate_pages_recursively(dir_path_content, template_path, dest_path, basepath):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    initial_path = dest_path
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(from_path):
            pre, ext = os.path.splitext(filename)
            dest_path = os.path.join(dest_path, f"{pre}.html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            dest_path = os.path.join(dest_path, filename)
            print(f"The filename: {filename}, from path: {from_path}, to path: {dest_path}")
            generate_pages_recursively(from_path, template_path, dest_path, basepath)
            dest_path = initial_path




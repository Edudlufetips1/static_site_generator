from markdown_blocks import markdown_to_html_node
import os
from pathlib import Path

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no header found")
        
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    file = open(from_path, "r")
    markdown_content = file.read()
    file.close()
    
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()  

    md_to_html_node = markdown_to_html_node(markdown_content)
    html = md_to_html_node.to_html()
    title = extract_title(markdown_content)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
    to_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)
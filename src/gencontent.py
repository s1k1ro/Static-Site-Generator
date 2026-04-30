import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path 


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()
        
    raise Exception("There is no h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #open the file in read mode ("r")
    md_file = open(from_path, "r")
    #read its entire contents nto a string
    md_contents = md_file.read()
    #close the md_file
    md_file.close()
    
    template_file = open(template_path, "r")
    template_contents = template_file.read()
    template_file.close()

    html_string = markdown_to_html_node(md_contents).to_html()
    title = extract_title(md_contents)

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_string)

    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    file = open(dest_path, "w")
    file.write(template_contents)
    file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        full_path = os.path.join(dir_path_content, item)
        dest_subdir = os.path.join(dest_dir_path,item)
        if os.path.isfile(full_path):
            dest_subdir_new = Path(dest_subdir).with_suffix(".html")            
            generate_page(full_path, template_path, dest_subdir_new)
        else:
            generate_pages_recursive(full_path, template_path, dest_subdir)




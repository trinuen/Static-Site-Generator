import os
import shutil
from markdown_to_html import markdown_to_html_node
from extract_markdown import extract_markdown_images, extract_markdown_links
def main():
  copy("../static", "../public")
  generate_pages_recursive("../content", "../template.html", "../public/")

def copy(src: str, dest: str):
  if not os.path.exists(src):
    return

  if os.path.exists(dest):
    shutil.rmtree(dest)
    
  shutil.copytree(src, dest)

def extract_title(markdown: str):
  if markdown.startswith("# "):
    return markdown.removeprefix("#").split("\n")[0].strip()
  raise Exception("No h1 found") 

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  if os.path.isfile(from_path) and os.path.isfile(template_path):
    with open(from_path, "r") as f:
      from_path_content = f.read()

    with open(template_path, "r") as f:
      template_path_content = f.read()

    content = markdown_to_html_node(from_path_content).to_html()
    title = extract_title(from_path_content)
    template_path_content = template_path_content.replace("{{ Title }}", title)
    template_path_content = template_path_content.replace("{{ Content }}", content)
    directories = extract_markdown_links(from_path_content)
    for directory in directories:
      if directory[1].startswith("/"):
        os.makedirs(os.path.dirname(dest_path) + directory[1], exist_ok=True)
    with open(dest_path, "w") as f:
      f.write(template_path_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  items_in_content = os.listdir(dir_path_content)
  
  for item in items_in_content:
    full_content_path = os.path.join(dir_path_content, item)

    if os.path.isfile(full_content_path):
      full_dest_path = os.path.join(dest_dir_path, item)
      if full_dest_path.endswith(".md"):
        full_dest_path = full_dest_path.replace("md", "html")
      print(full_dest_path)
      generate_page(full_content_path, template_path, full_dest_path)
  
    elif os.path.isdir(full_content_path):
      items_in_subdir = os.listdir(full_content_path)
      for sub_item in items_in_subdir:
        items_in_content.append(os.path.join(item, sub_item))

main()

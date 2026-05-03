import os
import shutil
from markdown_to_html import markdown_to_html_node
from extract_markdown import extract_markdown_images, extract_markdown_links
def main():
  copy("../static", "../public")
  generate_page("../content/index.md", "../template.html", "../public/index.html")

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
    # print(from_path_content)

    with open(template_path, "r") as f:
      template_path_content = f.read()
    # print(template_path_content)

    content = markdown_to_html_node(from_path_content).to_html()
    title = extract_title(from_path_content)
    template_path_content = template_path_content.replace("{{ Title }}", title)
    template_path_content = template_path_content.replace("{{ Content }}", content)
    # print(template_path_content)
    directories = extract_markdown_links(from_path_content)
    # print(directories)
    for directory in directories:
      # print(directory)
      if directory[1].startswith("/"):
        # print(f"make {os.path.dirname(dest_path) + directory[1]}")
        os.makedirs(os.path.dirname(dest_path) + directory[1], exist_ok=True)
    with open(dest_path, "w") as f:
      f.write(template_path_content)

main()

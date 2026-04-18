from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links
def split_nodes_image(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
    else:
      alt_text_and_url = extract_markdown_images(node.text)
      if len(alt_text_and_url) == 0:
        new_nodes.append(node)
        continue
  
      text_remain = node.text
      splitted_text = []
      for alt_text, url in alt_text_and_url:
        splitted_text.extend(text_remain.split(f"![{alt_text}]({url})", 1))
        text_remain = splitted_text.pop()

      j = 0
      for i in range(len(splitted_text)):
        if splitted_text[i] == "":
          continue
        new_nodes.append(TextNode(splitted_text[i], TextType.PLAIN))
        if j < len(alt_text_and_url):
          new_nodes.append(TextNode(alt_text_and_url[j][0], TextType.IMAGES, alt_text_and_url[j][1]))
          j += 1

  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
    else:
      alt_text_and_url = extract_markdown_links(node.text)
      if len(alt_text_and_url) == 0:
        new_nodes.append(node)
        continue

      text_remain = node.text
      splitted_text = []
      for alt_text, url in alt_text_and_url:
        splitted_text.extend(text_remain.split(f"[{alt_text}]({url})", 1))
        text_remain = splitted_text.pop()

      j = 0
      for i in range(len(splitted_text)):
        if splitted_text[i] == "":
          continue
        new_nodes.append(TextNode(splitted_text[i], TextType.PLAIN))
        if j < len(alt_text_and_url):
          new_nodes.append(TextNode(alt_text_and_url[j][0], TextType.LINKS, alt_text_and_url[j][1]))
          j += 1

  return new_nodes

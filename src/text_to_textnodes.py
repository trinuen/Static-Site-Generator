from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
    else:
      splitted_text = node.text.split(delimiter)
      if len(splitted_text) % 2 == 0:
        raise Exception("Closing delimiter is missing")
      
      for i in range(len(splitted_text)):
        if splitted_text[i] == "":
          continue
        elif i % 2 == 0:
          new_nodes.append(TextNode(splitted_text[i], TextType.PLAIN))
        else:
          new_nodes.append(TextNode(splitted_text[i], text_type))
  return new_nodes

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
  
      org_text = node.text
      for alt_text, url in alt_text_and_url:
        splitted_text = (org_text.split(f"![{alt_text}]({url})", 1))
        if len(splitted_text) != 2:
          raise ValueError("invalid markdown, image section not closed")
        if splitted_text[0] != "":
          new_nodes.append(TextNode(splitted_text[0], TextType.PLAIN))
        new_nodes.append(TextNode(alt_text, TextType.IMAGES, url))
        org_text = splitted_text[1]

      if org_text != "":
        new_nodes.append(TextNode(org_text, TextType.PLAIN))

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

      org_text = node.text
      for alt_text, url in alt_text_and_url:
        splitted_text = (org_text.split(f"[{alt_text}]({url})", 1))
        if len(splitted_text) != 2:
          raise ValueError("invalid markdown, link section not closed")
        if splitted_text[0] != "":
          new_nodes.append(TextNode(splitted_text[0], TextType.PLAIN))
        new_nodes.append(TextNode(alt_text, TextType.LINKS, url))
        org_text = splitted_text[1]

      if org_text != "":
        new_nodes.append(TextNode(org_text, TextType.PLAIN))

  return new_nodes


def text_to_textnodes(text):
  node = TextNode(text, TextType.PLAIN)
  res = [node]
  res = split_nodes_delimiter(res, '**', TextType.BOLD)
  res = split_nodes_delimiter(res, '_', TextType.ITALIC)
  res = split_nodes_delimiter(res, '`', TextType.CODE)
  res = split_nodes_image(res)
  res = split_nodes_link(res)
  return res

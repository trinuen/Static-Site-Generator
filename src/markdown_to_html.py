from htmlnode import HTMLNode, ParentNode, LeafNode
from markdown_blocks import *
from text_to_textnodes import text_to_textnodes
from text_to_html import text_node_to_html_node
from textnode import TextNode, TextType

def markdown_to_html_node(markdown: str) -> ParentNode:
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    block_type = block_to_block_type(block)

    if block_type == BlockType.paragraph:
      children.append(ParentNode("p", text_to_children(block)))

    elif block_type == BlockType.heading:
      header_size = get_header_size(block)
      children.append(ParentNode(f"h{header_size}", get_heading_children(block)))
  
    elif block_type == BlockType.code:
      htmlnodes = get_code_children(block)
      children.append(ParentNode("pre",htmlnodes))

    elif block_type == BlockType.quote:
      block = block.replace("> ", "")
      children.append(ParentNode("blockquote", text_to_children(block)))

    elif block_type == BlockType.unordered_list:
      htmlnodes = get_unordered_items(block)
      children.append(ParentNode("ul", htmlnodes))

    elif block_type == BlockType.ordered_list:
      htmlnodes = get_ordered_items(block)
      children.append(ParentNode("ol", htmlnodes))
  
  return ParentNode("div", children)

def text_to_children(text) -> list[HTMLNode]:
  htmlNodes = []
  text = text.replace("\n", " ")
  textnodes = text_to_textnodes(text)
  for textnode in textnodes:
    htmlNodes.append(text_node_to_html_node(textnode))
  return htmlNodes

def get_header_size(text):
  if text.startswith("# "):
    return 1
  elif text.startswith("## "):
    return 2
  elif text.startswith("### "):
    return 3
  elif text.startswith("#### "):
    return 4
  elif text.startswith("##### "):
    return 5
  elif text.startswith("###### "):
    return 6

def get_heading_children(text):
  text = text.replace("###### ", "")
  text = text.replace("##### ", "")
  text = text.replace("#### ", "")
  text = text.replace("### ", "")
  text = text.replace("## ", "")
  text = text.replace("# ", "")
  return text_to_children(text)

def get_code_children(text):
  text = text.replace("```", "")
  textnode = TextNode(text, TextType.PLAIN)
  htmlnode = text_node_to_html_node(textnode)
  htmlnode.tag = "code"
  return [htmlnode]

def get_unordered_items(text):
  items = text.replace("- ", "").split("\n")
  res = []
  for item in items:
    res.extend([ParentNode("li", text_to_children(item))])
  return res

def get_ordered_items(text):
  items = text.split("\n")
  for i in range(len(items)):
    items[i] = items[i].replace(f"{i+1}. ", "")
  res = []
  for item in items:
    res.extend([ParentNode("li", text_to_children(item))])
  return res
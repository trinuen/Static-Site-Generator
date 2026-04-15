from textnode import TextNode, TextType
from leafnode import LeafNode

def text_node_to_html_node(text_node: TextNode):
  if text_node.text_type == TextType.PLAIN_TEXT:
    return LeafNode(None, text_node.text)
  elif text_node.text_type == TextType.BOLD_TEXT:
    return LeafNode("b", text_node.text)
  elif text_node.text_type == TextType.ITALIC_TEXT:
    return LeafNode("i", text_node.text)
  elif text_node.text_type == TextType.CODE_TEXT:
    return LeafNode("code", text_node.text)
  elif text_node.text_type == TextType.LINKS:
    return LeafNode("a", text_node.text, {"href": text_node.url})
  elif text_node.text_type == TextType.IMAGES:
    return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
  else:
    raise ValueError("Invalid text type")
    
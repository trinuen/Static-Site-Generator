from textnode import TextNode, TextType
from enum import Enum

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
  new_nodes = []
  for node in old_nodes:
    if node.text_type != TextType.PLAIN:
      new_nodes.append(node)
    else:
      splitted_text = node.text.split(delimiter)
      if len(splitted_text) % 2 == 0:
        raise Exception("Closing delimiter is missing")
      
      for i in range(len(splitted_text)):
        if i % 2 == 0:
          new_nodes.append(TextNode(splitted_text[i], TextType.PLAIN))
        else:
          new_nodes.append(TextNode(splitted_text[i], text_type))
  return new_nodes
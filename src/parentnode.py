from htmlnode import HTMLNode
from leafnode import LeafNode
class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if not self.tag:
      raise ValueError("Tag does not exist")
    if not self.children:
      raise ValueError("Children does not exist")
    res = ""
    for node in self.children:
      res += node.to_html()
    
    return f"<{self.tag}>{res}</{self.tag}>"
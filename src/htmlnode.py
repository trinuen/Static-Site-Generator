class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("Not implemented")

  def props_to_html(self):
    res = []
    if self.props is None:
      return ""
    for k, v in self.props.items():
      res.append(f' {k}="{v}"')
    return " ".join(res)

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value is None:
      raise ValueError("Value does not exist")
    if not self.tag:
      return self.value
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
  def __repr__(self):
    return f"LeafNode({self.tag}, {self.value}, {self.props})"

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
    
    return f"<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"
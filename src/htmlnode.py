class HTMLNode:
  def __init__(self, tag:str="", value:str="", children=[], props={}):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def to_html(self):
    raise NotImplementedError("not implemented")

  def props_to_html(self):
    res = []
    if not self.props:
      return ""
    for k, v in self.props.items():
      res.append(f"{k}=\"{v}\"")
    return " ".join(res)

  def __repr__(self):
    return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
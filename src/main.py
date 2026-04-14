from textnode import TextNode, TextType

def main():
  textNode = TextNode("some text", TextType.BOLD_TEXT, "website.com")
  print(repr(textNode))

main()
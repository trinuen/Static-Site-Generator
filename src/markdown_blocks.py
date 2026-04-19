from enum import Enum

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def block_to_block_type(block):
  items = block.split("\n")
  if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
    return BlockType.heading
  elif len(items) > 1 and items[0].startswith("```") and items[-1].startswith("```"):
    return BlockType.code
  elif block.startswith(">"):
    return BlockType.quote
  elif block.startswith("- "):
    for item in items:
      if not item.startswith("- "):
        return BlockType.paragraph
    return BlockType.unordered_list
  elif block.startswith("1."):
    for i in range(len(items)):
      if not items[i].startswith(f"{i+1}. "):
        return BlockType.paragraph
    return BlockType.ordered_list
  return BlockType.paragraph

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_markdown import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = []
    split_string_sections = markdown.split("\n\n")
    for section in split_string_sections:
        section = section.strip()
        if section:
            blocks.append(section)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(md):
    if md.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if md.startswith("```") and md.endswith("```"):
        return BlockType.CODE
    
    lines = md.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_html_node(block):        
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        children = text_to_children(block)
        return ParentNode("p", children)
   
    elif block_type == BlockType.HEADING:
        level = 0
        for char in block:
            if char == "#": level += 1
            else:
                break
        text = block[level + 1:]
        children = text_to_children(text)    
        return ParentNode(f"h{level}", children)
    
    elif block_type == BlockType.QUOTE:
        quotes = [] 
        lines = block.split("\n")
        for line in lines:
            text = line[1:].strip()
            quotes.append(text)
        content = " ".join(quotes)
        children = text_to_children(content)
        return ParentNode("blockquote", children)
    
    elif block_type == BlockType.CODE:
        text = block[4:-3]
        node = TextNode(text, TextType.TEXT) 
        converted = text_node_to_html_node(node)
        code = ParentNode("code", [converted])
        return ParentNode("pre", [code])
    
    elif block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        items = []
        for line in lines:
            text = line[2:]
            children = text_to_children(text)
            items.append(ParentNode("li", children))
        return ParentNode("ul", items)

    elif block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        items = []
        for line in lines:
            text = line.split(". ", 1)[1]
            children = text_to_children(text)
            items.append(ParentNode("li", children))
        return ParentNode("ol", items)
    else:
        raise ValueError("invalid block type")
    
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children
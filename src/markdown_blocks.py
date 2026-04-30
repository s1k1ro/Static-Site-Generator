from enum import Enum 
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextType, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1

        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    




def markdown_to_blocks(markdown):
    #split into sections based on new lines
    sections = markdown.split("\n\n")
    #make a list to hold cleaned blocks
    blocks = []
    for section in sections:
        cleaned = section.strip()

        if cleaned != "":
            blocks.append(cleaned)
    
    return blocks


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
    
        if block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        else:
            raise ValueError(f"unknown block type: {block_type}")
        
        block_nodes.append(node)
    return ParentNode("div", block_nodes)


def text_to_children(text):
    text_list = text_to_textnodes(text)
    html_node_list = []
    for node in text_list:
        html_node_list.append(text_node_to_html_node(node))
    return html_node_list


def heading_to_html_node(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break

    stripped_text = block[(count+1):]
    return ParentNode(
        f"h{count}",  
        text_to_children(stripped_text)
        )

def paragraph_to_html_node(block):
    split_block = block.split("\n")
    joined_block = " ".join(split_block)
    return ParentNode(
        "p",
        text_to_children(joined_block)
    )

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines: 
        cleaned = line.lstrip(">").strip()
        new_lines.append(cleaned)
    joined_block = " ".join(new_lines)
    return ParentNode(
        "blockquote",
        text_to_children(joined_block)
    )

def unordered_list_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        cleaned = line.lstrip("-").strip()
        node = ParentNode("li", text_to_children(cleaned))
        new_lines.append(node)
    return ParentNode(
        "ul",
        new_lines
    )

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []
    for i, line in enumerate(lines, start = 1):
        prefix = f"{i}. "
        cleaned = line[len(prefix):]
        node = ParentNode("li", text_to_children(cleaned))
        li_nodes.append(node)
    return ParentNode(
        "ol",
        li_nodes
    )
    
def code_to_html_node(block):
    content = block[4:-3]
    text_node = TextNode(content, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    first_wrap = ParentNode("code", [html_node])
    return ParentNode(
        "pre",
        [first_wrap]
    )

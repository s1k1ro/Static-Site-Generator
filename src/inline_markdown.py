import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("invalid markdown syntax")
            for i, text in enumerate(split_text):
                if i % 2 == 0:
                    if text:
                        new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            image_list = extract_markdown_images(node.text)
            if not image_list:
                new_nodes.append(node)
                continue
            remaining = node.text #start with the full text
            for image in image_list:
                alt, url = image #unpacking tuple
                sections = remaining.split(f"![{alt}]({url})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                remaining = sections[1]
            if remaining != "": #check for trailing text and append
                new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        #if its not a text node just append to list,
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            #extract list of links each value is a tuple
            link_list = extract_markdown_links(node.text)
            #if list link is empty means there are no links just text and append node
            if not link_list:
                new_nodes.append(node)
                continue
            remaining = node.text #create a holder variable for remaining starting with original text
            for link in link_list: #loop through links
                text, url = link #unpack tuple
                sections = remaining.split(f"[{text}]({url})" ,1) #split before and after link
                if sections[0] != "": #if text before the link is not empty
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(text, TextType.LINK, url)) #append link
                remaining = sections[1] #update remaining
            if remaining != "":
                new_nodes.append(TextNode(remaining, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    #start with one plain text node
    nodes = [TextNode(text, TextType.TEXT)]

    #extract structured markdown first
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    #split plain text foramtting delimeters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    return nodes





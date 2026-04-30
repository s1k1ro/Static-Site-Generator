from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

def main():
    #node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(node)

    copy_files_recursive("static", "public")
    generate_pages_recursive("content", "template.html", "public")





main()
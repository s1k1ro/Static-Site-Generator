import unittest

from markdown_blocks import *


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_mtb_single_block(self):
        md = "Just one paragraph."

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Just one paragraph."

            ],
        )
    
    def test_mtb_heading_paragraph_list(self):
        md = """
# Heading

This is a paragraph with **bold** text.

- item one
- item two
- item three
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph with **bold** text.",
                "- item one\n- item two\n- item three"

            ],
        )
    
    def test_mtb_extra_blank_lines_start_end(self):
        md = """


First Block



Second Block

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First Block",
                "Second Block"

            ],
        )

    def test_mtb_blocks_with_surrounding_spaces(self):
        md="""
    First block with spaces

    Second block with spaces     """

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block with spaces",
                "Second block with spaces",

            ],
        )

    def test_mtb_empty_input(self):
        md = ""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_b2bt_heading(self):
        block = "## Hello World"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_b2bt_code(self):
        block = "```\ndef foo():\n    pass\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)
    def test_b2bt_quote(self):
        block ="> first line\n> second line"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_b2bt_unordered_list(self):
        block ="- apples\n- bananas\n- cherries"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_b2bt_ordered_list(self):
        block ="1. first\n2. second\n3. third"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)
    def test_b2bt_paragraph(self):
        block ="""
just some normal text
spanning two lines
"""
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_b2bt_7hash(self):
        block = "####### This is not a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)


    def test_mthn_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",

        )
    def test_mthn_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_mthn_heading(self):
        md = "# This is a heading with **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading with <b>bold</b> text</h1></div>",
        )

    def test_mthn_multiple_heading_levels(self):
        md = """
# Heading One

## Heading Two

### Heading Three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading One</h1><h2>Heading Two</h2><h3>Heading Three</h3></div>",
        )

    def test_mthn_quote(self):
        md = """
> This is a quote
> with two lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with two lines</blockquote></div>",
        )

    def test_mtn_unordered_list(self):
        md = """
- apples
- bananas with **bold**
- cherries
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>apples</li><li>bananas with <b>bold</b></li><li>cherries</li></ul></div>",
        )  
    def test_mthn_mixed_blocks(self):
        md = """     
# Title

This is a paragraph.

- list item one
- list item two

> A quote here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>This is a paragraph.</p><ul><li>list item one</li><li>list item two</li></ul><blockquote>A quote here</blockquote></div>",
        )  


if __name__ == "__main__":
    unittest.main()


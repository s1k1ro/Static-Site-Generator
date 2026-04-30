import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestInlineMarkdown(unittest.TestCase):
    def test_simple_code(self):
        old_node = TextNode("This is `inline code` and text",TextType.TEXT)
        self.assertEqual((split_nodes_delimiter([old_node],"`", TextType.CODE)), [
            TextNode("This is ", TextType.TEXT),
            TextNode("inline code", TextType.CODE),
            TextNode(" and text", TextType.TEXT)
        ])
    def test_bold_delimiter(self):
        old_node = TextNode("This is **bold words** and text",TextType.TEXT)
        self.assertEqual((split_nodes_delimiter([old_node],"**", TextType.BOLD)), [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold words", TextType.BOLD),
            TextNode(" and text", TextType.TEXT)
        ])
    def test_non_text(self):
        old_node = TextNode("The bold words", TextType.BOLD)
        self.assertEqual((split_nodes_delimiter([old_node],"**", TextType.BOLD)), [
            TextNode("The bold words", TextType.BOLD)
        ])

    def test_invalid_markdown(self):
        with self.assertRaises(Exception):
            old_node = TextNode("This is **bold words", TextType.TEXT)
            split_nodes_delimiter([old_node],"**", TextType.BOLD)
    
    def test_extract_image(self):
        text =  "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )
    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_extract_link_with_image(self):
        text = "Here is an image ![cat](https://img.com/cat.png) and a link [boot.dev](https://boot.dev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("boot.dev", "https://boot.dev")]
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    def test_split_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])    
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )    

    def test_split_image_no_link(self):
        node = TextNode("just some plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])    
        self.assertListEqual(
            [
                TextNode("just some plain text", TextType.TEXT,),
            ],
            new_nodes,
        )        
    def test_split_image_non_text_node(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])    
        self.assertListEqual(
            [
                TextNode("already bold", TextType.BOLD,),
            ],
            new_nodes,
        )   


    def test_split_link(self):
        node = TextNode(
            "Check out [boot.dev](https://www.boot.dev) and [github](https://github.com) for coding.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
               TextNode("Check out ", TextType.TEXT), 
               TextNode("boot.dev", TextType.LINK, "https://www.boot.dev"),
               TextNode(" and ", TextType.TEXT),
               TextNode("github", TextType.LINK, "https://github.com"),
               TextNode(" for coding.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_only_link(self):
        node = TextNode("[only a link](https://example.com)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])    
        self.assertListEqual(
            [
                TextNode("only a link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    
    def test_split_link_no_link(self):
        node = TextNode("just some plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])    
        self.assertListEqual(
            [
                TextNode("just some plain text", TextType.TEXT,),
            ],
            new_nodes,
        )        
    def test_split_link_non_text_node(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])    
        self.assertListEqual(
            [
                TextNode("already bold", TextType.BOLD,),
            ],
            new_nodes,
        )    
    
    def test_text2nodes_plain_text_only(self):
        text = "This is just plain text"
        actual = text_to_textnodes(text)

        expected = [
            TextNode("This is just plain text", TextType.TEXT)
        ]

        self.assertEqual(actual, expected)

    def test_text2nodes_mixed_formatting(self):
        text = "This is **bold** and _italic_ and `code`"
        actual = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(actual, expected)

    def test_text2nodes_image_only(self):
        text = "This has an ![wizard bear](https://example.com/bear.png)"
        actual = text_to_textnodes(text)

        expected = [
            TextNode("This has an ", TextType.TEXT),
            TextNode("wizard bear", TextType.IMAGE, "https://example.com/bear.png"),
        ]

        self.assertEqual(actual, expected)

    def test_text2nodes_link_only(self):
        text = "This has a [Boot.dev](https://boot.dev) link"
        actual = text_to_textnodes(text)

        expected = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
            TextNode(" link", TextType.TEXT),
        ]

        self.assertEqual(actual, expected)

    def test_text2nodes_full_mixed_case(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()


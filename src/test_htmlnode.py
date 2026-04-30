import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com"')
    def test_no_props(self):
        node = HTMLNode(props = None)
        self.assertEqual(node.props_to_html(), "")
    def test_mulitple_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"' )
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_tag_and_props(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Hello, world!</a>')
    
    def test_leaf_no_tag(self):
        node= LeafNode(None, "this is text")
        self.assertEqual(node.to_html(), "this is text")
    
    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span","child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )
    def test_to_html_with_great_grandchildren(self):
        great_grandchild_node = LeafNode("p", "greatgrandchild")
        grandchild_node = ParentNode("b", [great_grandchild_node])
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b><p>greatgrandchild</p></b></span></div>"
        )    
    
    def test_to_html_Parent_multiple_child_same_level(self):
        child_node_1 = LeafNode("span", "childnode1")
        child_node_2 = LeafNode("b", "childnode2")
        parent_node = ParentNode("div", [child_node_1, child_node_2]) 
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>childnode1</span><b>childnode2</b></div>"
        )

    def test_to_html_Parent_child_withprops(self):
        child_node_1 = LeafNode("span", "childnode1")
        child_node_2 = LeafNode("b", "childnode2",{"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node_1, child_node_2]) 
        self.assertEqual(
            parent_node.to_html(),
            '<div><span>childnode1</span><b href="https://www.google.com">childnode2</b></div>'
        )





if __name__ == "__main__":
    unittest.main()


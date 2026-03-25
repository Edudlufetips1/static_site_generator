import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "click me", None, {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_tag(self):
        node = HTMLNode("filler", "uppercase", None, None)
        self.assertEqual(node.tag, "filler") 

    def test_props_to_html2(self):
        node = HTMLNode("filler", "uppercase", None, None)
        self.assertEqual(node.props_to_html(), "") 

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Serral is the GOAT", {"href": "https://www.nowhere.place"})
        self.assertEqual(node.to_html(), '<a href="https://www.nowhere.place">Serral is the GOAT</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "value")
        self.assertEqual(node.to_html(), "value")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_parent_mult_children(self):
        child_node1 = LeafNode("a", "child1")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("c", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(), "<c><a>child1</a><b>child2</b></c>")
    
    def test_parent_no_tag(self):
        child_node = LeafNode("a", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_no_children(self):
        parent_node = ParentNode("a", None)
        self.assertRaises(ValueError, parent_node.to_html)

if __name__ == "__main__":
    unittest.main()
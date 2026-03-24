import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("This is a test node", TextType.ITALIC)
        node2 = TextNode("This is a test node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_url_is_None(self):
        node = TextNode("some text", TextType.BOLD, url=None)
        node2 = TextNode("some text", TextType.BOLD)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
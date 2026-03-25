import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "text")
        self.assertEqual(html_node.tag, "code")

    def test_link(self):
        node = TextNode("text", TextType.LINK, 'https://oxford.edu')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'text')
        self.assertEqual(html_node.props["href"], "https://oxford.edu") # type: ignore

    def test_image(self):
        node = TextNode("image test", TextType.IMAGE, "https://image.test")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["alt"], "image test")
        self.assertEqual(html_node.props["src"], "https://image.test") # type: ignore

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_invalid_text_type(self):
        # We use a dummy object or None to force the error
        node = TextNode("wrong", "nonsense")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()
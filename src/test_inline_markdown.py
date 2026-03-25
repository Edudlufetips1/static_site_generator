import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_bold_italic(self):
        node1 = TextNode("bolded", TextType.BOLD)
        node2 = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bolded", TextType.BOLD), 
                TextNode("This is ", TextType.TEXT), 
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_two_bold_sections(self):
        node = TextNode("**first** and **second**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("first", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.BOLD)
            ],
            new_nodes,
        )

    def test_end_code_block(self):
        node = TextNode("This ends with a `code_block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This ends with a ", TextType.TEXT),
                TextNode("code_block", TextType.CODE)
            ],
            new_nodes,
        )

    def test_unclosed_delimiter(self):
        node = TextNode("This has an `unclosed code block", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_start_with_delimiter(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("link to tomorrow is [to tom](www.tomorrow.today)")
        self.assertEqual([("to tom", "www.tomorrow.today")], matches)

    def test_no_image_to_extract(self):
        matches = extract_markdown_images("the link to this image has been removed")
        self.assertEqual([], matches)
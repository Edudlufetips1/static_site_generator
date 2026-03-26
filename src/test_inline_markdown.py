import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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

    def test_no_link_to_extract(self):
        matches = extract_markdown_links("there are no links here, just plain text")
        self.assertEqual([], matches)

    def test_split_images_multiple(self):
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_image_no_alt_text(self):
        node = TextNode("This is text with a ![](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_nodes,
        )

    def test_malformed_image_markdown(self):
        node = TextNode("This is a malformed image ![oops(https://site.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is a malformed image ![oops(https://site.com)", TextType.TEXT),
            ],
            new_nodes
        )
    
    def test_link_with_no_text(self):
        node = TextNode("This is a link with no text [](https://person.hu)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is a link with no text ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://person.hu"),
            ],
            new_nodes
        )

    def test_malformed_link_markdown(self):
        node = TextNode("This is a malformed link [(www.who.where)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is a malformed link [(www.who.where)", TextType.TEXT),
            ],
            new_nodes
        )

    def test_split_links_multiple(self):
        node = TextNode("This is text with a [link1](www.link1.com) and another [link2](www.link2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "www.link1.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "www.link2.com"),
            ],
            new_nodes
        )
    
    def test_text_to_nodes_multiple_text_types(self):
        new_nodes = text_to_textnodes("This is text with a [link](www.google.com) and an ![image](www.canislupis.com/rottweiler.jpeg)")
        self.assertEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.canislupis.com/rottweiler.jpeg"),
            ],
            new_nodes
        )

    def test_text_only_one_bold_word(self):
        new_nodes = text_to_textnodes("**antidistablishmentarianism**")
        self.assertEqual(
            [
                TextNode("antidistablishmentarianism", TextType.BOLD),
            ],
            new_nodes
        )

    def test_image_without_text(self):
        new_nodes = text_to_textnodes("![](www.notexttothisIMAGE.jpeg)")
        self.assertEqual(
            [
                TextNode("",TextType.IMAGE, "www.notexttothisIMAGE.jpeg"),
            ],
            new_nodes
        )
    
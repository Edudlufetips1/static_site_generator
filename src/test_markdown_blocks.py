from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, block_to_html_node, text_to_children, markdown_to_html_node
import unittest
class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_remove_excess_empty_lines(self):
        md = """
This line is in a different zip code




from this one.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This line is in a different zip code",
                "from this one."
            ]
        )

    def test_leading_trailing_newline_removal(self):
        md = """
This should be the first and only line.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This should be the first and only line."
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Hi"), BlockType.HEADING)
    def test_code(self):
        md ="""
```
a bunch of code
```
"""
        self.assertEqual(block_to_block_type(md.strip()), BlockType.CODE)
    def test_quote(self):
        self.assertEqual(block_to_block_type(">practice doesn't always make perfect, but good practice gets you closer"), BlockType.QUOTE)
    def test_unordered_list(self):
        md = """
- 3
- apple
- shoe
"""
        self.assertEqual(block_to_block_type(md.strip()), BlockType.UNORDERED_LIST)
    def test_ordered_list(self):
        md = """
1. tom
2. dick
3. harry
"""
        self.assertEqual(block_to_block_type(md.strip()), BlockType.ORDERED_LIST)
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("just the most boring text ever"), BlockType.PARAGRAPH)
class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
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
    
    def test_heading(self):
        md = """
### A third level heading lives here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>A third level heading lives here</h3></div>")
    
    def test_quote(self):
        md = """
> Is doing a thing once and expecting lots of results... sanity?!
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Is doing a thing once and expecting lots of results... sanity?!</blockquote></div>")

    def test_code(self):
        md = """
```
a noobish block of code
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>a noobish block of code\n</code></pre></div>")

    def test_unordered_list(self):
        md = """
- 6
- 3
- 5
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>6</li><li>3</li><li>5</li></ul></div>")
    
    def test_ordered_list(self):
        md = """
1. Jordan
2. Kareem
3. Wilt
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Jordan</li><li>Kareem</li><li>Wilt</li></ol></div>")
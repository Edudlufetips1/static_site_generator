from markdown_blocks import markdown_to_blocks

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

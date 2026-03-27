def markdown_to_blocks(markdown):
    blocks = []
    split_string_sections = markdown.split("\n\n")
    for section in split_string_sections:
        section = section.strip()
        if section:
            blocks.append(section)
    return blocks
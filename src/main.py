from textnode import TextNode, TextType
from copystatic import copy_files_recursive
from gencontent import generate_page, extract_title

def main():
    textnode = TextNode("title", TextType.BOLD, "https:idk.com")
    print(textnode)

    copy_files_recursive("./static", "./public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()
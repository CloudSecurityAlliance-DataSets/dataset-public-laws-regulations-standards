import argparse
from bs4 import BeautifulSoup

# Function to convert HTML to Markdown
def convert_to_markdown(soup):
    markdown = []
    
    # Iterate over all elements and convert them
    for element in soup.find_all():
        if element.name == "h1":
            markdown.append(f"# {element.text.strip()}")
        elif element.name == "h2":
            markdown.append(f"## {element.text.strip()}")
        elif element.name == "h3":
            markdown.append(f"### {element.text.strip()}")
        elif element.name == "h4":
            markdown.append(f"#### {element.text.strip()}")
        elif element.name == "p":
            markdown.append(element.text.strip())
        elif element.name == "ul":
            for li in element.find_all("li"):
                markdown.append(f"- {li.text.strip()}")
        elif element.name == "ol":
            for idx, li in enumerate(element.find_all("li"), 1):
                markdown.append(f"{idx}. {li.text.strip()}")
        elif element.name == "table":
            for row in element.find_all("tr"):
                cells = row.find_all(["th", "td"])
                markdown.append(" | ".join(cell.text.strip() for cell in cells))
                markdown.append("|" + " --- |" * len(cells))
    
    return "\n\n".join(markdown)

# Main function
def main():
    parser = argparse.ArgumentParser(description="Convert HTML to Markdown")
    parser.add_argument("filename", help="Input HTML file to convert")
    args = parser.parse_args()

    input_filename = args.filename
    output_filename = f"{input_filename}.md"

    # Load the HTML file
    with open(input_filename, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Convert to Markdown
    markdown_content = convert_to_markdown(soup)

    # Write to output Markdown file
    with open(output_filename, 'w', encoding='utf-8') as markdown_file:
        markdown_file.write(markdown_content)

    print(f"Markdown file saved to: {output_filename}")

if __name__ == "__main__":
    main()


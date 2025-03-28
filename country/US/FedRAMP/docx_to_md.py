#!/usr/bin/env python3
"""
Word Document to GitHub Markdown Converter

This script converts Word documents (.docx) to GitHub-flavored Markdown format (.md),
extracting embedded images to a separate directory and properly linking them in the
resulting markdown file.

Usage:
    python docx_to_md.py --input <docx_file_path>

Example:
    python docx_to_md.py --input FedRAMP-Security-Assessment-Report-(SAR)-Template.docx

Requirements:
    - mammoth: For Word document conversion and image extraction
    - pypandoc: For ensuring GitHub-flavored markdown
    - pandoc: External dependency used by pypandoc (must be installed separately)
"""

import argparse
import os
import re
import shutil
import uuid
from pathlib import Path

import mammoth
import pypandoc


def sanitize_filename(name):
    """
    Sanitize a string to be used as a valid filename.
    
    Args:
        name (str): The input string to sanitize
        
    Returns:
        str: A sanitized string with invalid filename characters replaced by underscores
    """
    # Replace invalid filename characters with underscores
    return re.sub(r'[\\/*?:"<>|]', '_', name)


def extract_base_name(input_file):
    """
    Extract the base name from a file path without extension.
    
    Args:
        input_file (str): Path to the input file
        
    Returns:
        str: Base name of the file without extension
    """
    base_name = os.path.basename(input_file)
    return os.path.splitext(base_name)[0]


def docx_to_md(input_file):
    """
    Convert a Word document to GitHub-flavored Markdown.
    
    Args:
        input_file (str): Path to the input .docx file
        
    Returns:
        None: Creates markdown file and images directory
    
    Notes:
        - Creates a directory with the same name as the docx file
        - Within that directory, creates:
          - A markdown file named filename.md
          - An images directory for extracted images
        - Uses pandoc via pypandoc to ensure GitHub-flavored markdown
    """
    # STEP 1: Create directory structure
    base_name = extract_base_name(input_file)
    sanitized_base = sanitize_filename(base_name)
    
    # Main directory
    output_dir = sanitized_base
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # Images directory inside main directory
    images_dir = f"{output_dir}/images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Created images directory: {images_dir}")
    
    # STEP 2: Define image handler for mammoth
    image_map = {}
    
    def handle_image(image):
        """Callback to extract images from Word document"""
        # Generate a unique ID for the image
        image_id = str(uuid.uuid4())
        # Determine file extension based on content type
        content_type = image.content_type
        extension = content_type.split("/")[1] if "/" in content_type else "png"
        
        # Create image filename
        image_filename = f"image_{image_id}.{extension}"
        image_path = os.path.join(images_dir, image_filename)
        
        # Save image content to file
        with open(image_path, "wb") as image_file:
            with image.open() as image_data:
                image_file.write(image_data.read())
        
        # Store the image mapping
        image_map[image_id] = image_filename
        
        # Return the markdown image reference with relative path from the markdown file
        # Since the MD file will be in the same directory as the images folder,
        # we use a relative path to the images directory
        return {"src": f"images/{image_filename}"}
    
    # STEP 3: Convert DOCX to initial markdown with mammoth
    print(f"Converting Word document: {input_file}")
    
    with open(input_file, "rb") as docx_file:
        result = mammoth.convert_to_markdown(
            docx_file,
            transform_document=mammoth.transforms.paragraph(lambda p: p),
            convert_image=mammoth.images.img_element(handle_image)
        )
    
    initial_markdown = result.value
    
    # Report any warnings
    if result.messages:
        print("\nConversion warnings:")
        for message in result.messages:
            print(f"  - {message}")
    
    # STEP 4: Convert to GitHub-flavored markdown using pypandoc
    print("Applying GitHub flavor markdown formatting with pypandoc")
    github_markdown = pypandoc.convert_text(
        initial_markdown,
        'gfm',  # GitHub-Flavored Markdown
        format='markdown',
        extra_args=['--wrap=none']  # Prevents line wrapping
    )
    
    # STEP 5: Write the output markdown file
    output_file = f"{output_dir}/{sanitized_base}.md"  # Using original filename with .md extension
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(github_markdown)
    
    print(f"Created markdown file: {output_file}")
    print(f"Extracted images saved to: {images_dir}/")
    
    # STEP 6: Report conversion statistics
    image_count = len(image_map)
    print(f"\nConversion statistics:")
    print(f"  - Images extracted: {image_count}")


def main():
    """
    Main function: Parse command line arguments and call docx_to_md.
    """
    parser = argparse.ArgumentParser(
        description='Convert Word documents to GitHub-flavored Markdown.',
        epilog='Creates a markdown file and extracts images to a directory.'
    )
    parser.add_argument('--input', required=True, help='Path to the input .docx file')
    
    args = parser.parse_args()
    
    # Validate that input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' does not exist.")
        return 1
    
    # Validate that input file is a Word document
    if not args.input.lower().endswith('.docx'):
        print(f"Error: Input file '{args.input}' is not a .docx file.")
        return 1
    
    # Convert Word document to Markdown
    docx_to_md(args.input)
    return 0


if __name__ == "__main__":
    main()
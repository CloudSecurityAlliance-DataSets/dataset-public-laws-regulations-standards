#!/usr/bin/env python3

import tiktoken
import argparse

def count_tokens(file_path, encoding_name='cl100k_base'):
    """
    Counts the tokens in a Markdown text document using OpenAI's tiktoken.

    Args:
        file_path (str): Path to the Markdown file.
        encoding_name (str): Tokenizer encoding to use (default is 'cl100k_base').

    Returns:
        int: Total number of tokens in the file.
    """
    # Load the tokenizer
    encoding = tiktoken.get_encoding(encoding_name)

    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Encode the content and count tokens
        tokens = encoding.encode(content)
        return len(tokens)
    except Exception as e:
        print(f"Error reading file or counting tokens: {e}")
        return 0

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Count tokens in a Markdown file for ChatGPT.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input Markdown file.")
    args = parser.parse_args()

    # Count tokens
    token_count = count_tokens(args.input)
    print(f"Total tokens in the file: {token_count}")

if __name__ == "__main__":
    main()


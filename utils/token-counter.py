#!/usr/bin/env python3

import argparse
import tiktoken

def count_tokens_in_file(filename: str, model: str = "gpt-3.5-turbo"):
    # Load the tokenizer for the specific model
    encoding = tiktoken.encoding_for_model(model)
    
    # Read the content of the file
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Encode the text into tokens
    tokens = encoding.encode(text)
    
    # Count the number of tokens
    num_tokens = len(tokens)
    
    print(f"Number of tokens in {filename}: {num_tokens}")

def main():
    parser = argparse.ArgumentParser(description="Count tokens in a text file for AI submission.")
    parser.add_argument('file', type=str, help="Path to the text file.")
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', 
                        help="AI model name for token counting (default: gpt-3.5-turbo).")
    
    args = parser.parse_args()
    
    # Call the function to count tokens
    count_tokens_in_file(args.file, args.model)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import os
import re
import csv
from bs4 import BeautifulSoup
from pathlib import Path

def extract_page_data(file_path):
    """Extract structured data from a single page file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else ""
        
        # Extract main heading (h1)
        h1_tag = soup.find('h1')
        heading = h1_tag.text if h1_tag else ""
        
        # Extract description from meta tag
        description_tag = soup.find('meta', {'name': 'description'})
        description = description_tag.get('content', '') if description_tag else ""
        
        # Extract section (from breadcrumb or URL path)
        path_parts = str(file_path).split('/')
        section = ""
        if len(path_parts) >= 3:  # Now we need at least 3 parts: ./aiuc-1.com/section/file
            section_raw = path_parts[-2]  # Get the directory name
            # Clean up section name
            section_map = {
                'data-and-privacy': 'Data & Privacy',
                'security': 'Security', 
                'safety': 'Safety',
                'reliability': 'Reliability',
                'accountability': 'Accountability',
                'society': 'Society'
            }
            section = section_map.get(section_raw, section_raw)
        
        # Extract keywords - look for gray background keyword tags
        keywords = []
        keyword_divs = soup.find_all('div', class_='bg-gray-200')
        for div in keyword_divs:
            text = div.text.strip()
            if text and text not in keywords:
                keywords.append(text)
        
        # Extract Application, Frequency, Type - use more flexible approach
        application = ""
        frequency = ""
        type_val = ""
        
        # Look for the metadata section with these fields
        metadata_sections = soup.find_all('div', class_='flex flex-col gap-2')
        for meta_section in metadata_sections:
            header_div = meta_section.find('div', string=lambda text: text and text.strip().upper() in ['APPLICATION', 'FREQUENCY', 'TYPE'])
            if header_div:
                header_text = header_div.text.strip().upper()
                # Find the next div with the value
                value_div = meta_section.find('div', class_='flex flex-wrap gap-2')
                if value_div:
                    value = value_div.text.strip()
                    if header_text == 'APPLICATION':
                        application = value
                    elif header_text == 'FREQUENCY':
                        frequency = value
                    elif header_text == 'TYPE':
                        type_val = value
        
        # Extract crosswalks - look for framework links more broadly
        crosswalks = []
        crosswalk_links = soup.find_all('a', href=lambda x: x and '/crosswalks/' in x)
        for link in crosswalk_links:
            # Look for the framework name in the link
            framework_div = link.find('div')
            if framework_div:
                framework_name = framework_div.text.strip()
                if framework_name and framework_name not in crosswalks:
                    crosswalks.append(framework_name)
        
        # Extract control activities - extract full content between "Should include" and "Organizations can submit"
        control_activities = ""
        all_text = soup.get_text(separator='\n')  # Preserve line breaks
        
        should_include_pos = all_text.find("Should include")
        organizations_pos = all_text.find("Organizations can submit alternative evidence demonstrating how they meet the requirement")
        
        if should_include_pos != -1 and organizations_pos != -1:
            # Extract the content between these two markers
            raw_activities = all_text[should_include_pos:organizations_pos].strip()
            # Clean up excessive whitespace while preserving intentional formatting
            lines = []
            for line in raw_activities.split('\n'):
                line = line.strip()
                if line:  # Skip empty lines
                    lines.append(line)
            control_activities = '\n'.join(lines)
        elif should_include_pos != -1:
            # Fallback: just get the first sentence if we can't find the end marker
            match = re.search(r'Should include[^\.]*\.', all_text, re.IGNORECASE)
            if match:
                control_activities = match.group(0).strip()
        
        return {
            'title': title,
            'section': section,
            'heading': heading,
            'description': description,
            'keywords': '; '.join(keywords) if keywords else '',
            'application': application,
            'frequency': frequency,
            'type': type_val,
            'crosswalks': '; '.join(crosswalks) if crosswalks else '',
            'control_activities': control_activities,
            'url_path': 'https://aiuc-1.com/' + str(file_path).replace('./aiuc-1.com/', '')
        }
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    """Main function to process all pages and generate CSV."""
    # Find all page files in the aiuc-1.com directory (exclude index.html and crosswalks)
    page_files = []
    
    for root, dirs, files in os.walk('./aiuc-1.com'):
        # Skip certain directories
        if any(skip in root for skip in ['/.', '/crosswalks']):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            # Skip index.html and files that are clearly not content pages
            if file != 'index.html' and not file.startswith('.'):
                page_files.append(file_path)
    
    print(f"Found {len(page_files)} page files to process...")
    
    # Extract data from each page
    data = []
    for file_path in page_files:
        page_data = extract_page_data(file_path)
        if page_data:
            data.append(page_data)
            print(f"Processed: {file_path}")
    
    # Write to CSV
    if data:
        fieldnames = ['title', 'section', 'heading', 'description', 'keywords', 
                     'application', 'frequency', 'type', 'crosswalks', 
                     'control_activities', 'url_path']
        
        with open('aiuc-1-standard-data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"\nCSV file 'aiuc-1-standard-data.csv' created with {len(data)} records!")
    else:
        print("No data extracted!")

if __name__ == '__main__':
    main()
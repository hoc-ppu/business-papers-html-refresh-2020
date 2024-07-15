# Create tables of InDesign files for business papers redesign index

import os
import re
import csv
import codecs
from bs4 import BeautifulSoup

# Filter .indd & .pdf extensions
def filter_files_with_extension(files):
    filtered_files = []
    for file in files:
        if file.endswith('.indd') or file.endswith('.pdf') or file.endswith('.html'):
            filtered_files.append(file)
    return filtered_files

# Extract YYYY-MM-DD from parent directory name
def extract_date_from_parent_directory(parent_dir):
    # Date from parent directory name
    match = re.search(r'\d{4}-\d{2}-\d{2}', parent_dir)
    if match:
        return match.group(0)
    else:
        return None

# Read folder and write to a CSV file
def read_indesign_folder(folder_path, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # CSV headers
        writer.writerow(['Date', 'Filename', 'Relative Path'])
        
        # Search for files in the (sub)folders
        for root, dirs, files in os.walk(folder_path):
            # Filter .indd or .pdf 
            filtered_files = filter_files_with_extension(files)
            for file in filtered_files:
                # Get path and dir
                file_path = os.path.join(root, file)
                parent_dir = os.path.basename(os.path.dirname(file_path))
                
                # Extract date from dir
                date = extract_date_from_parent_directory(parent_dir)
                
                if date:
                    # Get relative path of file
                    relative_path = os.path.relpath(file_path, folder_path)

                    # Write file info to CSV
                    writer.writerow([date, file, relative_path])
                
    print('CSV file generated.')

# Inject CSV contents into HTML tables (one table per date example)
def inject_csv_into_html(csv_file_path, html_file_path):
    # Read and group
    date_tables = {}
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip headers
        
        for row in reader:
            date = row[0]
            if date not in date_tables:
                date_tables[date] = []
            date_tables[date].append(row)

    # Read existing HTML
    with codecs.open(html_file_path, 'r', encoding='utf-8', errors='ignore') as html_file:
        html_content = html_file.read()

    # Find concats <div> in index.html and insert tables
    soup = BeautifulSoup(html_content, 'html.parser')
    concats_div = soup.find('div', id='concats')
    if concats_div:
        concats_div.clear() # Remove existing content

        # Generate and insert tables
        for date, rows in date_tables.items():
            # Create elements
            details = soup.new_tag('details')
            concats_div.append(details)

            summary = soup.new_tag('summary')
            details.append(summary)
            
            # Add drop-downs by date
            bold_date = soup.new_tag('b')
            bold_date.string = date
            summary.append(bold_date)
            span_icon = soup.new_tag('span', attrs={'class': 'icon'})
            span_icon.string = ' ⬇️'
            summary.append(span_icon)
            
            # Create table for current date
            table_html = '<table border="1">\n'
            
            for row in rows:
                table_html += '  <tr>\n'
                for cell in row[1:]:  
                    if row.index(cell) == 2:
                        full_url = f"https://github.com/hoc-ppu/business-papers-redesign/raw/master/InDesign/{cell}"
                        table_html += f'    <td><a href="{full_url}">{cell}</a></td>\n'
                    else:
                        table_html += f'    <td>{cell}</td>\n'
                table_html += '  </tr>\n'
            
            table_html += '</table>\n'
            
            details.append(BeautifulSoup(table_html, 'html.parser'))

        # Write back HTML
        with codecs.open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(str(soup))

        print('HTML file updated successfully.')
    else:
        print('Error: <div id="concats"> not found in HTML file.')

# Paths
indesign_folder = 'InDesign' # InDesign samples on repo
csv_file = 'demo/output.csv' # CSV
html_file = 'demo/index.html' # business-papers-redesign homepage

read_indesign_folder(indesign_folder, csv_file)
inject_csv_into_html(csv_file, html_file)


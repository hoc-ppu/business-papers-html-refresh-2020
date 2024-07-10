from bs4 import BeautifulSoup
import os
import re
import pyperclip
import requests

# Function to re-populate existing tables with samples
def update_html_table_with_files(file_path, table_id, directory):
    # Verify file path and dir
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"No such directory: '{directory}'")
    
    # Read in
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'lxml')
    table = soup.find('table', id=table_id)
    
    if not table:
        raise ValueError(f"Table with id '{table_id}' not found in the provided HTML content.")
    
    tbody = table.find('tbody')
    if not tbody:
        raise ValueError(f"No <tbody> found in the table with id '{table_id}'.")

    # Clear existing rows
    tbody.clear()

    # Get list of HTML files in the specified directory
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    for html_file in html_files:
        # Extract date from filename
        match = re.search(r'\d{4}-\d{2}-\d{2}', html_file)
        if not match:
            continue  # Skip files that do not have a date in the expected format

        date = match.group()

        # Create tr
        new_row = soup.new_tag('tr')
        
        # Create date placeholder
        date_cell = soup.new_tag('td')
        date_cell.string = date
        new_row.append(date_cell)
        
        # Create placeholder for new PDF link
        new_pdf_cell = soup.new_tag('td')
        new_pdf_cell.string = "TBD"
        new_row.append(new_pdf_cell)
        
        # Create placeholder for old PDF link
        old_pdf_cell = soup.new_tag('td')
        old_pdf_cell.string = "TBD"
        new_row.append(old_pdf_cell)
        
        # Create link to new HTML sample
        new_html_cell = soup.new_tag('td')
        link_tag = soup.new_tag('a', href=os.path.join(directory, html_file))
        link_tag.string = "HTML link"
        new_html_cell.append(link_tag)
        new_row.append(new_html_cell)
        
        # Create placeholder for old HTML sample
        current_online_html_cell = soup.new_tag('td')
        current_online_html_cell.string = "TBD"
        new_row.append(current_online_html_cell)
        
        # Append new row to table
        tbody.append(new_row)
    
    # Write content back to HTML
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    
    print(f"Table with ID '{table_id}' update complete.")


# Function to create a new table of complete examples
def populate_completes_table(file_path, table_id, dates, directories):
    # Verify file path
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    
    # Read in
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'lxml')
    table = soup.find('table', id=table_id)
    
    if not table:
        raise ValueError(f"Table with id '{table_id}' not found in the provided HTML content.")
    
    tbody = table.find('tbody')
    if not tbody:
        raise ValueError(f"No <tbody> found in the table with id '{table_id}'.")

    # Populate table with dates and links
    for date in dates:
        # Create a new row
        new_row = soup.new_tag('tr')
        
        # Create the Date cell
        date_cell = soup.new_tag('td')
        date_cell.string = date
        new_row.append(date_cell)
        
        # Create the New PDF design cell with link from 'newPDF' directory
        new_pdf_cell = soup.new_tag('td')
        new_pdf_link = os.path.join(directories['newPDF'], f'{date}.pdf')
        new_pdf_link_tag = soup.new_tag('a', href=new_pdf_link)
        new_pdf_link_tag.string = "PDF link"
        new_pdf_cell.append(new_pdf_link_tag)
        new_row.append(new_pdf_cell)
        
        # Create the Old PDF design cell with link from 'oldPDF' directory
        old_pdf_cell = soup.new_tag('td')
        old_pdf_link = os.path.join(directories['oldPDF'], f'{date}.pdf')
        old_pdf_link_tag = soup.new_tag('a', href=old_pdf_link)
        old_pdf_link_tag.string = "PDF link"
        old_pdf_cell.append(old_pdf_link_tag)
        new_row.append(old_pdf_cell)
        
        # Create the New HTML cell with link from 'newHTML' directory
        new_html_cell = soup.new_tag('td')
        new_html_link = os.path.join(directories['newHTML'], f'{date}.html')
        new_html_link_tag = soup.new_tag('a', href=new_html_link)
        new_html_link_tag.string = "HTML link"
        new_html_cell.append(new_html_link_tag)
        new_row.append(new_html_cell)
        
        # Create the Old HTML cell with link from 'oldHTML' directory
        old_html_cell = soup.new_tag('td')
        old_html_link = os.path.join(directories['oldHTML'], f'{date}.html')
        old_html_link_tag = soup.new_tag('a', href=old_html_link)
        old_html_link_tag.string = "HTML link"
        old_html_cell.append(old_html_link_tag)
        new_row.append(old_html_cell)
        
        # Append the new row to the table body
        tbody.append(new_row)
    
    # Write the updated HTML content back to the file with utf-8 encoding
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    
    print(f"Table with ID '{table_id}' update complete.")

# Example usage
file_path = 'C:\\Users\\remar\\Documents\\GitHub\\business-papers-redesign\\demo\\index_demo.html'
directory = 'C:\\Users\\remar\\Documents\\GitHub\\business-papers-redesign\\samples\\HTML'
new_pdf_directory = 'C:\\Users\\remar\\Documents\\GitHub\\business-papers-redesign\\samples\\newPDF'
old_pdf_directory = 'C:\\Users\\remar\\Documents\\GitHub\\business-papers-redesign\\samples\\oldPDF'
new_html_directory = 'C:\\Users\\remar\\Documents\\GitHub\\business-papers-redesign\\samples\\newHTML'
old_html_directory = 'C:\\Users\\remar\\Documents\\GitHub\\business-papers-redesign\\samples\\oldHTML'

# Menu to select table ID to update
print("Select action:")
print("1. Update existing table of Effectives, Committees, Announcements, etc.")
print("2. Populate table of complete papers based on a date.")

action_selection = input("Enter your choice (1 or 2): ")

if action_selection == '1':
    print("Select table to update:")
    print("1. Update table with ID 'Effectives'.")
    print("2. Update table with ID 'Committees'.")
    print("3. Update table with ID 'Announcements'.")
    print("4. Update table with ID 'FDOs'.")
    print("5. Update table with ID 'Call Lists'")
    print("6. Update table with ID 'Votes and Proceedings'")
    print("7. Update table with ID 'Questions Tabled'")
    print("8. Update table with ID 'Early Day Motions'")
    print("9. Update table of complete samples'")

    selection = input("Enter your choice (1-9): ")

    if selection == '1':
        table_id = 'effectives'
    elif selection == '2':
        table_id = 'committees'
    elif selection == '3':
        table_id = 'announcements'
    elif selection == '4':
        table_id = 'FDOs'
    elif selection == '5':
        table_id = 'VnPs'
    elif selection == '6':
        table_id = 'VnPs'
    elif selection == '7':
        table_id = 'questionstabled'
    elif selection == '8':
        table_id = 'calllists'
    elif selection == '9':
        table_id = 'completes'
    else:
        print("Invalid selection. Please choose a number from 1 to 4.")
        exit()

    # Update the HTML table based on user's selection
    update_html_table_with_files(file_path, table_id, directory)

elif action_selection == '2':
    table_id = 'completes'
    
    dates_input = input("Enter dates (YYYY-MM-DD, comma-separated): ")
    dates = [date.strip() for date in dates_input.split(',') if date.strip()]

    if not dates:
        print("No valid dates provided. Exiting.")
        exit()

    # Directories for PDF and HTML links
    directories = {
        'newPDF': new_pdf_directory,
        'oldPDF': old_pdf_directory,
        'newHTML': new_html_directory,
        'oldHTML': old_html_directory
    }

    # Populate the 'completes' table based on user input
    populate_completes_table(file_path, table_id, dates, directories)

else:
    print("Invalid selection. Please choose either 1 or 2.")

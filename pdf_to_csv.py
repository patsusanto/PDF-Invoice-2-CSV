import pdfplumber
import pandas as pd
import re

def clean_text(text):
    """Remove newlines and non-ASCII characters from extracted text."""
    if isinstance(text, str):
        text = text.replace("\n", " ")  # Replace newlines with spaces
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
        return text.strip()
    return text

def extract_tables_from_pdf(pdf_path, csv_path, page_numbers, num_headers):
    tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in page_numbers:
            if page_num > len(pdf.pages) or page_num < 1:
                print(f"Skipping page {page_num}: Out of range.")
                continue
            
            page = pdf.pages[page_num - 1]  # Adjust for zero-based index
            extracted_tables = page.extract_tables()
            
            if extracted_tables:  # Ensure there's at least one table
                table = extracted_tables[0]  # Extract only the first table on the page
                cleaned_table = [[clean_text(cell) for cell in row] for row in table]  # Clean each cell
                
                # Remove first column if it matches the user-defined number of headers
                if cleaned_table and len(cleaned_table[0]) == num_headers:
                    cleaned_table = [row[1:] for row in cleaned_table]

                tables.extend(cleaned_table)  # Append cleaned table

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(tables)
    df.to_csv(csv_path, index=False, header=False)

# Get user input for settings
pdf_file = input("Enter the PDF file path: ")  
csv_file = input("Enter the output CSV file name (add .csv at the end): ")

try:
    num_headers = int(input("Enter the number of headers to check for column removal: "))
    page_numbers = input("Enter the page numbers to extract (comma-separated, e.g., 1,2,3): ")
    page_numbers = [int(p.strip()) for p in page_numbers.split(",")]  # Convert input to list of integers
except ValueError:
    print("Invalid input. Please enter numbers only.")
    exit()

# Run extraction
extract_tables_from_pdf(pdf_file, csv_file, page_numbers, num_headers)
print(f"Data extracted and saved to {csv_file}")

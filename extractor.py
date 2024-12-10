import re
from PyPDF2 import PdfReader, PdfWriter
from pdfminer.high_level import extract_text
from collections import defaultdict

def split_pdf_by_student_id(input_pdf_path, output_dir):
    """
    Splits a PDF into individual files based on student IDs found in the text.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_dir (str): Directory where the individual PDFs will be saved.

    Returns:
        list: List of file paths for the generated PDFs.
    """
    # Regex pattern for a 6-digit student ID
    student_id_pattern = r"\b\d{6}\b"
    
    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    num_pages = len(reader.pages)
    
    # Extract text from the PDF using pdfminer for better text parsing
    extracted_texts = {}
    for page_number in range(num_pages):
        extracted_texts[page_number] = extract_text(input_pdf_path, page_numbers=[page_number])
    
    # Map to store pages associated with each student ID
    student_pages_map = defaultdict(list)
    for page_number, text in extracted_texts.items():
        student_ids = re.findall(student_id_pattern, text)
        if student_ids:
            student_id = student_ids[0]  # Assume the first match is valid
            student_pages_map[student_id].append(page_number)
    
    # Write individual PDFs based on the student ID mapping
    output_paths = []
    for student_id, pages in student_pages_map.items():
        writer = PdfWriter()
        for page_number in pages:
            writer.add_page(reader.pages[page_number])
        
        output_path = f"{output_dir}/{student_id}.pdf"
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        output_paths.append(output_path)
    
    return output_paths

if __name__ == "__main__":
    import os
    import sys
    
    # Ensure the correct arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python split_pdf_by_student_id.py <input_pdf_path> <output_dir>")
        sys.exit(1)
    
    input_pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Split the PDF
    print("Processing PDF...")
    output_files = split_pdf_by_student_id(input_pdf_path, output_dir)
    print(f"PDF split complete. Generated files:")
    for file in output_files:
        print(file)

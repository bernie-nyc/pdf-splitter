import re  # Regular expression library for searching patterns (https://docs.python.org/3/library/re.html)
from PyPDF2 import PdfReader, PdfWriter  # Library to read/write PDF files (https://pypdf2.readthedocs.io/)
from pdfminer.high_level import extract_text  # Tool to extract text reliably from PDF files (https://pdfminersix.readthedocs.io/en/latest/)
from collections import defaultdict  # Creates dictionary-like object with default values (https://docs.python.org/3/library/collections.html#collections.defaultdict)

def split_pdf_by_student_id(input_pdf_path, output_dir):
    """
    Splits a single PDF into separate PDFs for each student based on unique student IDs found within the text.

    Args:
        input_pdf_path (str): Path to the original PDF containing pages for multiple students.
        output_dir (str): Directory path where the individual student PDFs will be stored.

    Returns:
        list: List containing file paths of the newly created individual PDFs.
    """
    # Define a regular expression pattern for identifying student IDs (6-digit numeric IDs).
    student_id_pattern = r"\b\d{6}\b"

    # Load the input PDF file
    reader = PdfReader(input_pdf_path)  # Reads the PDF file for page extraction
    num_pages = len(reader.pages)  # Total number of pages in the PDF

    # Extract readable text from each PDF page using pdfminer (more accurate than PyPDF2)
    extracted_texts = {}
    for page_number in range(num_pages):
        # Extract text from current page_number; pdfminer provides clearer text extraction
        extracted_texts[page_number] = extract_text(input_pdf_path, page_numbers=[page_number])

    # Dictionary mapping each student ID to the pages associated with them
    student_pages_map = defaultdict(list)

    # Iterate over extracted text to find student IDs on each page
    for page_number, text in extracted_texts.items():
        # Find all occurrences of the student ID pattern on this page
        student_ids = re.findall(student_id_pattern, text)
        if student_ids:
            # Assume the first found student ID on a page is the correct one for that page
            student_id = student_ids[0]
            # Map page to the identified student ID
            student_pages_map[student_id].append(page_number)

    # Create separate PDFs for each student ID
    output_paths = []
    for student_id, pages in student_pages_map.items():
        writer = PdfWriter()  # Creates a new PDF file writer

        # Add all pages belonging to the current student to the new PDF
        for page_number in pages:
            writer.add_page(reader.pages[page_number])

        # Define the file path for the new PDF using the student ID as the filename
        output_path = f"{output_dir}/{student_id}.pdf"

        # Save the new PDF file
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        # Store the output path to the list
        output_paths.append(output_path)

    return output_paths

# The following code runs only when this script is executed directly (not imported)
if __name__ == "__main__":
    import os  # Standard Python library for interacting with the operating system (https://docs.python.org/3/library/os.html)
    import sys  # Standard Python library to interact with the command line (https://docs.python.org/3/library/sys.html)

    # Check if exactly two command-line arguments (input PDF path and output directory) are provided
    if len(sys.argv) != 3:
        print("Usage: python split_pdf_by_student_id.py <input_pdf_path> <output_dir>")
        sys.exit(1)  # Exit the program if arguments are incorrect

    # Get input arguments from the command line
    input_pdf_path = sys.argv[1]
    output_dir = sys.argv[2]

    # Ensure the output directory exists; create it if it does not
    os.makedirs(output_dir, exist_ok=True)

    # Start processing the PDF
    print("Processing PDF...")
    output_files = split_pdf_by_student_id(input_pdf_path, output_dir)

    # Notify the user upon completion and list the created files
    print(f"PDF split complete. Generated files:")
    for file in output_files:
        print(file)

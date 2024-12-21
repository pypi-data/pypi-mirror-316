import fitz  # PyMuPDF
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
import magic  # To detect MIME type
import os

def get_mimetype(file_path):
    """
    Detects the MIME type of a file (e.g., document) using python-magic.
    """
    mime = magic.Magic(mime=True)
    mimetype = mime.from_file(file_path)
    return mimetype

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF using PyMuPDF.
    This method handles text extraction from a wide range of PDFs.
    """
    try:
        # Check MIME type of the input PDF file
        mimetype = get_mimetype(pdf_path)
        print(f"Detected MIME type: {mimetype}")

        if not mimetype.startswith('application/pdf'):
            raise ValueError(f"Provided file is not a PDF. MIME type: {mimetype}")

        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF using PyMuPDF: {str(e)}"

def extract_tables_from_pdf(pdf_path):
    """
    Extracts tables from a PDF using pdfplumber.
    This method extracts tables present in the PDF and returns them as a list of dictionaries.
    """
    try:
        # Check MIME type of the input PDF file
        mimetype = get_mimetype(pdf_path)
        print(f"Detected MIME type: {mimetype}")

        if not mimetype.startswith('application/pdf'):
            raise ValueError(f"Provided file is not a PDF. MIME type: {mimetype}")

        with pdfplumber.open(pdf_path) as pdf:
            tables = []
            for page in pdf.pages:
                table = page.extract_tables()
                if table:
                    tables.extend(table)
            return tables
    except Exception as e:
        return f"Error extracting tables from PDF using pdfplumber: {str(e)}"

def extract_text_from_scanned_pdf(pdf_path):
    """
    Extracts text from scanned PDFs (images within PDFs) using OCR with PyTesseract.
    """
    try:
        # Check MIME type of the input PDF file
        mimetype = get_mimetype(pdf_path)
        print(f"Detected MIME type: {mimetype}")

        if not mimetype.startswith('application/pdf'):
            raise ValueError(f"Provided file is not a PDF. MIME type: {mimetype}")

        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                # Use PyTesseract to perform OCR on image-based pages
                img = page.to_image()
                text += img.to_string()
            return text
    except Exception as e:
        return f"Error extracting text from scanned PDF: {str(e)}"

def extract_metadata_from_pdf(pdf_path):
    """
    Extracts metadata such as author, title, and creation date from a PDF file.
    """
    try:
        # Check MIME type of the input PDF file
        mimetype = get_mimetype(pdf_path)
        print(f"Detected MIME type: {mimetype}")

        if not mimetype.startswith('application/pdf'):
            raise ValueError(f"Provided file is not a PDF. MIME type: {mimetype}")

        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        return metadata
    except Exception as e:
        return f"Error extracting metadata from PDF: {str(e)}"

def split_pdf(pdf_path, output_folder):
    """
    Splits a PDF into individual pages and saves them as separate PDF files.
    """
    try:
        # Check MIME type of the input PDF file
        mimetype = get_mimetype(pdf_path)
        print(f"Detected MIME type: {mimetype}")

        if not mimetype.startswith('application/pdf'):
            raise ValueError(f"Provided file is not a PDF. MIME type: {mimetype}")

        reader = PdfReader(pdf_path)
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_path = os.path.join(output_folder, f"page_{i+1}.pdf")
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
        return f"PDF split into {len(reader.pages)} individual pages."
    except Exception as e:
        return f"Error splitting PDF: {str(e)}"

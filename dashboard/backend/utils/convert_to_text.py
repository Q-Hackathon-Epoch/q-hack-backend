import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import pdfplumber
import os


def convert_to_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    text = ""
    file_ext = os.path.splitext(file_path)[1].lower()

    try:
        if file_ext == '.pdf':
            # First try PyMuPDF (faster for most cases)
            try:
                with fitz.open(file_path) as doc:
                    text = "\n".join([page.get_text() for page in doc])
            except Exception as e:
                print(f"PyMuPDF failed, trying pdfplumber: {e}")
                with pdfplumber.open(file_path) as pdf:
                    text = "\n".join([page.extract_text() for page in pdf.pages])

        elif file_ext in ('.html', '.htm'):
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                text = soup.get_text(separator='\n', strip=True)

        else:
            raise ValueError(f"Unsupported file type: {file_ext}. Use PDF or HTML.")

    except Exception as e:
        print(f"Error processing file: {e}")
        return None

    return text
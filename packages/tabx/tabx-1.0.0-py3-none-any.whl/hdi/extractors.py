from .models import (
    get_tesseract_text,
    get_doctr_text,
    get_camelot_table,
    get_tabula_table,
    summarize_text
)
from pdf2image import convert_from_path


def extract_table_from_pdf(pdf_path, method="camelot"):
    """Extract tables from a PDF file."""
    try:
        if method == "camelot":
            return get_camelot_table(pdf_path)
        elif method == "tabula":
            return get_tabula_table(pdf_path)
        else:
            raise ValueError("Invalid method. Choose 'camelot' or 'tabula'.")
    except Exception as e:
        print(f"[Error - PDF Extraction]: {e}")
        return None


def extract_table_from_image(image_path, method="tesseract"):
    """Extract tables or text from an image."""
    try:
        if method == "tesseract":
            return get_tesseract_text(image_path)
        elif method == "doctr":
            return get_doctr_text(image_path)
        else:
            raise ValueError("Invalid method. Choose 'tesseract' or 'doctr'.")
    except Exception as e:
        print(f"[Error - Image Extraction]: {e}")
        return None


def extract_text_from_image(image_path, method="tesseract"):
    """Extract plain text from an image."""
    return extract_table_from_image(image_path, method=method)


def extract_text_from_pdf(pdf_path, method="tesseract"):
    """Extract text from a PDF by converting it to images."""
    try:
        images = convert_from_path(pdf_path)
        text = ""
        for image in images:
            text += extract_text_from_image(image, method=method)
        return text
    except Exception as e:
        print(f"[Error - PDF to Text]: {e}")
        return None


def summarize_pdf_text(pdf_path, method="tesseract"):
    """Summarize text extracted from a PDF."""
    text = extract_text_from_pdf(pdf_path, method=method)
    if text:
        return summarize_text(text)
    return None


def save_to_excel(data, output_path="output.xlsx"):
    """Save extracted tables to an Excel file."""
    import pandas as pd

    try:
        with pd.ExcelWriter(output_path) as writer:
            for i, table in enumerate(data):
                pd.DataFrame(table).to_excel(writer, sheet_name=f"Sheet{i+1}")
        print(f"[Success]: Data saved to {output_path}")
    except Exception as e:
        print(f"[Error - Save to Excel]: {e}")

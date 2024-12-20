from setuptools import setup, find_packages

setup(
    name="tabx",
    version="1.0.0",
    description="Advanced Table Extraction and Text Recognition Library",
    author="Tanmay Dumbre",
    author_email="tanmaymdumbrek@gmail.com",
    packages=find_packages(),
    install_requires=[
        "opencv-python",        # For image processing
        "numpy",                # For numerical operations
        "pandas",               # For handling tables and data
        "pytesseract",          # For OCR text extraction from images
        "doctr",                # Advanced document OCR extraction
        "camelot-py[cv]",       # Extracting tables from PDFs
        "tabula-py",            # Extracting tables from PDFs (Java-based)
        "openpyxl",             # For saving extracted tables to Excel
        "transformers",         # Hugging Face Transformers for AI processing
        "torch",                # Deep learning backend
        "pillow",               # For image handling
        "pdf2image",            # Convert PDFs to images
    ],
    python_requires=">=3.7",
)

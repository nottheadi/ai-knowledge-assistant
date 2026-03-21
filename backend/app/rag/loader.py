"""
PDF loader utility for extracting documents from PDF files.
"""

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    """
    Load a PDF file and extract its documents.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        list: List of loaded document objects.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

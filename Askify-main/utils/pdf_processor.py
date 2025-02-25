
from langchain_community.document_loaders import PyPDFLoader

"""
This module provides a function `load_pdf` to load and process PDF documents.

It utilizes the `PyPDFLoader` class from the `langchain_community.document_loaders` library.
"""


def load_pdf(file_path: str) -> PyPDFLoader.load:
    """
    Loads a PDF document from the specified file path.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list or str:
            * If successful, returns a list containing the extracted content
              from each page of the PDF.
            * If the file is not found, returns the string "The Given File is does not exist".
            * If any other exception occurs, returns the exception object itself.
    """

    try:
        # Loading a PDF file from the specified path
        loader = PyPDFLoader(file_path)

        # Extracting the content from the PDF
        docs = loader.load()

        # Checking the number of pages loaded
        return docs
    except FileNotFoundError:
        return "The Given File is does not exist"

    except Exception as e:
        return e


if __name__ == "__main__":
    """
    Example usage demonstrating how to load a PDF and access its content (page 0 in this case).
    """

    docs = load_pdf("C:/Users/HP/OneDrive/Desktop/Askify-main/Askify-main/upload")

    if isinstance(docs, list):
        # Access content of the first page (assuming valid data)
        print("Docs", docs)
        print("docs[0]",docs[0])
        print("docs[0].page_content",docs[0].page_content)
    else:
        print(f"Error: {docs}")  # Print the error message if loading failed

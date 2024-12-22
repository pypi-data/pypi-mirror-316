"""
-----------------------------------------------------------------------------
Module Name: zbinfigs
Submodule Name: utils.py
Description: Utility functions for pdf analysis and file management.
Author: Isaac Spackman
Date Created: December 8, 2024
Last Modified: December 8, 2024
Version: 0.0.0
License: MIT
-----------------------------------------------------------------------------
"""

import shutil
import os
import pandas as pd
import logging
from .collection import *
from typing import Tuple, List
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from tqdm import tqdm


def read_collection(csvfile: str) -> collection.Collection:
    return collection.Collection(csvfile)

def process_pdf_folder(pdfs_folder: str, file_range: Tuple[int, int]) -> None:
    """
    Processes PDF files in the given folder, converts them to Markdown, and extracts images.
    
    Args:
        pdfs_folder (str): The folder containing the PDF files to be processed.
        file_range (Tuple[int, int]): The range of files (inclusive) to process (start, end).
    """
    # Initialize logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    # Get the list of valid PDF files
    pdf_files = _get_valid_pdf_files(pdfs_folder)
    if not pdf_files:
        logger.warning("No valid PDF files found in the folder.")
        return

    # Select the range of files to process
    selected_files = _select_files_in_range(pdf_files, file_range)
    if not selected_files:
        logger.warning(f"No files selected in the specified range: {file_range}")
        return

    # Create the converter object for processing
    converter = PdfConverter(artifact_dict=create_model_dict())

    # Process each selected file
    for file in tqdm(selected_files, desc="Processing PDFs", unit="file"):
        try:
            logger.info(f"Processing file: {file}")
            _process_single_pdf(file, converter, pdfs_folder, logger)
        except Exception as e:
            logger.error(f"Error processing {file}: {e}")

def _get_valid_pdf_files(pdfs_folder: str) -> List[str]:
    """
    Retrieves a sorted list of valid PDF files in the specified folder.
    
    Args:
        pdfs_folder (str): The folder to search for PDF files.
    
    Returns:
        List[str]: A list of valid PDF file paths sorted by filename.
    """
    logger = logging.getLogger(__name__)
    files = [f for f in os.listdir(pdfs_folder) if _is_valid_pdf_filename(f)]
    
    if not files:
        logger.warning("No valid PDF files found in the folder.")
    
    # Sort files by name to ensure consistent processing
    return sorted(files)

def _is_valid_pdf_filename(filename: str) -> bool:
    """
    Checks if a filename starts with 8 alphanumeric characters followed by an optional underscore.
    
    Args:
        filename (str): The filename to check.
    
    Returns:
        bool: True if the filename matches the expected pattern, False otherwise.
    """
    return filename[:8].isalnum() and filename[8:9] in ['_', ''] and filename.endswith('.pdf')

def _select_files_in_range(files: List[str], file_range: Tuple[int, int]) -> List[str]:
    """
    Selects a subset of files based on the provided range (inclusive).
    
    Args:
        files (List[str]): A list of files to select from.
        file_range (Tuple[int, int]): A tuple containing the start and end indices (inclusive).
    
    Returns:
        List[str]: A list of files selected by the range.
    """
    start, end = file_range
    if start < 0 or end >= len(files):
        raise ValueError(f"Invalid range: {file_range}, available files: 0 to {len(files)-1}")
    return files[start:end+1]

def _process_single_pdf(pdf_file: str, converter: PdfConverter, pdfs_folder: str, logger: logging.Logger) -> None:
    """
    Converts a single PDF to Markdown and saves the output in a folder named by the first 8 characters of the filename.
    
    Args:
        pdf_file (str): The path to the PDF file to process.
        converter (PdfConverter): The converter instance used to process the PDF.
        pdfs_folder (str): The folder where the PDF file is located.
        logger (logging.Logger): The logger instance to use for logging events.
    """
    # Get the first 8 characters of the filename to use as the folder name
    folder_name = pdf_file[:8]
    output_folder = os.path.join(pdfs_folder, folder_name)
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process the PDF to get rendered text and images
    try:
        rendered = converter(os.path.join(pdfs_folder, pdf_file))
        text, _, images = text_from_rendered(rendered)

        # Save the original PDF
        shutil.copy(os.path.join(pdfs_folder, pdf_file), output_folder)

        # Save the Markdown text
        markdown_file = os.path.join(output_folder, f"{folder_name}.md")
        with open(markdown_file, 'w', encoding='utf-8') as md_file:
            md_file.write(text)

        # Save extracted images
        _save_extracted_images(images, output_folder)

        logger.info(f"Successfully processed and saved files for {pdf_file}.")

    except Exception as e:
        logger.error(f"Error processing PDF {pdf_file}: {e}")

def _save_extracted_images(images: List[str], output_folder: str) -> None:
    """
    Saves the extracted images to the output folder.
    
    Args:
        images (List[str]): A list of paths to the extracted images.
        output_folder (str): The folder where the images should be saved.
    """
    for img_name, img in images.items():
        try:
            img_path = os.path.join(output_folder, f"{output_folder}_{img_name}")
            img.save(img_path)
        except Exception as e:
            logging.error(f"Error saving image: {e}")


def gather_figures():
    # locate the image files for the .pdfs in the range selected
    # and merge into a single .pdf 
    # export the page ranges for each record to a .csv
    return

def merge_summary_pdfs():
    # merge pdfs into a single document and make an updated
    # page range metadata file
    return

def sort_annotated():
    # locate the images based on their annotations and sort into 
    # folders accordingly - rename the figures to avoid name clashes
    return

def add_annotations():
    # add annotations to the main .csv file
    return

"""
-----------------------------------------------------------------------------
Module Name: zbinfigs
Submodule Name: collections.py
Description: A collections class to read and parse zotero collection .csv 
             and annotated .csv data.
Author: Isaac Spackman
Date Created: December 8, 2024
Last Modified: December 8, 2024
Version: 0.00
License: MIT
-----------------------------------------------------------------------------
"""
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Optional
from xhtml2pdf import pisa
from bs4 import BeautifulSoup
import logging
import shutil
import os


class Collection:
    def __init__(self, csvfile: str):
        """
        Initializes the Collection object by reading a CSV file into a pandas DataFrame.

        Args:
            csvfile (str): The path to the CSV file to be loaded.
        """
        self.df = pd.read_csv(csvfile)

        # Initialize logging with a specific configuration
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)

    def _check_record_files(self, row: pd.Series) -> Optional[str]:
        """
        Checks if any valid PDF or HTML file exists for a given record.

        Args:
            row (pd.Series): A row from the DataFrame containing the file attachments.

        Returns:
            Optional[str]: The path to the valid file if found, else None.
        """
        files = row.get('File Attachments')

        # Check if there are any file attachments
        if pd.isna(files):
            self.logger.warning(f'No files found for {row["Title"]}.')
            return None

        file_list = [f.strip() for f in files.split(";")]

        # Check for PDF files
        pdf_files = [f for f in file_list if f.lower().endswith(".pdf")]
        for pdf in pdf_files:
            if os.path.exists(pdf):
                self.logger.info(f'The .pdf file exists for {row["Title"]}: {pdf}')
                return pdf
            else:
                self.logger.warning(f'The .pdf file does not exist for {row["Title"]}: {pdf}')
        
        # Check for HTML files if no valid PDF found
        html_files = [f for f in file_list if f.lower().endswith(".html")]
        for html in html_files:
            if os.path.exists(html):
                self.logger.info(f'Using the HTML file for {row["Title"]}: {html}')
                return html
            else:
                self.logger.warning(f'The HTML file does not exist for {row["Title"]}: {html}')

        # If no valid files were found
        self.logger.warning(f'No valid file found for {row["Title"]}.')
        return None

    def _remove_css_from_html(self, html_content: str) -> str:
        """
        Removes inline styles, <style> tags, and <link> tags with rel="stylesheet" 
        from the provided HTML content.

        Args:
            html_content (str): The raw HTML content to be cleaned.

        Returns:
            str: The cleaned HTML content without CSS.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove inline styles
        for tag in soup.find_all(True):
            tag.attrs = {key: value for key, value in tag.attrs.items() if key != 'style'}
        
        # Remove <style> tags
        for style in soup.find_all('style'):
            style.decompose()
        
        # Remove <link> tags with rel="stylesheet"
        for link in soup.find_all('link', rel='stylesheet'):
            link.decompose()
        
        return str(soup)

    def _html_to_pdf(self, input_html_file: str, output_pdf_file: str) -> None:
        """
        Reads an HTML file, removes CSS, and converts the cleaned HTML to a PDF.

        Args:
            input_html_file (str): The input HTML file path to be processed.
            output_pdf_file (str): The output PDF file path where the result will be saved.

        Returns:
            None
        """
        try:
            with open(input_html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Clean the HTML by removing CSS
            cleaned_html = self._remove_css_from_html(html_content)

            # Convert the cleaned HTML to PDF
            with open(output_pdf_file, 'wb') as pdf:
                pisa_status = pisa.CreatePDF(cleaned_html, dest=pdf)
            
            if pisa_status.err:
                self.logger.error(f"Error converting HTML to PDF: {output_pdf_file}")
            else:
                self.logger.info(f"PDF successfully created: {output_pdf_file}")
        
        except Exception as e:
            self.logger.error(f"Error processing HTML to PDF for {input_html_file}: {e}")

    def export_pdfs_to_folder(self, folder: str = "collection_pdfs") -> None:
        """
        Exports PDFs to the specified folder. This method processes each row in the DataFrame,
        checks if the file is a PDF or HTML file, and either copies the PDF or converts the HTML to PDF.

        Args:
            folder (str): The destination folder for the files. Default is "collection_pdfs".
        """
        # Ensure the folder exists
        os.makedirs(folder, exist_ok=True)

        for idx, row in self.df.iterrows():
            record_file = self._check_record_files(row)
            if record_file:
                if record_file.endswith(".html"):
                    dst = os.path.join(folder, f"{row['Key']}_HTML.pdf")
                    try:
                        self._html_to_pdf(record_file, dst)
                        self.logger.info(f"Converted HTML file for record {row['Key']}")
                    except Exception as e:
                        self.logger.error(f"Error converting HTML to PDF for record {row['Key']}: {e}")
                
                elif record_file.endswith(".pdf"):
                    dst = os.path.join(folder, f"{row['Key']}.pdf")
                    try:
                        shutil.copy(record_file, dst)
                        self.logger.info(f"Copied PDF file for record {row['Key']}")
                    except Exception as e:
                        self.logger.error(f"Error copying PDF file for record {row['Key']}: {e}")
                
                else:
                    self.logger.warning(f"Unsupported file type for record {row['Key']}: {record_file}")
            else:
                self.logger.warning(f"No files found for record {row['Key']}")

    
    def _get_file_type_counts(self) -> Dict[str, Dict[int, int]]:
        """
        Helper method to gather file type counts (PDF, HTML, or No File) by year.

        This method will count the number of records with each file type (PDF, HTML, None) for each publication year.

        Returns:
            Dict[str, Dict[int, int]]: A dictionary with file types as keys and a dictionary of counts for each year.
        """
        file_type_counts = {"pdf": {}, "html": {}, "none": {}}

        for _, row in self.df.iterrows():
            record_file = self._check_record_files(row)

            if record_file:
                year = row.get('Publication Year')

                if pd.isna(year):
                    self.logger.warning(f"Missing publication year for record {row['Key']}")
                    continue

                if record_file.lower().endswith(".pdf"):
                    file_type = "pdf"
                elif record_file.lower().endswith(".html"):
                    file_type = "html"
                else:
                    file_type = "none"

                # Count occurrences by year
                file_type_counts[file_type][year] = file_type_counts[file_type].get(year, 0) + 1
            else:
                self.logger.warning(f"No valid file found for record {row['Key']}")

        return file_type_counts

    def plot_pdfs_available(self, plot_type: str = "bar", x_axis: Optional[str] = "year") -> plt.Figure:
        """
        Plots the number of available PDF files and HTML files relative to the total number of records.

        This function can generate either a bar chart (stacked by year) or a pie chart (summarizing all years).
        
        Args:
            plot_type (str): Type of plot to generate. Either "bar" or "pie". Defaults to "bar".
            x_axis (Optional[str]): The axis to plot on for the bar chart. Default is "year".

        Returns:
            plt.Figure, plt.Axis: The figure and axis object containing the plot.
        """
        # Get file type counts by year
        file_type_counts = self._get_file_type_counts()

        if plot_type == "bar":
            return self._plot_stacked_bar_chart(file_type_counts, x_axis)
        elif plot_type == "pie":
            return self._plot_pie_chart(file_type_counts)
        else:
            self.logger.error(f"Invalid plot type: {plot_type}. Must be 'bar' or 'pie'.")
            raise ValueError("Invalid plot type. Choose 'bar' or 'pie'.")

    def _plot_stacked_bar_chart(self, file_type_counts: Dict[str, Dict[int, int]], x_axis: str) -> plt.Figure:
        """
        Helper method to plot a stacked bar chart for file types by year.

        Args:
            file_type_counts (Dict[str, Dict[int, int]]): Dictionary of file type counts by year.
            x_axis (str): The axis to plot on (typically 'year').

        Returns:
            plt.Figure: The figure object containing the stacked bar chart.
        """
        years = sorted(set(self.df['Publication Year'].dropna()))
        pdf_counts = [file_type_counts['pdf'].get(year, 0) for year in years]
        html_counts = [file_type_counts['html'].get(year, 0) for year in years]
        none_counts = [file_type_counts['none'].get(year, 0) for year in years]

        fig, ax = plt.subplots()
        ax.bar(years, pdf_counts, label="PDF", color="blue")
        ax.bar(years, html_counts, bottom=pdf_counts, label="HTML", color="orange")
        ax.bar(years, none_counts, bottom=[i + j for i, j in zip(pdf_counts, html_counts)], label="No File", color="gray")

        ax.set_xlabel(x_axis)
        ax.set_ylabel('Record Count')
        ax.set_title('PDF and HTML Availability by Year')
        ax.legend()

        self.logger.info("Stacked bar chart plotted successfully.")
        return fig, ax

    def _plot_pie_chart(self, file_type_counts: Dict[str, Dict[int, int]]) -> plt.Figure:
        """
        Helper method to plot a pie chart summarizing the total file types across all years.

        Args:
            file_type_counts (Dict[str, Dict[int, int]]): Dictionary of file type counts by year.

        Returns:
            plt.Figure: The figure object containing the pie chart.
        """
        total_pdf = sum(file_type_counts['pdf'].values())
        total_html = sum(file_type_counts['html'].values())
        total_none = sum(file_type_counts['none'].values())

        labels = ['PDF', 'HTML', 'No File']
        sizes = [total_pdf, total_html, total_none]
        colors = ['blue', 'orange', 'gray']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

        ax.set_title('Distribution of File Types Across All Years')

        self.logger.info("Pie chart plotted successfully.")
        return fig, ax

    def plot_annotations():
        # make a plot of the distribution of annotations based on the records
        # that could be processed
        return
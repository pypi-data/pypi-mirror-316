# Zbinfigs
Version : 0.1.7  
  
## Overview
zbinfigs is a python code designed to facilitate classification of scholarly articles stored in zotero collections. 
The code input is a .csv exported from a zotero collection. The code allows for several options:  
  1. Organize and compile .pdfs
  2. Extract images to summary .pdf
  3. Read annotations
  4. Train and test classifier

### Organize and Compile
A raw zotero collection may not have .pdf files for all records, and for those that have .pdf files not all may be accessible. 
In the organize and compile option, the program reads a default .csv describing a zotero collection and checks all of the file links.
Where no files are available, this flag is written to a summary document. If only .html files are available, the program strips the CSS 
from the file and converts it to a .pdf file. At the end of the program execution, all available .pdf files are written to a common folder. 
This can be useful to transfer data to an HPC system for further analysis.  

### Extract Images 
From a folder of .pdf files and the original exported zotero .csv file, the program uses the **marker** package to convert to markdown and 
extract the figure images. The figure images for the entire directory are stitched into a single .pdf file for review and annotation. 
The converted text and original image files are retained for further semantic analysis. This step may be broken into chunks for parallel processing 
on an HPC system.

### Read Annotations 
The program takes an annotations input file that contains the .pdf page number for all figures that match from manual annotation. 
These annotations are then connected with the original zotero collection .csv file and summary stats written.  

### Train and Test Classifier  
From the annotated dataset, several classifiers are applied and summary performance written.  
  
  
# Examples  
This is a sketch of the planned usage - this will probably change.  
  
**File Preparation**
```python
import zbinfigs as zbf

# read the collection into a collection object
collection = zbf.read_collection("mycollection.csv")

# export the collection .pdfs to a common folder
collection.export_pdfs_to_folder(folder_name="mypdfs")

```
**Figure Extraction**  
This is the slowest step and should be parallelized if possible.
```python
import zbinfigs as zbf
import sys

# get the minimum and maximum file indices to process
rmin, rmax = sys.argv[0], sys.argv[1]

# read the pdfs in the range selected and convert to markdown + extract images
# the result is a folder for each .pdf
zbf.process_pdf_folder(folder_name="mypdfs", range=(rmin, rmax))
```

**Figure Compilation**
```python
import zbinfigs as zbf
import sys

# get the minimum and maximum file indices to process
rmin, rmax = sys.argv[0], sys.argv[1]

# locate the image files for the .pdfs in the range selected and merge into a single .pdf
# export the page ranges for each record to a .csv
zbf.gather_figures(folder_name="mypdfs", range=(rmin, rmax))

# merge pdfs into a single document and make an updated page range .csv file
# this knows to look for the .csv page number metadata
zbf.merge_summary_pdfs(folder_name="mypdfs")
```

**Read Annotations**
```python
import zbinfigs as zbf

# locate the raw images based on their annotations and sort into folders accordingly
# this expects a summary pdf .csv of page range data to match with
zbf.sort_annotated(folder_name="mypdfs", annotations="myannotations.csv")

# add annotations to the main .csv
zbf.add_annotations(collection="mycollection.csv", 
                    annotations="myannotations.csv", 
                    outfile="myannotatedcollection.csv")
```

**Analysis**
```python
import zbinfigs as zbf


collection = zbf.read_collection("myannotatedcollection.csv")

# make a pie chart of the total number of records
# sections for .html files and .pdf files available
collection.plot_pdfs_available(type="bar", x="year")
collection.plot_pdfs_available(type="pie")


# make a pie chart of the total number of records analyzed
# sections for each annotation condition
collection.plot_annotations(type="bar", x="year")
collection.plot_annotations(type="pie")

# make a plot of the annotation type v. the document processed
collection.plot_annotations(type="bar", x="pdf_html")
```  
  
**Train and Test Classifier**  
This shows an example of using several different image classification strategies implemented in sklearn on the resulting dataset. Uniquely, this system can also apply OCR to an image and use the result to aid classification.  
  

```python
# implement some stuff here
# if the OCR turns up a key term (like axis titles or units that are conserved by figure type)  
# skip the image classification and directly assign to a group

# make useful summary plots that classify performance, false positives, etc.  
```
  
## Future Plans  
 - An example semantic analysis / clustering would be nice  
    This would use the markdown text generated during the previous step and extract the region where the paper is from, author information or any number of other characteristics (paper length?). It may also check for linguistic similarities among the papers that match the annotation conditions, and potential differences with the remaining papers as an alternative classification approach.  
  - Unit tests for all functions
  - Code linting
  - Continuous integration for package deployment
  - More documentation on annotation examples
  - Tutorial script  
  - Prepare for RSE presentation?  
  - Parallelization of pdf processing with mpi4py (platform agnostic)
  - Robust try/except error handling with logging information
  
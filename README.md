# Zendesk Ticket Comments to CSV

## About
This script was created in order to extract data from both Zendesk `comments` and `ticket` nodes -- exported from the tickets.xml file(s) -- and have that data cleanly exported to legible CSV files. There were no simplified tools that were able to achieve what I was looking to perform this task, so  script was written to achieve purpose.

The script allows you to specify a set of arguments to customize the output of your CSV. More importantly, one of the script's important functions is the ability to "rotate" CSV files once the defined `max_file_size` argument has been set. This will allow the segmentation of multiple files split across the set limit to avoid having a single large CSV file, allowing batches to be created instead.

New files created during the rotation process will automatically be appended with the defined header as the firstrow.

## Example
### Specifying Arguments
Arguments can be easily adjusted within the script by making changes to the following lines:
```python
args = {'directory': '',    # Output directory
        'filename': 'output.csv',   # Name of the output file
        'max_file_size': 5142880,   # File size in bytes (default is set to 5 MB)
        'header': ['Zendesk_ID', 'Created_Date', 'Author_ID', 'Comments'], # Header(s) to use
        }
```

In the case your are expecting various CSV files to be created during the rotation, file will be created using the filename structure `01_output.csv`, `02_output.csv`, etc.

### Usage
```python
python xml-to-csv.py file-to-parse.xml
```
**Note:** Currently, the file *only*  checks for XML files.

## TODO
- Adjust script to take arguments from the cli

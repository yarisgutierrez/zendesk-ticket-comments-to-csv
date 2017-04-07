#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Yaris Alex Gutierrez"
__email__ = "yarisgutierrez@gmail.com"
__license__ = "MIT"

# Export defined nodes from an XML file into a CSV. This script is designed
# to break up large CSV files into chunks once the set file size has been met.
# This script was created specifically to extract comment data from Zendesk
# ticket XML files into CSV files to allow importing into other systems (e.g.
# SalesForce)
# Usage Example: python xml_to_csv.py file_to_parse.xml

import os
import sys

from xml.etree import ElementTree as ET
import csv

xml_file = sys.argv[1]

if not xml_file.endswith('.xml'):
    print "%s is not a valid XML file. Exiting." % xml_file
    exit()

tree = ET.parse(xml_file)
root = tree.getroot()

# Ignore characters/string(s) (if any)
ignore_chars = ['>', '>>']


class RotateFile(object):
    """Rotates to new CSV file once defined file size is exceeded.

    Typical use:

        args = {'directory': '/some/dir',
                'filename': 'filenamename.csv',
                'max_file_size': 123456,  # File size in bytes
                'header': 'FirstColumnName', # CSV header. List can be used
                }

        output = RotateFile(**args)
        (...)
    """
    def __init__(self, directory='', filename='', max_files=sys.maxint,
                 max_file_size='', header=''):
        self.ii = 1
        self.header = header
        self.directory, self.filename = directory, filename
        self.max_file_size, self.max_files = max_file_size, max_files
        self.finished, self.fh = False, None
        self.open()

    def rotate(self):
        """Rotate the file, if necessary"""
        if (os.stat(self.filename_template).st_size > self.max_file_size):
            self.close()
            self.ii += 1
            if (self.ii <= self.max_files):
                self.open()
            else:
                self.close()
                self.finished = True

    def open(self):
        self.fh = open(self.filename_template, 'w')
        self.writer = csv.writer(self.fh)
        self.writer.writerow(self.header)

    def write(self, text=""):
        self.writer = csv.writer(self.fh)
        self.writer.writerow([s.encode("utf-8") for s in text])
        self.fh.flush()
        self.rotate()

    def close(self):
        self.fh.close()

    @property
    def filename_template(self):
        return "%0.2d" % self.ii + "_" + self.filename


def comments():
    for comment in root.iter('comment'):
        created_at = comment.find("created-at").text
        value = comment.find("value").text
        author_id = comment.find("author-id").text
        if not value:
            continue
        yield created_at, value, author_id


def tickets(root):
    for ticket in root.iter('ticket'):
        nice_id = ticket.find("nice-id").text
        for comment in comments():
            created_at, value, author_id = comment
            yield nice_id, created_at, author_id, value


# Set arguments
args = {'directory': '',
        'filename': 'output.csv',
        'max_file_size': 5142880,
        'header': ['Zendesk_ID', 'Created_Date', 'Author_ID', 'Comments'],
        }

fout = RotateFile(**args)

for row in tickets(root):
    # The if statement below can be omitted from the code if no characters
    # are being defined in the ingore_chars variable above. If this is the
    # case, ensure that the proper indentation is set.
    if not any(ignore_chars in row for ignore_char in ignore_chars):
        print ', '.join(row)
        fout.write(row)

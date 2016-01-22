#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Remove rowspans from all tables in a page
# Should probably expand this to deal with colspans too
# Should also copy full tag contents from the first rowspan to
# subsequent rows.
# Example:
# curl -s 'https://en.wikipedia.org/wiki/List_of_2015_albums' | normalize-rows.py

from bs4 import BeautifulSoup
import sys
import argparse

def fix_rows_with_rowspan(rows, column, contents):
    """delete the rowspan from the first row"""
    del(rows[0].find_all('td')[column]['rowspan'])
    """Copy the contents of the rowspan down through the slice of rows from the caller"""
    """Ignore the first row because the contents are already there"""
    for row_number, row in enumerate(rows):
        if row_number != 0:
            row.find_all('td')[column].contents = contents

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('html', nargs='?', type=argparse.FileType('rb'),
                        default=sys.stdin, help="HTML from pipeline", metavar="HTML")
    args = parser.parse_args()
    
    html = BeautifulSoup(args.html.read(), "html.parser")
    rows = html.find_all('tr')
    for row_number, row in enumerate(rows):
        """Check for rowspan in row"""
        tr_with_rowspan = row.find_all('td', rowspan=True) 
        if tr_with_rowspan:
            """if the row has a rowspan, identify the column/td it is in"""
            for column_number, td in enumerate(tr_with_rowspan):
                if td.has_attr('rowspan'):
                    rowspan_value = int(td['rowspan'])
                    contents = td.contents
                    """Take a slice of rows covered by the rowspan"""
                    """The rowspan will be the first item in the list sent to fix_rows_with_rowspan"""
                    fix_rows_with_rowspan(rows[row_number:(row_number + rowspan_value)], column_number, contents)

    result = str(html)
    try:
        sys.stdout.write(result + "\n")
        sys.stdout.flush()
    except IOError:
        pass

if __name__ == "__main__":
    exit(main())

"""
Functions for exploring the data
"""

import pre_processing

if __name__ == "__main__":
    filepath = '/home/james/projects/dite_swim_data/raw_data/20181020-Swimming Classification Data.xlsx'
    series = pre_processing.load_raw_spreadsheet(filepath)
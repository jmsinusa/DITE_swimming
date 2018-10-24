"""
Functions for exploring the data
"""

import pre_processing
import os
import settings
from matplotlib import pyplot as plt
import seaborn as sns


if __name__ == "__main__":
    filepath = os.path.join(settings.LOCAL_DATA_DIR, '20181020_preliminary.xlsx')
    series = pre_processing.load_raw_spreadsheet(filepath)
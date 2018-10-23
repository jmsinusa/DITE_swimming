# DITE_swimming
Analysis of swimming time series data

## Pre-processing

#### pre_processing.load_raw_spreadsheet
Verifies that spreadsheet is in exactly the expected format, otherwise raises `AssertionError`.
Returns series, a dictionary containing the elapsed time (in seconds), the 12 dimensional sensor data, one classification target and one event target per row.

    import pre_processing
    series = pre_processing.load_raw_spreadsheet(filepath)

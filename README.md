# DITE_swimming
Analysis of swimming time series data

## Prerequisits
| Package         | Version |
| --------------- | ------- |
| numpy           | 1.15.3  | 
| pandas          | 0.23.4  |
| python-dateutil | 2.7.3   |
| pytz            | 2018.5  |
| six             | 1.11.0  |
| xlrd            | 1.1.0   |

## Pre-processing

#### pre_processing.load_raw_spreadsheet
Verifies that spreadsheet is in exactly the expected format, otherwise raises `AssertionError`.
Returns series, a dictionary containing the elapsed time (in seconds), the 12 dimensional sensor data, one classification target and one event target per row.

    import pre_processing
    series = pre_processing.load_raw_spreadsheet(filepath)
    series.keys()

    dict_keys(['subject_cat', 'stroke_phase_def', 'true_time', 'elapsed_time', 'swim_class_def', 'stroke_phase', 'sensor_vals', 'cols', 'swim_class'])

"""
Load raw data into numpy
"""

import numpy as np
import pandas as pd
from datetime import datetime


GYRO_COLS = [
    'R Wrist X Gyro', 'R Wrist Y Gyro', 'R Wrist Z Gyro', 'R Wrist X Accel',
    'R Wrist Y Accel', 'R Wrist Z Accel', 'Back X Gyro', 'Back Y Gyro', 'Back Z Gyro',
    'Back X Accel', 'Back Y Accel', 'Back Z Accel'
]


def load_raw_spreadsheet(filepath):
    """
    Load spreadsheet
    :param filepath: Full path to spreadsheet
    :return: dict containing:
        ture_time: datetime.datetime objects giving actual time (ignore date)
        elapsed_time: Elapsed time for this series, in seconds.
        cols: Name of the 12 columns that make up the sensor vals
        sensor_vals: numpy array of sensor values for 12 sensors, at each time step
        swim_class: The classification target: Each row with a swim class
        swim_class_def: Definitions for the four swim classes
        stroke_phase: Stroke events. Most are zero (null). Others are 1 - 8.
        stroke_phase_def: Stroke event defintions.
        subject_cat: Category of subject (Elite)
    """
    # Preprocess
    try:
        verify_spreadsheet(filepath)
    except AssertionError as err:
        print("\nSpreadsheet has failed validation.")
        print(err)
        raise

    df = pd.read_excel(filepath, header=None, skiprows=11, usecols=[0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17],
                       names=['time', 'R Wrist X Gyro', 'R Wrist Y Gyro', 'R Wrist Z Gyro', 'R Wrist X Accel',
                              'R Wrist Y Accel', 'R Wrist Z Accel', 'Back X Gyro', 'Back Y Gyro', 'Back Z Gyro',
                              'Back X Accel', 'Back Y Accel', 'Back Z Accel', 'Swim class', 'Stroke class'])

    ## FIXME: 12hr time format will break if activity spans midday or midnight??

    df['time'] = df['time'].apply(lambda x: _format_time(x))
    elapsed_time = df['time'].apply(lambda x: (x - df['time'][0]).total_seconds())
    elapsed_time = np.array(elapsed_time.values)
    # cast time array to a datetime.time object
    time_arr = np.array(df['time'].apply(lambda x: x.time()).values)
    series = {'true_time': time_arr, 'elapsed_time': elapsed_time, 'cols': list(df.columns[1:-2])}
    series['sensor_vals'] = np.array(df.iloc[:,1:-2].values).T
    series['sensor_vals'] = df[GYRO_COLS]
    series['swim_class'] = np.array(df['Swim class'].values)
    series['swim_class_def'] = {1: 'Not swimming', 2: 'Swimming', 3: 'Push off event', 4: 'Turn event'}
    series['stroke_phase_def'] = {0: 'No event', 1: 'R Hand Entry', 2: 'R Start of Down Sweep', 3: 'R Catch', 4: 'R Recovery',
                                  5: 'L Hand Entry', 6: 'L Start of Down Sweep', 7: 'L Catch', 8: 'L Recovery'}
    series['stroke_phase'] = np.array(df['Stroke class'].values, dtype=np.int8) # Note: This forces null to 0.
    series['subject_cat'] = df.iloc[0][1]

    # Normalise sensor_vals to mean=0 std=1
    vals = series['sensor_vals']
    means = np.mean(vals, axis=1)
    means2 = np.tile(np.expand_dims(means, 1), (1, vals.shape[1]))
    stds = np.std(vals, axis=1)
    std2 = np.tile(np.expand_dims(stds, 1), (1, vals.shape[1]))
    newvals = (vals - means2) / std2
    series['sensor_vals_normed'] = newvals
    return series


def verify_spreadsheet(filepath):
    """
    Ensure that spreadsheet conforms to known standard.
    Raises IOError if not
    :param filepath:
    :return:
    """
    df = pd.read_excel(filepath, header=None, nrows=11)
    assert df.iloc[0][0] == 'Category'
    assert df.iloc[0][7] == 'Swimming Classification'
    assert df.iloc[0][9] == 1
    assert df.iloc[1][9] == 2
    assert df.iloc[2][9] == 3
    assert df.iloc[3][9] == 4
    assert df.iloc[0][10] == 'Not Swimming'
    assert df.iloc[1][10] == 'Swimming'
    assert df.iloc[2][10] == 'Push Off Event'
    assert df.iloc[3][10] == 'Turn event '
    assert int(df.iloc[0][15]) == 1
    assert int(df.iloc[1][15]) == 2
    assert int(df.iloc[2][15]) == 3
    assert int(df.iloc[3][15]) == 4
    assert int(df.iloc[4][15]) == 5
    assert int(df.iloc[5][15]) == 6
    assert int(df.iloc[6][15]) == 7
    assert int(df.iloc[7][15]) == 8
    assert df.iloc[0][16] == 'R Hand Entry'
    assert df.iloc[4][16] == 'L Hand Entry'


def chunk_series(series, sentence_length=120):
    """
    Split series data into a number of events, each of length sentence_length
    :param series:
    :return: data, dict containing:
        elapsed_time np.array[chunk no, time step]) = elapsed time FROM START OF CHUNK in seconds
        sensor_vals_normed: np.array([chunk no, sensor no, timestep]) = sensor val
        swim_class: np.array([chunk no, time step]) = swim class
        stroke_phase: np.array([chunk no, time step]) = Stroke events. Most are zero (null). Others are 1 - 8.
        # And the following, for reference.
        cols: Name of the 12 columns that make up the sensor vals
        swim_class_def: Definitions for the four swim classes
        stroke_phase_def: Stroke event defintions.
        subject_cat: Category of subject (Elite)

    """
    raise NotImplementedError('Chuck series not yet created.')

def _format_time(time_str):
    return datetime.strptime(time_str, "'%I:%M:%S.%f'")

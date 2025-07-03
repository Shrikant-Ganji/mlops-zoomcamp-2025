# tests/test_preprocessing.py

import pandas as pd
from datetime import datetime as dt
from preprocessing import prepare_data  # import your function here


def test_prepare_data():
    data = [
        (None, None, dt(2023, 1, 1, 1, 1), dt(2023, 1, 1, 1, 10)),
        (1, 1, dt(2023, 1, 1, 1, 2), dt(2023, 1, 1, 1, 10)),
        (1, None, dt(2023, 1, 1, 1, 2), dt(2023, 1, 1, 1, 2, 59)),
        (3, 4, dt(2023, 1, 1, 1, 2), dt(2023, 1, 2, 2, 1)),
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    actual_df = prepare_data(df)

    expected_data = [
    {
        'PULocationID': 1,
        'DOLocationID': 1,
        'tpep_pickup_datetime': dt(2023, 1, 1, 1, 2),
        'tpep_dropoff_datetime': dt(2023, 1, 1, 1, 10),
        'PU_DO': '1_1',
        'trip_duration': 8.0,
    },
    {
        'PULocationID': 3,
        'DOLocationID': 4,
        'tpep_pickup_datetime': dt(2023, 1, 1, 1, 2),
        'tpep_dropoff_datetime': dt(2023, 1, 2, 2, 1),
        'PU_DO': '3_4',
        'trip_duration': 1499.0,  # corrected here
    },
]
    expected_df = pd.DataFrame(expected_data)

    # Reset index before comparing, because dropping rows can cause index mismatch
    pd.testing.assert_frame_equal(actual_df.reset_index(drop=True), expected_df.reset_index(drop=True))
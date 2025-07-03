import pandas as pd

def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and prepares the taxi trip data:
    - Drops rows with missing pickup/dropoff locations
    - Converts location IDs to integers
    - Adds PU_DO feature (pickup_dropoff_id)
    - Calculates trip duration in minutes
    """
    # Drop rows where pickup or dropoff location ID is missing
    df_clean = df.dropna(subset=['PULocationID', 'DOLocationID']).copy()

    # Convert location IDs to int
    df_clean['PULocationID'] = df_clean['PULocationID'].astype(int)
    df_clean['DOLocationID'] = df_clean['DOLocationID'].astype(int)

    # Create combined pickup/dropoff feature
    df_clean['PU_DO'] = df_clean['PULocationID'].astype(str) + '_' + df_clean['DOLocationID'].astype(str)

    # Calculate trip duration in minutes
    df_clean['trip_duration'] = (
        df_clean['tpep_dropoff_datetime'] - df_clean['tpep_pickup_datetime']
    ).dt.total_seconds() / 60

    return df_clean
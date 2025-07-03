import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from joblib import dump

def read_data(filename: str, categorical: list):
    df = pd.read_parquet(filename)
    df['duration'] = (df.lpep_dropoff_datetime - df.lpep_pickup_datetime).dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    df[categorical] = df[categorical].astype(str)
    return df

def main(year: int, month: int):
    input_file = f"../data/green_tripdata_{year}-{month:02d}.parquet"
    output_file = f"models/lin_reg_{year}_{month:02d}.bin"
    
    categorical = ['PULocationID', 'DOLocationID']
    
    df = read_data(input_file, categorical)
    
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    df['PU_DO'] = df['PU_DO'].astype(str)
    
    from sklearn.feature_extraction import DictVectorizer
    dv = DictVectorizer()

    train_dicts = df[['PU_DO', 'trip_distance']].to_dict(orient='records')
    X_train = dv.fit_transform(train_dicts)
    y_train = df['duration'].values

    model = LinearRegression()
    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)
    with open(output_file, "wb") as f_out:
        dump((dv, model), f_out)

    print(f"✅ Model trained and saved to {output_file}")

if __name__ == "__main__":
    main(year=2023, month=3)
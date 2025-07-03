import boto3
import pytest
from moto.s3 import mock_s3
import pandas as pd
import io

BUCKET = "nyc-duration"

@mock_s3
def test_write_and_read_parquet_from_s3():
    # Setup mock S3
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET)

    # Sample DataFrame
    df = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})

    # Write to S3
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    s3.put_object(Bucket=BUCKET, Key="test.parquet", Body=buffer.getvalue())

    # Read back from S3
    obj = s3.get_object(Bucket=BUCKET, Key="test.parquet")
    result_df = pd.read_parquet(io.BytesIO(obj['Body'].read()))

    # Assert both are equal
    pd.testing.assert_frame_equal(df, result_df)

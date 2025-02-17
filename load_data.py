import pandas as pd
from pynessie.client import NessieClient
from pynessie.model import Content, Operation
from minio import Minio
from minio.error import S3Error

# Nessie configuration
NESSIE_API_URL = "http://localhost:19120/api/v1"
NESSIE_BRANCH = "main"
NESSIE_CATALOG_NAME = "example_catalog"

# Minio configuration
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password"
MINIO_BUCKET_NAME = "example-bucket"
MINIO_OBJECT_NAME = "example-data.csv"
MINIO_FILE_PATH = "example-data.csv"

# Create sample data
def create_sample_data():
    data = {
        "id": [1, 2, 3],
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35]
    }
    df = pd.DataFrame(data)
    df.to_csv(MINIO_FILE_PATH, index=False)
    print("Sample data created")

# Initialize Nessie client
nessie_client = NessieClient(base_url=NESSIE_API_URL)

# Create a catalog entry in Nessie
def create_catalog_entry():
    try:
        nessie_client.create_branch(NESSIE_BRANCH)
        nessie_client.commit(
            branch=NESSIE_BRANCH,
            message="Create catalog entry",
            operations=[
                Operation.Put(
                    key=NESSIE_CATALOG_NAME,
                    content=Content(
                        type="ICEBERG_TABLE",
                        metadata_location="s3://{}/{}".format(MINIO_BUCKET_NAME, MINIO_OBJECT_NAME)
                    )
                )
            ]
        )
        print("Catalog entry created in Nessie")
    except Exception as e:
        print(f"Error creating catalog entry in Nessie: {e}")

# Initialize Minio client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Upload data to Minio
def upload_data_to_minio():
    try:
        found = minio_client.bucket_exists(MINIO_BUCKET_NAME)
        if not found:
            minio_client.make_bucket(MINIO_BUCKET_NAME)
        else:
            print("Bucket '{}' already exists".format(MINIO_BUCKET_NAME))

        minio_client.fput_object(
            MINIO_BUCKET_NAME, MINIO_OBJECT_NAME, MINIO_FILE_PATH
        )
        print("Data uploaded to Minio")
    except S3Error as e:
        print(f"Error uploading data to Minio: {e}")

if __name__ == "__main__":
    create_sample_data()
    upload_data_to_minio()
    create_catalog_entry()
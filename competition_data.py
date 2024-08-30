from pyopensky.s3 import S3Client

s3 = S3Client()

to_download = [
    "2022-01-01.parquet",
    "challenge_set.csv",
]
download = True

for obj in s3.s3client.list_objects("competition-data", recursive=True):
    print(f"{obj.bucket_name=}, {obj.object_name=}")
    if download and obj.object_name in to_download:
        s3.download_object(obj)


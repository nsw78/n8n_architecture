class MinioClient:
    def __init__(self, minio_url, access_key, secret_key):
        from minio import Minio
        self.client = Minio(minio_url, access_key=access_key, secret_key=secret_key, secure=False)

    def upload_file(self, bucket_name, file_object, object_name):
        try:
            # Check if the bucket exists, if not create it
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            # Upload the file
            self.client.put_object(bucket_name, object_name, file_object.stream, length=file_object.content_length, content_type=file_object.content_type)
            return {"message": "File uploaded successfully", "object_name": object_name}
        except Exception as e:
            return {"error": str(e)}
class MinioClient:
    def __init__(self, minio_url, access_key, secret_key):
        from minio import Minio
        self.client = Minio(minio_url, access_key=access_key, secret_key=secret_key, secure=False)

    def upload_file(self, bucket_name, object_name, data_stream, data_length, content_type='application/octet-stream'):
        """
        Faz upload de um stream de dados para um bucket no MinIO.

        :param bucket_name: Nome do bucket.
        :param object_name: Nome do objeto a ser criado.
        :param data_stream: O stream de dados do arquivo.
        :param data_length: O tamanho total dos dados.
        :param content_type: O tipo de conteúdo (MIME type) do arquivo.
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                self.client.make_bucket(bucket_name)
            self.client.put_object(bucket_name, object_name, data_stream, length=data_length, content_type=content_type)
            return {"message": "File uploaded successfully", "object_name": object_name}
        except Exception as e:
            return {"error": str(e)}
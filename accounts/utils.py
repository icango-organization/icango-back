import boto3

from icango.settings import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_STORAGE_BUCKET_NAME, AWS_S3_CUSTOM_DOMAIN
)

class BaseS3():
    s3_resource = boto3.resource(
        's3',
        region_name = AWS_REGION,
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    bucket = s3_resource.Bucket(AWS_STORAGE_BUCKET_NAME)

    def __init__(self, **kwargs):
        self.field = kwargs.get("field")

    @classmethod
    def post(cls, files=None, keys=None):
        for file, key in zip(files, keys):
            cls.bucket.upload_fileobj(
                file, key,
                ExtraArgs = {
                    "ContentType" : file.content_type
                }
            )

    def api_post(self, files=None, data_set=None):
        if type(data_set) == dict:
            keys = [data.get(self.field).replace(AWS_S3_CUSTOM_DOMAIN, "") for data in data_set]
        else:
            keys = [getattr(data, self.field).replace(AWS_S3_CUSTOM_DOMAIN, "") for data in data_set]

        return self.post(files=files, keys=keys)

    @classmethod
    def delete(cls, prefixes=None):
        for prefix in prefixes:
            object = cls.bucket.objects.filter(Prefix=prefix)
            object.delete()
    
    def api_delete(self, data_urls=None, data_folder=None, data_folder_id=None):
        prefixes = []
        
        if data_urls:
            prefixes = [key.get(self.field).lstrip(AWS_S3_CUSTOM_DOMAIN) for key in data_urls]
        elif data_folder:
            prefixes = [
                data_folder
                + "/" + str(data_folder_id)
            ]
        
        return self.delete(prefixes=prefixes)
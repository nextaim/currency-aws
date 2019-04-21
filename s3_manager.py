import boto3

BUCKET_NAME = 'currency-reports'

s3 = boto3.resource('s3')


def upload_file(name, data):
    s3.Bucket(BUCKET_NAME).put_object(Key=name+'.xml', Body=data)

import os
from PIL import Image
import getopt, sys
from io import BytesIO
from flask import Flask, request
import boto3
from datetime import datetime, timedelta

S3_BUCKET = os.environ.get('S3_BUCKET')
S3_OBJECT_PREFIX = os.environ.get('S3_OBJECT_PREFIX')
PROXY_HOST = os.environ.get('PROXY_HOST')
CLOUDFRONT_ORIGIN = os.environ.get('CLOUDFRONT_ORIGIN')

app = Flask(__name__)

# Check if the url contains image or not
def check_url_format(format):
    if format in ("image/png", "image/jpeg", "image/jpg"):
        return True
    else:
        return False

# Connect to S3 with access key and secret
def connect_s3():
    try:
        client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('SECRET_KEY')
        )
    except Exception as e:
        raise("Something went wrong with connection!")
    return client

# Check and fetch the metadata of any bucket
def get_images_metadata(path):
    client = connect_s3()
    try:
        meta_data = client.get_object(Bucket=S3_BUCKET,Key=path)
        return meta_data
    except Exception as e:
        return 404

# Check and fetch the binary of any bucket
def get_images_binary(path):
    client = connect_s3()
    try:
        byte_file = client.get_object(Bucket=S3_BUCKET,Key=path)['Body'].read()
        return byte_file
    except Exception as e:
        return 404


# View to resize any image of S3
@app.route('/resize')
def resize():
    width = int(request.args.get('width'))
    height = int(request.args.get('height'))
    relative_path = request.args.get('path')

    # Check cache and return the file path
    resized_path = '{proxy_host}/{width}x{height}/{path}'.format(proxy_host=PROXY_HOST, width=width, height=height, path=relative_path)
    resized_metadata = get_images_metadata(resized_path)
    if resized_metadata != 404:
        return 'https://' + resized_path

    # If Cache miss get Image from S3 and resize it.

    # Check the file format  
    relative_metadata = get_images_metadata(relative_path)
    file_format = relative_metadata['ContentType']
    if check_url_format(file_format):
        # Get image
        relative_file_byte = get_images_binary(relative_path)
        # Convert to Image type object
        img_obj = Image.open(BytesIO(relative_file_byte))
        # Resize the height and width
        img_obj = img_obj.resize((width, height), Image.ANTIALIAS)
        # Connect to S3 and upload the resized image with 48 hour expiry.
        client = connect_s3()
        in_mem_file = BytesIO()
        img_obj.save(in_mem_file, format=file_format[6:])
        in_mem_file.seek(0)
        client.put_object(Body=in_mem_file,Bucket=S3_BUCKET,Key=resized_path,Expires=datetime.now() + timedelta(days=2))
        return 'https://' + resized_path
    else:
        return "We doesn't support this file-type!!"

#View to return the original path of the Image
@app.route("/<path:path>")
def get_original_image(path):
    actual_path = S3_OBJECT_PREFIX + '/' + S3_BUCKET + '/' + "/".join(path.split('/')[1:])
    client = connect_s3()
    return actual_path

if __name__ == '__main__':
    app.run()
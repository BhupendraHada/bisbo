from __future__ import absolute_import, unicode_literals
import boto3
from io import BytesIO
from PIL import Image as pil_image
from resizeimage import resizeimage
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile


class S3Connection(object):

    def upload(self, data, image_file):
        if data.get("file_name"):
            _file_path = data['directory'] + data.get("file_name")
        else:
            _file_path = data['directory'] + image_file.name

        _file_url = ''
        if getattr(settings, "SERVER_NAME", ""):
            image_file.file.seek(0)
            session = boto3.session.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            s3_client = session.resource('s3')
            s3_client.Bucket(settings.AWS_BUCKET_NAME).upload_fileobj(image_file.file, Key=_file_path)
            _file_url = settings.AWS_HOST_URL + _file_path
        else:
            session = boto3.session.Session()
            s3_client = session.resource('s3')
            image_file.file.seek(0)
            s3_client.Bucket(settings.AWS_BUCKET_NAME).upload_fileobj(image_file.file, Key=_file_path,
                                                                      ExtraArgs={'ACL': ''})
            _file_url = settings.AWS_HOST_URL + _file_path
        return _file_url


class ImageTransform(object):

    def resize(self, file):
        _size = (380, 380)
        img = pil_image.open(file)
        if img.size > _size:
            file_format = file.name.split('.')[-1]
            if file_format == 'jpg':
                file_format = 'jpeg'
            img = resizeimage.resize_thumbnail(img, _size)
            thumb_io = BytesIO()
            img.save(thumb_io, img.format)
            file = InMemoryUploadedFile(thumb_io, None, file.name, 'image/{0}'.format(file_format), _size, None)
        return file

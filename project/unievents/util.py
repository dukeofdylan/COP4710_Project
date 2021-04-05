import requests
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


def download(url, path, chunk=2048):
    req = requests.get(url, stream=True)
    if req.status_code == 200:
        with open(path, "wb") as f:
            for chunk in req.iter_content(chunk):
                f.write(chunk)
            f.close()
        return path
    raise Exception("Given url is return status code:{}".format(req.status_code))

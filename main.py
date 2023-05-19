import io
import os
import numpy
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from utils.str_utils import replace_turkish_chars
from utils.text_extraction_utils import get_converted_image, get_annotations, get_votes
import google.auth

credentials, project = google.auth.default()
vision_client = vision_v1.ImageAnnotatorClient(credentials=credentials)


# image_uri = 'gs://secim2/im1.png'
image_uri = 'im1.png'

im_arr, annotations = get_annotations(vision_client, image_uri)
res = get_votes(annotations)
# converted_image = get_converted_image(im_arr, annotations)
# cv2.imwrite("imres.png", converted_image)

pass

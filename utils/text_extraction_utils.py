import io
import numpy
import cv2
from PIL import Image
from google.cloud.vision_v1 import types
from utils.str_utils import remove_turkish_chars, string_matching


def get_annotations(vision_client, image_uri):
    # Load the image from Google Cloud Storage
    with io.open(image_uri, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    pil_image = Image.open(io.BytesIO(content))

    im_arr = numpy.array(pil_image)
    im_arr = im_arr[:, :, :3]

    # Use the Google Cloud Vision API to perform OCR on the image
    response = vision_client.text_detection(image=image)
    annotations = response.text_annotations

    # Print the extracted text
    # if annotations:
    #     print(annotations[0].description)
    # else:
    #     print('No text found in the image.')

    return im_arr, annotations


def get_converted_image(im_arr, annotations):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.3
    color = (0, 0, 0)
    thickness = 1

    converted_image = numpy.ones_like(im_arr) * 255

    for ann in annotations[1:]:
        word = remove_turkish_chars(ann.description.lower())

        upper_left = ann.bounding_poly.vertices[0]
        x, y = upper_left.x, upper_left.y
        converted_image = cv2.putText(
            converted_image,
            word,
            (x, y),
            font,
            fontScale=fontScale,
            color=color,
            thickness=thickness,
        )
    return converted_image


def get_votes(annotations):
    a_dict = {
        "recep": [],
        "muharrem": [],
        "kemal": [],
        "sinan": [],
    }

    for ann in annotations[1:]:
        word = remove_turkish_chars(ann.description.lower())

        upper_left = ann.bounding_poly.vertices[0]
        x, y = upper_left.x, upper_left.y

        for key in a_dict.keys():
            ratio = string_matching(word, key)
            if ratio > 0.8:
                a_dict[key].append({"x": x, "y": y})
    return a_dict

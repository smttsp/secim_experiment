import io
import numpy
import cv2
from PIL import Image
from google.cloud.vision_v1 import types
from utils.str_utils import remove_turkish_chars, string_matching
from pprint import pprint

CANDIDATES = ("recep", "muharrem", "kemal", "sinan")


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


def get_important_locations(candidates, annotations):
    important_locations = {can: [] for can in candidates}

    important_locations.update(
        {
            "rakamla": [],
            "yaziyla": [],
            # "toplam": []
        }
    )

    for ann in annotations[1:]:
        word = remove_turkish_chars(ann.description.lower())

        xs = set()
        ys = set()

        for ver in ann.bounding_poly.vertices:
            xs.add(ver.x)
            ys.add(ver.y)
        xyxy = (min(xs), min(ys), max(xs), max(ys))

        for key in important_locations.keys():
            ratio = string_matching(word, key)
            if ratio > 0.85:
                important_locations[key].append({"xyxy": xyxy, "ratio": ratio})

    return important_locations


def get_parallel_lines(candidates, important_locations):
    pass


def get_mid_horizontal_point(xyxy1, xyxy2):
    mid = (xyxy1[-1] + xyxy2[1]) / 2
    return int(mid)


def get_separators_for_votes(candidates, important_locations):
    horz_separators = []
    for c1, c2 in zip(candidates[:-1], candidates[1:]):
        # print(important_locations[c1], important_locations[c2])
        mid = get_mid_horizontal_point(important_locations[c1][0]["xyxy"], important_locations[c2][0]["xyxy"])
        horz_separators.append(mid)

    diff = horz_separators[1] - horz_separators[0]
    horz_separators.insert(0, horz_separators[0] - diff)
    horz_separators.append(horz_separators[-1] + diff)
    horz_separators.append(horz_separators[-1] + diff)
    return horz_separators


def get_votes_per_candidate(annotations, candidates, horz_separators):
    candidates_wtotal = list(candidates)
    candidates_wtotal.append("total")

    for cand, up_line, low_line in zip(candidates_wtotal, horz_separators[:-1],  horz_separators[1:]):
        print(cand)
        for ann in annotations[1:]:
            word = remove_turkish_chars(ann.description.lower())

            y_mean = numpy.mean(list({ver.y for ver in ann.bounding_poly.vertices}))
            if up_line < y_mean < low_line:
                print(word)
        print("----\n")


def get_votes(annotations, candidates=CANDIDATES):

    important_locations = get_important_locations(candidates, annotations)
    horz_separators = get_separators_for_votes(candidates, important_locations)

    parallel_lines = get_parallel_lines(candidates, important_locations)


    return important_locations

import io
import numpy
import cv2
from PIL import Image
from google.cloud.vision_v1 import types
from utils.str_utils import replace_turkish_chars, string_matching, get_number
from pprint import pprint
from collections import defaultdict

CANDIDATES = ("recep", "muharrem", "kemal", "sinan")
NUM_FORMAT = ("rakamla", "yaziyla")


def get_annotations(vision_client, image_uri):
    # Load the image from Google Cloud Storage
    with io.open(image_uri, "rb") as image_file:
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
        word = replace_turkish_chars(ann.description.lower())

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


def get_important_locations(candidates, count_info, annotations):
    important_locations = {can: [] for can in candidates}

    important_locations.update({cnt: [] for cnt in count_info})

    for ann in annotations[1:]:
        word = replace_turkish_chars(ann.description.lower())

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


def get_midpoint(xyxy1, xyxy2, axis="horz"):
    if axis == "horz":
        mid = xyxy1[-1] + xyxy2[1]
    else:
        mid = xyxy1[-2] + xyxy2[0]

    return int(mid / 2)


def get_horz_separators_for_votes(candidates, important_locations):
    horz_separators = []
    for c1, c2 in zip(candidates[:-1], candidates[1:]):
        # print(important_locations[c1], important_locations[c2])
        mid = get_midpoint(
            important_locations[c1][0]["xyxy"], important_locations[c2][0]["xyxy"], axis="horz"
        )
        horz_separators.append(mid)

    diff = horz_separators[1] - horz_separators[0]
    horz_separators.insert(0, horz_separators[0] - diff)
    horz_separators.append(horz_separators[-1] + diff)
    horz_separators.append(horz_separators[-1] + diff)

    return horz_separators


def get_vert_separators_for_votes(num_format, important_locations):
    rakam = important_locations[num_format[0]][0]["xyxy"]
    yazi = important_locations[num_format[1]][0]["xyxy"]

    rakam_endx = rakam[2]
    yazi_begx = yazi[0]

    vert_mid_separator = int((3 * rakam_endx + yazi_begx) / 4)

    rakam_center = get_midpoint(rakam, rakam, axis="vert")
    yazi_center = get_midpoint(yazi, yazi, axis="vert")

    v1 = 2 * rakam_center - vert_mid_separator
    v3 = 2 * yazi_center - vert_mid_separator

    vert_separators = [v1, vert_mid_separator, v3]

    return vert_separators


def get_votes_per_candidate(annotations, candidates, num_format, horz_separators, vert_separators):
    candidates_wtotal = list(candidates)
    candidates_wtotal.append("total")

    results = defaultdict(dict)
    for cand, up_line, low_line in zip(
        candidates_wtotal, horz_separators[:-1], horz_separators[1:]
    ):
        print(cand)
        for format, left_line, right_line in zip(
            num_format, vert_separators[:-1], vert_separators[1:]
        ):
            print(format)
            words = []
            for ann in annotations[1:]:
                word = replace_turkish_chars(ann.description.lower())

                y_center = numpy.mean(list({ver.y for ver in ann.bounding_poly.vertices}))
                x_center = numpy.mean(list({ver.x for ver in ann.bounding_poly.vertices}))

                if up_line < y_center < low_line and left_line < x_center < right_line:
                    print("----", word)
                    words.append(word)
            output = " ".join(words)
            num = get_number(format, output)
            results[cand][format] = num

            print("###")
        print("----\n")

    return results


def determine_vote_counts(results, num_format):
    """Determining vote counts from the text-predictions & line adjustments.
    the results format is as follows:

    {
        candidate: {"yaziyla(string)": cnt1, "rakamla(digit)": cnt2 }
    }

    if for a candidate,
    1. both string and digit are the same, pick that number
    2. one of them is negative (-1, -2 or -3, each indicate different failure), then pick the other number
    3. if both conflict, try all combinations and pick the best matches

    Args:
        results (dict):
        num_format:

    Returns:

    """

    final_counts = dict()

    for candidate, vote_counts in results.items():
        dig_cnt = vote_counts[num_format[0]]
        str_cnt = vote_counts[num_format[1]]

        # 1
        if dig_cnt == str_cnt:
            final_counts[candidate] = dig_cnt
        elif dig_cnt < 0 <= str_cnt:
            final_counts[candidate] = str_cnt
        elif dig_cnt >= 0 > str_cnt:
            final_counts[candidate] = dig_cnt
        elif dig_cnt < 0 and str_cnt < 0:
            final_counts[candidate] = 0

    total_up_to_now = sum(list(final_counts.values()))
    total_up_to_now = total_up_to_now - final_counts.get("total", 0)

    # traverse and find the correct numbers, also make sure that the sum adds up to total.
    #   notice total can be wrong
    if len(final_counts) != len(results):
        pass

    return final_counts


def get_votes(annotations, candidates=CANDIDATES, num_format=NUM_FORMAT):
    important_locations = get_important_locations(candidates, num_format, annotations)
    horz_separators = get_horz_separators_for_votes(candidates, important_locations)
    vert_separators = get_vert_separators_for_votes(num_format, important_locations)
    results = get_votes_per_candidate(
        annotations, candidates, num_format, horz_separators, vert_separators
    )

    final_results = determine_vote_counts(results, num_format)
    return important_locations

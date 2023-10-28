from pupil_apriltags import Detector
import cv2

import math
from typing import List

APRIL_TAG_DETECTION = True

at_detector = Detector(
    families="tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0,
)


def process_image(image, tags, targets):
    for tag in tags:
        corner_01 = (int(tag.corners[0][0]), int(tag.corners[0][1]))
        corner_02 = (int(tag.corners[1][0]), int(tag.corners[1][1]))
        if tag.tag_id in targets:
            w = 2.5
            p = math.sqrt(
                (corner_02[0] - corner_01[0]) ** 2 + (corner_02[1] - corner_01[1]) ** 2
            )
            d_prime = (w * 955) / p
            draw_tag(image, tag, (0, 0, 255), corner_01, corner_02, str(d_prime))
        else:
            draw_tag(image, tag, (0, 255, 0), corner_01, corner_02, "-")
    return image


def draw_tag(image, tag, color, corner_01, corner_02, D_prime) -> None:
    center = (int(tag.center[0]), int(tag.center[1]))
    corner_03 = (int(tag.corners[2][0]), int(tag.corners[2][1]))
    corner_04 = (int(tag.corners[3][0]), int(tag.corners[3][1]))
    height, width, _ = image.shape
    image_center = (width // 2, height // 2)

    cv2.circle(image, image_center, 15, (0, 255, 0), 20)
    cv2.circle(image, (center[0], center[1]), 5, color, 5)
    cv2.line(
        image, (corner_01[0], corner_01[1]), (corner_02[0], corner_02[1]), color, 2
    )
    cv2.line(
        image, (corner_02[0], corner_02[1]), (corner_03[0], corner_03[1]), color, 2
    )
    cv2.line(
        image, (corner_03[0], corner_03[1]), (corner_04[0], corner_04[1]), color, 2
    )
    cv2.line(
        image, (corner_04[0], corner_04[1]), (corner_01[0], corner_01[1]), color, 2
    )
    cv2.putText(
        image,
        str(tag.tag_id),
        (center[0] - 10, center[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        color,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        image,
        D_prime,
        (center[0] - 10, center[1] - 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        color,
        2,
        cv2.LINE_AA,
    )


def calculate_alignment(img, tags, targets):
    """
    - True: there's no need to align
    - False: no april tag is detected
    - [int, int]: amount to move left or right, and forward or backward, respectively
    """
    height, width, _ = img.shape
    image_center = (width // 2, height // 2)

    # TODO: maybe fix this
    cv2.circle(img, image_center, 5, (255, 0, 0), 5)

    for tag in tags:
        if tag.tag_id in targets:
            object_center = tag.center

            left_right = object_center[0] - image_center[0]
            forward_backward = object_center[1] - image_center[1]

            if -1 < left_right < 1 or -1 < forward_backward < 1:  # TODO: might change
                return True

            return int(left_right), int(forward_backward)  # TODO: might change

    return False

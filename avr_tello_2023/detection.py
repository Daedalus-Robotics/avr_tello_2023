from pupil_apriltags import Detector
import cv2
import numpy as np

import math

at_detector = Detector(
    families="tag36h11",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0,
)


def process_image_H(image, detected_circles):
    if detected_circles is not None:
        np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
            # center
            cv2.circle(image, (int(x), int(y)), 1, (0, 0, 255), 3)
    return image


def process_image_A(image, tags, targets):
    for tag in tags:
        corner_01 = (int(tag.corners[0][0]), int(tag.corners[0][1]))
        corner_02 = (int(tag.corners[1][0]), int(tag.corners[1][1]))
        if tag.tag_id in targets:
            w = 2.5
            p = math.sqrt(
                (corner_02[0] - corner_01[0]) ** 2 + (corner_02[1] - corner_01[1]) ** 2
            )
            d_prime = (w * 955) / p
            _draw_tag(image, tag, (0, 0, 255), corner_01, corner_02, str(d_prime))
        else:
            _draw_tag(image, tag, (0, 255, 0), corner_01, corner_02, "-")
    return image


def _draw_tag(image, tag, color, corner_01, corner_02, D_prime) -> None:
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


def _draw_image_center(img):
    height, width = img.shape
    image_center = (width // 2, height // 2)
    cv2.circle(img, image_center, 5, (255, 0, 0), 15)
    return image_center


def _range_check(left_right, forward_backward) -> tuple[int, int]:
    y = 0.5833
    x = 0.7625

    move_x = int(left_right * x)
    move_y = int(forward_backward * y)

    if -20 < move_x < 20:
        if move_x < 0:
            move_x = -20
        else:
            move_x = 20

    if -20 < move_y < 20:
        if move_y < 0:
            move_y = -20
        else:
            move_y = 20

    print(f"x, y: {move_x}, {move_y}")

    return move_x, move_y


def calculate_alignment_A(img, tags, targets):
    image_center = _draw_image_center(img)
    for tag in tags:
        if tag.tag_id in targets:
            object_center = tag.center

            left_right = image_center[0] - object_center[0]
            forward_backward = image_center[1] - object_center[1]

            if (
                -20 < left_right < 20 or -20 < forward_backward < 20
            ):  # TODO: might change
                return None

            return _range_check(forward_backward, left_right)

    return None


def calculate_alignment_H(img, detected_circles):
    image_center = _draw_image_center(img)
    if detected_circles is not None:
        np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            x, y = pt[0], pt[1]

            left_right = image_center[0] - x
            forward_backward = image_center[1] - y

            if (
                -10 < left_right < 10 or -10 < forward_backward < 10
            ):  # TODO: might change
                return None

            # flipped
            return _range_check(forward_backward, left_right)

    return None


def calculate_alignment_S(img, square):
    # image_center = _draw_image_center(img)

    try:
        height, width, _ = img.shape
    except ValueError:
        height, width = img.shape

    image_center = (width // 2, height // 2)
    cv2.circle(img, image_center, 5, (0, 0, 255), 5)

    if square is not None:
        (x, y, w, h) = square
        obj_center = (w // 2 + x, h // 2 + y)

        # square's center
        cv2.circle(img, obj_center, 10, (100, 200, 100))

        x = image_center[0] - obj_center[0]
        y = image_center[1] - obj_center[1]

        if -15 < x < 15 and -15 < y < 15:  # TODO: might change
            return None

        return _range_check(x, y)

    return None

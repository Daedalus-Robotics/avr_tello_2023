from djitellopy import Tello
import cv2
import numpy as np

from time import sleep
from threading import Thread

import smoke_jumper
from detection import (
    process_image_A,
    process_image_H,
    at_detector,
    calculate_alignment_A,
    calculate_alignment_H,
    calculate_alignment_S,
)
from constants import *

CONTRAST = 2
BRIGHTNESS = 19
DIRECTION = True


def clamp_x_y(x: int, y: int) -> tuple[int, int]:
    if -5 < x < 5:
        x = 0
    if -5 < y < 5:
        y = 0
    return x, y


def adjust_to_tello_rc(x: int, y: int, adjust: float = 0.785) -> tuple[int, int]:
    (x, y) = (int(x * adjust), int(y * adjust))
    return x, y


def align_tello(tello: Tello, frame_read, detection_type: str):
    img, show_img = get_frames(frame_read)
    if detection_type == "A":
        tags, targets = show_april_tag(img, show_img)
        amount_to_move = calculate_alignment_A(img, tags, targets)
    elif detection_type == "H":
        detected_circles = show_helipad(img, show_img)
        amount_to_move = calculate_alignment_H(img, detected_circles)
    else:
        squares = show_square(img, show_img)
        amount_to_move = calculate_alignment_S(img, squares)

    if amount_to_move is None:
        return

    left_right, forward_backward = amount_to_move

    # actually aligning the tello
    if left_right > 0:
        tello.move_right(left_right)
    else:
        tello.move_left(-left_right)

    if forward_backward > 0:
        tello.move_forward(forward_backward)
    else:
        tello.move_back(-forward_backward)


def show_square(img_for_detection, show_img):
    blur = cv2.medianBlur(img_for_detection, 5)
    sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

    # threshold and morph close
    thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours and filter using threshold area
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    squares: list[tuple[int, int, int, int]] = []
    for c in cnts:
        area = cv2.contourArea(c)
        if MIN_AREA < area < MAX_AREA:
            x, y, w, h = cv2.boundingRect(c)
            squares.append((x, y, w, h))
            cv2.rectangle(show_img, (x, y), (x + w, y + h), (36, 255, 12), 2)

    return squares


def show_april_tag(img_for_detection, show_img):
    tags = at_detector.detect(
        img_for_detection, estimate_tag_pose=False, camera_params=None, tag_size=None
    )

    targets = [6, 2]
    show_img = process_image_A(show_img, tags, targets)

    return tags, targets


def show_helipad(img_for_detection, show_img):
    img = cv2.addWeighted(img_for_detection, CONTRAST, img_for_detection, 0, BRIGHTNESS)
    img = cv2.medianBlur(img, 5)
    detected_circles = cv2.HoughCircles(
        img,
        cv2.HOUGH_GRADIENT,
        1,
        50,
        param1=30,
        param2=50,
        minRadius=3,
        maxRadius=100,
    )
    show_img = process_image_H(show_img, detected_circles)

    return detected_circles


def show_frame(tello: Tello, frame_read, detection_type: str):
    img_for_detection, show_img = get_frames(frame_read)
    if detection_type == "A":
        show_april_tag(img_for_detection, show_img)
    elif detection_type == "H":
        show_helipad(img_for_detection, show_img)
    else:
        show_square(img_for_detection, show_img)

    cv2.imshow("CAMERA FEED", show_img)
    cv2.waitKey(1)


def get_frames(frame_read):
    frame = frame_read.frame
    img = frame
    show_img = np.copy(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if not DIRECTION:
        show_img = cv2.cvtColor(show_img, cv2.COLOR_BGR2RGB)

    return img, show_img


def enter_recon_path(tello: Tello) -> None:
    tello.takeoff()
    tello.move_up(60)

    # go straight to the school
    tello.move_forward(HELIPAD_APRIL + APRIL_SCHOOL)

    align_tello(tello, tello.get_frame_read(), "S")

    smoke_jumper.close_dropper()
    sleep(2)
    smoke_jumper.open_dropper()

    tello.move_back(HELIPAD_APRIL + APRIL_SCHOOL)

    tello.land()

from djitellopy import Tello
import cv2
from keyboard import send
import numpy as np

from time import sleep
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
THRESH = 20
BLOCK = 51


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
    for _ in range(3):
        img, show_img = get_frames(frame_read)
        if detection_type == "A":
            tags, targets = show_april_tag(img, show_img)
            amount_to_move = calculate_alignment_A(img, tags, targets)
        elif detection_type == "H":
            detected_circles = show_helipad(img, show_img)
            amount_to_move = calculate_alignment_H(img, detected_circles)
        else:
            square = show_square(img, show_img)
            amount_to_move = calculate_alignment_S(img, square)

        if amount_to_move is True:
            return
        elif amount_to_move is False:
            tello.move_up(20)
            continue

        left_right, forward_backward = amount_to_move

        # actually aligning the tello
        if left_right > 0:
            if left_right < 20:
                tello.send_rc_control(20, 0, 0, 0)
                sleep(0.5)
                tello.send_rc_control(0, 0, 0, 0)
                continue

            tello.move_right(left_right)
        elif left_right < 0:
            if left_right > -20:
                tello.send_rc_control(-20, 0, 0, 0)
                sleep(0.5)
                tello.send_rc_control(0, 0, 0, 0)
                continue

            tello.move_left(-left_right)

        if forward_backward > 0:
            if forward_backward < 20:
                tello.send_rc_control(0, -20, 0, 0)
                sleep(0.5)
                tello.send_rc_control(0, 0, 0, 0)
                continue

            tello.move_forward(forward_backward)
        elif forward_backward < 0:
            if left_right > -20:
                tello.send_rc_control(0, 20, 0, 0)
                sleep(0.5)
                tello.send_rc_control(0, 0, 0, 0)
                continue

            tello.move_back(-forward_backward)

        break


def show_square(img_for_detection, show_img):
    img_for_detection = cv2.addWeighted(img_for_detection, 2, img_for_detection, 0, 10)
    thresh = cv2.adaptiveThreshold(
        img_for_detection,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        BLOCK,
        9,
    )

    # Draw all contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255, 255, 255), -1)  # MUST BE WHITE

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    final = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=8)

    cv2.imshow("Modified", final)

    # Find contours and filter using threshold area
    cnts = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # squares = cnts
    squares = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        if -200 < (x + w) - (y + h) < 200 and 1000 < area < 12000:
            squares.append(c)

    areas = [cv2.contourArea(c) for c in squares]

    if len(areas) == 0:
        return None

    index = areas.index(max(areas))
    if len(squares) > 0:
        c = squares[index]
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(show_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # if len(squares) > 0:
    #     c = max(squares, key=cv2.contourArea)
    #     x, y, w, h = cv2.boundingRect(c)
    #     cv2.rectangle(show_img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    #     return x, y, w, h

    return None


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
        100,
        param1=30,
        param2=50,
        minRadius=20,
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
        square = show_square(img_for_detection, show_img)
        calculate_alignment_S(show_img, square)

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
    tello.move_up(50)

    # go straight to the school
    tello.move_forward(HELIPAD_APRIL + APRIL_SCHOOL)

    align_tello(tello, tello.get_frame_read(), "S")

    smoke_jumper.close_dropper()
    # just hover over the building
    tello.send_keepalive()
    smoke_jumper.open_dropper()

    Tello.LOGGER.info("Completed Autonomous Recon Path")

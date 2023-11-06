from djitellopy import Tello, TelloException
import cv2
import keyboard
from textual.app import App
import numpy as np
import serial

from inspect import signature
from platform import system
from threading import Thread
from typing import List
from time import sleep

from constants import (
    BACK_BRIDGE_DISTANCE,
    BACK_TO_MIDDLE_BRIDGE_DISTANCE,
    SCHOOL_DISTANCE,
    APRIL_SCHOOL,
    HELIPAD_APRIL,
)
from detection import (
    at_detector,
    process_image_A,
    calculate_alignment_A,
    calculate_alignment_H,
    process_image_H,
)
import smoke_jumper

DETECTION_TYPE = "A"


def get_battery(tello: Tello) -> str:
    try:
        battery = tello.get_battery()
    except TelloException as e:
        print(e)
        raise Exception("Could not get tello battery. Maybe not connected to tello?")

    return f"Battery: {battery}%"


def get_frames(tello: Tello):
    frame_read = tello.get_frame_read()
    frame = frame_read.frame
    img = frame
    dbg_img = img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dbg_img = cv2.cvtColor(dbg_img, cv2.COLOR_BGR2RGB)

    # lower_bound = np.array([0, 0, 0])
    # upper_bound = np.array([350, 55, 100])

    # img = cv2.inRange(img, lower_bound, upper_bound)

    # cv2.resize(img, 360, 240)

    return img, dbg_img


def _show_frame(img, show_img, detection_type: str):
    if detection_type == "A":
        tags = at_detector.detect(
            img, estimate_tag_pose=False, camera_params=None, tag_size=None
        )

        target = [6, 2]
        dbg_img = process_image_A(show_img, tags, target)

        cv2.waitKey(1)
        cv2.imshow("camera feed", dbg_img)

        return dbg_img, tags, target
    else:
        detected_circles = cv2.HoughCircles(
            img,
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=50,
            param2=30,
            minRadius=1,
            maxRadius=40,
        )
        dbg_img = process_image_H(show_img, detected_circles)
        cv2.waitKey(1)
        cv2.imshow("camera feed", dbg_img)

        return dbg_img, detected_circles

    cv2.waitKey(1)
    cv2.imshow("camera feed", show_img)

    return None


def show_frames(tello: Tello) -> None:
    img, dbg_img = get_frames(tello)
    return _show_frame(img, dbg_img, DETECTION_TYPE)


def align_tello(tello: Tello, detection_type: str) -> bool:
    height_level = 1
    while True:
        if detection_type == "A":
            DETECTION_TYPE = "A"
            dbg_img, tags, targets = show_frames(tello)
            amount_to_move = calculate_alignment_A(dbg_img, tags, targets)
        else:
            DETECTION_TYPE = "H"
            dbg_img, detected_circles = show_frames(tello)
            amount_to_move = calculate_alignment_H(dbg_img, detected_circles)

        if amount_to_move is True:
            break

        if amount_to_move is False:
            if height_level == 3:  # TODO: might change
                return False

            # move Tello higher
            tello.move_up(35)

            height_level += 1
            continue

        left_right, forward_backward = amount_to_move

        # actually aligning the tello
        if left_right > 0:
            tello.move_right(left_right)
            # tello.send_rc_control(0, -left_right, 0, 0)
        else:
            tello.move_left(-left_right)
            # tello.send_rc_control(0, -left_right, 0, 0)

        if forward_backward > 0:
            tello.move_forward(forward_backward)
            # tello.send_rc_control(-forward_backward, 0, 0, 0)
        else:
            tello.move_back(-forward_backward)
            # tello.send_rc_control(-forward_backward, 0, 0, 0)

        # sleep(1 / 10)
        # tello.send_rc_control(0, 0, 0, 0)


def enter_recon_path(tello: Tello) -> None:
    tello.takeoff()
    # align Tello just after the takeoff
    # align_tello(tello, "H")

    tello.move_up(100)  # TODO: might change
    tello.move_up(50)  # TODO: might change

    # move to April Tag
    tello.move_forward(HELIPAD_APRIL + 5)  # TODO: Might change
    # align Tello to April Tag
    align_tello(tello, "A")

    # move to school (no need for alignment bc the distance is short)
    tello.move_forward(APRIL_SCHOOL + 20)  # TODO: might change

    # droping the smoke jumper
    smoke_jumper.close_dropper()
    sleep(3)

    # rotate Tello 180 degrees
    tello.rotate_clockwise(180)

    # move to April Tag
    tello.move_forward(APRIL_SCHOOL + 10)
    # align Tello to April Tag
    align_tello(tello, "A")

    # move to the helipad
    tello.move_forward(HELIPAD_APRIL)
    # align Tello before landing
    # align_tello(tello, "H")

    tello.land()

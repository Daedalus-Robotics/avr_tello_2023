from djitellopy import Tello, TelloException
import cv2
import keyboard
from textual.app import App
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
from april_tag import at_detector, process_image, calculate_alignment
import smoke_jumper
import april_tag


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
    cv2.resize(dbg_img, 360, 240)

    return img, dbg_img


def _show_frame(img, dbg_img, detection_type: str):
    if april_tag.APRIL_TAG_DETECTION:
        tags = at_detector.detect(
            img, estimate_tag_pose=False, camera_params=None, tag_size=None
        )

        target = [6]
        dbg_img = process_image(dbg_img, tags, target)

        cv2.waitKey(1)
        cv2.imshow("camera feed", dbg_img)

        return dbg_img, tags, target

    cv2.waitKey(1)
    cv2.imshow("camera feed", dbg_img)

    return None


def show_frames(tello: Tello, detection_type=None) -> None:
    img, dbg_img = get_frames(tello)
    return _show_frame(img, dbg_img, detection_type)


def align_tello(tello: Tello, detection_type: str) -> bool:
    height_level = 1
    while True:
        # since APRIL_TAG_DETECTION flag is turned on, we always get these
        dbg_img, tags, targets = show_frames(tello, detection_type)
        amount_to_move = calculate_alignment(dbg_img, tags, targets)

        if amount_to_move is True:
            break

        if amount_to_move is False:
            if height_level == 3:  # TODO: might change
                return False

            # move Tello higher
            tello.move_up(15)  # TODO: might change

            height_level += 1
            continue

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

        sleep(1 / 2)


def enter_recon_path(tello: Tello) -> None:
    april_tag.APRIL_TAG_DETECTION = True

    tello.takeoff()
    # align Tello just after the takeoff
    align_tello(tello, "H")

    # move to April Tag
    tello.move_forward(HELIPAD_APRIL)
    # align Tello to April Tag
    align_tello(tello, "A")

    # move to school (no need for alignment bc the distance is short)
    tello.move_forward(APRIL_SCHOOL)

    # droping the smoke jumper
    smoke_jumper.open_dropper()
    smoke_jumper.close_dropper()

    # rotate Tello 180 degrees
    tello.rotate_clockwise(180)

    # move to April Tag
    tello.move_forward(APRIL_SCHOOL)
    # align Tello to April Tag
    align_tello(tello, "A")

    # move to the helipad
    tello.move_forward(HELIPAD_APRIL)
    # align Tello before landing
    align_tello(tello, "H")

    tello.land()

    april_tag.APRIL_TAG_DETECTION = False

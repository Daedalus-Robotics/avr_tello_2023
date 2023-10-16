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
)
from april_tag import at_detector, process_image, calculate_alignment, align_tello
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

    return img, dbg_img


def _show_frame(img, dbg_img):
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


def show_frames(tello: Tello) -> None:
    img, dbg_img = get_frames(tello)
    return _show_frame(img, dbg_img)


def enter_recon_path(tello: Tello) -> None:
    april_tag.APRIL_TAG_DETECTION = True

    # first recon path
    tello.takeoff()

    # TODO: Need april tag distance too!
    tello.move_forward(0)
    keyboard.wait("esc")

    # Align the drone
    align_tello(tello)

    tello.move_forward(SCHOOL_DISTANCE)

    # blocks until you press esc
    keyboard.wait("esc")

    smoke_jumper.open_dropper()
    smoke_jumper.close_dropper()

    tello.move_back(SCHOOL_DISTANCE)
    tello.land()

    april_tag.APRIL_TAG_DETECTION = False

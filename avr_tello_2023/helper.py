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
from april_tag import at_detector, process_image, target_action


def get_battery(tello: Tello) -> str:
    try:
        battery = tello.get_battery()
    except TelloException as e:
        print(e)
        raise Exception("Could not get tello battery. Maybe not connected to tello?")

    return f"Battery: {battery}%"


def show_frames(tello: Tello) -> None:
    frame_read = tello.get_frame_read()
    frame = frame_read.frame
    img = frame
    dbg_img = img

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tags = at_detector.detect(
        img, estimate_tag_pose=False, camera_params=None, tag_size=None
    )

    target = [6]
    dbg_img = process_image(dbg_img, tags, target)

    # move the tello
    tello.send_rc_control(*target_action(target))

    cv2.waitKey(1)
    cv2.imshow("camera feed", dbg_img)


def enter_recon_path(tello: Tello) -> None:
    # first recon path
    tello.takeoff()
    tello.move_forward(SCHOOL_DISTANCE)

    # blocks until you press esc
    # TODO: should I fix this later?
    keyboard.wait("esc")

    # TODO: HERE IS WHERE CODE GO FOR PARACHUTE DROP

    tello.move_back(SCHOOL_DISTANCE)
    tello.land()

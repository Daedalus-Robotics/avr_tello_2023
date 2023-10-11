from djitellopy import Tello, TelloException
import cv2
import keyboard
from textual.app import App

from inspect import signature
from platform import system
from threading import Thread
from typing import List
from time import sleep

from constants import BACK_BRIDGE_DISTANCE, BACK_TO_MIDDLE_BRIDGE_DISTANCE, SCHOOL_DISTANCE

def get_battery(tello: Tello) -> str:
    try:
        battery = tello.get_battery()
    except TelloException as e:
        print(e)
        raise Exception('Could not get tello battery. Maybe not connected to tello?')
    
    return f'Battery: {battery}%'

def show_frames(tello: Tello) -> None:
    frame_read = tello.get_frame_read()
    while True:
        frame = frame_read.frame
        img = cv2.resize(frame, (360, 240))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('camera feed', img)

def get_color(tello: Tello) -> None:
    tello.takeoff()
    tello.move_up(100)  # needs to check this distance go over the building
    tello.rotate_clockwise(180)
    tello.move_forward(BACK_BRIDGE_DISTANCE)
    tello.move_right(BACK_TO_MIDDLE_BRIDGE_DISTANCE)
    tello.rotate_clockwise(180)

    # blocks until you press esc
    # TODO: should I fix this later?
    keyboard.wait('esc')

    tello.move_forward(BACK_BRIDGE_DISTANCE)
    tello.move_right(BACK_TO_MIDDLE_BRIDGE_DISTANCE)
    tello.land()


def enter_recon_path(tello: Tello) -> None:
    # first recon path
    tello.takeoff()
    tello.move_forward(SCHOOL_DISTANCE)
    
    # blocks until you press esc
    # TODO: should I fix this later?
    keyboard.wait('esc')
    
    # TODO: HERE IS WHERE CODE GO FOR PARACHUTE DROP
    
    tello.move_back(SCHOOL_DISTANCE)
    tello.land()


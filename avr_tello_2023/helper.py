from djitellopy import Tello, TelloException
import cv2
import keyboard
from textual.app import App

from inspect import signature
from threading import Thread

from constants import BACK_BRIDGE_DISTANCE, BACK_TO_MIDDLE_BRIDGE_DISTANCE, SCHOOL_DISTANCE

def get_battery(tello: Tello) -> str:
    try:
        battery = tello.get_battery()
    except TelloException:
        raise Exception('Could not get tello battery. Maybe not connected to tello?')
    
    return f'Battery: {battery}%'

def start_threads(tello: Tello, app: App) -> None:
    Thread(
            target=show_frames,
            args=(tello,),
            daemon=True
    ).start()

def show_frames(tello: Tello) -> None:
    while True:
        frame = tello.get_frame_read().frame
        frame = cv2.resize(frame, (360, 240))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("CAM", frame)

def enter_manual_mode(tello: Tello) -> None:
    """
        Enters Manual Mode

        Commands are:
         - w: moves the drone forward
         - s: moves the drone backward
         - d: moves the drone right
         - a: moves the drone left
         - t: takeoff
         - l: lands
    """
    distance = 80
    manual_commands = {  # I could've used a match statement, but IDK, I just felt like using this instead.
        'w': tello.move_forward,
        's': tello.move_back,
        'd': tello.move_right,
        'a': tello.move_left,
        't': tello.takeoff,
        'l': tello.land,
    }

    while True:
        for letter, func in manual_commands.items():
            if keyboard.is_pressed(letter):
                # checking for the number of arguments the function takes
                if len(signature(func).parameters) > 0:
                    # noinspection PyArgumentList
                    func(distance)
                else:
                    func()
            elif keyboard.is_pressed('q'):
                # getting outta manual mode
                return


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


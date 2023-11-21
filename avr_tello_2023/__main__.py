from djitellopy import Tello
import keyboard

from helper import (
    align_tello,
    enter_recon_path,
    clamp_x_y,
    adjust_to_tello_rc,
)
from pythondualsense import Dualsense
import helper

from smoke_jumper import scan_ports, configure
from smoke_jumper import close_dropper as drop
from smoke_jumper import open_dropper as close_dropper
from helper import show_frame
from sys import exit
from time import sleep


def move_tello_x_y(pos: tuple[int, int]) -> None:
    (x, y) = clamp_x_y(*pos)
    (x, y) = adjust_to_tello_rc(x, y)
    tello.send_rc_control(x, -y, 0, 0)


def move_tello_z(pos: tuple[int, int]) -> None:
    (x, y) = clamp_x_y(*pos)
    (x, y) = adjust_to_tello_rc(x, y)
    tello.send_rc_control(0, 0, -y, x)


def drop_smokejumper() -> None:
    drop()
    sleep(1)
    close_dropper()


def setup_controller(dualsense: Dualsense) -> None:
    dualsense.right_stick.on_move.register(move_tello_x_y)
    dualsense.left_stick.on_move.register(move_tello_z)
    dualsense.left_bumper.on_press.register(tello.takeoff)
    dualsense.right_bumper.on_press.register(tello.land)
    dualsense.right_trigger.on_press.register(drop_smokejumper)
    dualsense.triangle.on_press.register(tello.send_keepalive)


def run_app(tello: Tello) -> None:
    detection_type = "A"
    frame_read = tello.get_frame_read()

    while True:
        # if keyboard.is_pressed("a"):
        #     align_tello(tello, frame_read, "A")
        # elif keyboard.is_pressed("A"):
        #     align_tello(tello, frame_read, "H")
        # elif keyboard.is_pressed("s"):
        #     align_tello(tello, frame_read, "S")
        # elif keyboard.is_pressed("B"):
        #     battery = tello.get_battery()
        #     Tello.LOGGER.info(f"Tello battery: {battery}%")
        # elif keyboard.is_pressed("c"):
        #     if helper.DIRECTION:
        #         tello.set_video_direction(Tello.CAMERA_FORWARD)
        #         helper.DIRECTION = False
        #     else:
        #         tello.set_video_direction(Tello.CAMERA_DOWNWARD)
        #         helper.DIRECTION = True
        # elif keyboard.is_pressed("d"):
        #     if detection_type == "A":
        #         detection_type = "H"
        #     else:
        #         detection_type = "A"
        # elif keyboard.is_pressed("D"):
        #     detection_type = "S"
        # elif keyboard.is_pressed("r"):
        #     enter_recon_path(tello)
        # elif keyboard.is_pressed("q"):
        #     break
        # elif keyboard.is_pressed("Q"):
        #     tello.emergency()
        show_frame(tello, frame_read, detection_type)
        sleep(0.1)


if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    tello.streamon()
    # tello.set_video_fps(Tello.FPS_30)

    tello.set_video_direction(Tello.CAMERA_DOWNWARD)

    # disable Tello logger
    Tello.LOGGER.disabled = True

    # port = scan_ports()[0]
    # configure(port)

    # set up for the controller
    # dualsense_controller = Dualsense()
    # dualsense_controller.open()
    # setup_controller(dualsense_controller)

    # if not dualsense_controller.is_open:
    #     Tello.LOGGER.error("Dualsense controller not connected")
    #     exit(1)

    try:
        run_app(tello)
    finally:
        tello.end()

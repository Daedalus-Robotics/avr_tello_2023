from djitellopy import Tello
import cv2
import keyboard

tello = Tello()
tello.connect()
tello.streamon()

school_distance = 359  # distance to the school building in cm from helipad
back_bridge_distance = 620  # distance from helipad to back of bridge line in cm
back_to_middle_bridge_distance = 190  # distance from the back of the bridge to the middle where color square is (needs to be calibrated)

print(tello.get_battery())
try:
    while True:
        img = tello.get_frame_read().frame  #
        cv2.imshow('frame', img)
        cv2.waitKey(1)

        if keyboard.is_pressed('r'):
            # first recon path
            tello.takeoff()
            tello.move_forward(school_distance)
            # HERE IS WHERE CODE GO FOR PARACHUTE DROP
            tello.move_back(school_distance)
            tello.land()
        elif keyboard.is_pressed('c'):
            # tello code to get color from building
            tello.takeoff()
            tello.move_up(100)  # needs to check this distance go over the building
            tello.rotate_clockwise(180)
            tello.move_forward(back_bridge_distance)
            tello.move_right(back_to_middle_bridge_distance)
            tello.rotate_clockwise(180)
            # implement a wait key to show color to people
            tello.move_forward(back_bridge_distance)
            tello.move_right(back_to_middle_bridge_distance)
            tello.land()
except KeyboardInterrupt:
    exit(1)

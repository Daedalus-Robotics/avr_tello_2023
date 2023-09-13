from djitellopy import Tello
import cv2

from inspect import signature

tello = Tello()
tello.connect()
tello.streamon()

school_distance = 359  # distance to the school building in cm from helipad
back_bridge_distance = 620  # distance from helipad to back of bridge line in cm
back_to_middle_bridge_distance = 190  # distance from the back of the bridge to the middle where color square is (needs to be calibrated)

battery_left = tello.get_battery()

print(f"tello battery: {battery_left}%")

def enter_manual_mode():
    distance = 50
    
    # I could've used match statement, but IDK, I just felt like using this instead.
    commands = {
        ord('w'): tello.move_forward,
        ord('s'): tello.move_back,
        ord('d'): tello.move_right,
        ord('a'): tello.move_left,
        ord('t'): tello.takeoff,
        ord('l'): tello.land,
    }
    
    # commands in human-readable format
    commands_str = "\n".join([f"{letter}: {func.__name__}" for letter, func in commands.items()])

    while True:
        key = cv2.waitKey(1)
        for letter, func in commands.items():
            if key == letter:
                # checking for the number of arguments the function takes
                if len(signature(func).parameters) == 1:
                    func(distance)
                else:
                    func()
            elif key == ord('m'):
                # getting outta manual mode
                return
            else:
                print(f"Invalid command '{letter}'")
                print(f"Command list: \n{commands_str}")

def main():
    while True:
       img = tello.get_frame_read().frame  #
       cv2.imshow('frame', img)
       key = cv2.waitKey(1)

       if key == ord('r'):
           # first recon path
           tello.takeoff()
           tello.move_forward(school_distance)
           # HERE IS WHERE CODE GO FOR PARACHUTE DROP
           tello.move_back(school_distance)
           tello.land()
       elif key == ord('c'):
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
       elif key == ord('m'): # manual mode
           enter_manual_mode()

if __file__ == 'main':
    try:
        main()
    except KeyboardInterrupt:
        tello.land()
        exit(1)
    finally:
        tello.land()

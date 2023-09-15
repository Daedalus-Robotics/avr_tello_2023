from djitellopy import Tello
import cv2
import keyboard

from inspect import signature

tello = Tello()
tello.connect()
tello.streamon()

school_distance = 359  # distance to the school building in cm from helipad
back_bridge_distance = 620  # distance from helipad to back of bridge line in cm
back_to_middle_bridge_distance = 190  # distance from the back of the bridge to the middle where color square is (needs to be calibrated)
manual_commands = {                 # I could've used match statement, but IDK, I just felt like using this instead.
    'w': tello.move_forward,
    's': tello.move_back,
    'd': tello.move_right,
    'a': tello.move_left,
    't': tello.takeoff,
    'l': tello.land,
}
manual_commands_str = "\n".join([f"{letter}: {func.__name__}" for letter, func in manual_commands.items()]) # commands in human-readable format
battery_left = tello.get_battery() # how much batter left

def enter_manual_mode():
    """
        Enters Manual Mode

        Commands are:
         - w: moves the drone forward
         - s: moves the drone backword
         - d: moves the drone right
         - a: moves the drone left
         - t: takeoff
         - l: lands
    """
    distance = 50
    
    while True:
        for letter, func in manual_commands.items():
            if keyboard.is_pressed(letter):
                # checking for the number of arguments the function takes
                if len(signature(func).parameters) == 1:
                    func(distance)
                else:
                    func()
            elif keyboard.is_pressed('q'):
                # getting outta manual mode
                return

def get_color():
    """ TODO """
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

def enter_recon_path():
    """ TODO """
    # first recon path
    tello.takeoff()
    tello.move_forward(school_distance)
    # HERE IS WHERE CODE GO FOR PARACHUTE DROP
    tello.move_back(school_distance)
    tello.land()

def main():
    while True:
        img = tello.get_frame_read().frame
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow('frame', img)
       
        if keyboard.is_pressed('r'):
            enter_recon_path()
        elif keyboard.is_pressed('c'):
            get_color()
        elif keyboard.is_pressed('m'):
            enter_manual_mode()

if __name__ == '__main__':
    Tello.LOGGER.info(f"Battery: {battery_left}%")

    try:
        main()
    except KeyboardInterrupt:
        tello.land()
        exit(1)
    finally:
        tello.land()

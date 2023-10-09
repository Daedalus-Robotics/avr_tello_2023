CSS_PATH = './style.tcss'

SCHOOL_DISTANCE = 359  # distance to the school building in cm from helipad

BACK_BRIDGE_DISTANCE = 620  # distance from helipad to back of bridge line in cm

# TODO: Calibrate distance
BACK_TO_MIDDLE_BRIDGE_DISTANCE = 190  # distance from the back of the bridge to the middle where color square is

# key, action, description
MANUAL_MODE_COMMANDS = [
    ('q', 'request_quit_manual', 'Quit Manual Mode'),
    ('Q', 'request_force_quit', 'Force quit'),
    ('w', 'move_forward', "Moves the Tello drone forward"),
    ('a', 'move_left', "Moves the Tello drone left"),
    ('d', 'move_right', "Moves the Tello drone right"),
    ('s', 'move_backward', "Moves the Tello drone backward"),
    ('e', 'rotate_ccw', 'Rotates the Tello drone counter clockwise'),
    ('r', 'rotate_cw', 'Rotates the Tello drone clockwise'),
    ('f', 'move_up', 'Moves the Tello drone upward'),
    ('c', 'move_down', 'Moves the Tello drone downward'),
    ('l', 'land', 'Lands the Tello drone'),
    ('t', 'takeoff', 'Take off!'),
]

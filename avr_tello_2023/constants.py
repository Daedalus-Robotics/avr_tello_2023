CSS_PATH = "./style.tcss"

# TODO: add APRIL_TAG_DISTANCE

SCHOOL_DISTANCE = 359  # distance to the school building in cm from helipad
HELIPAD_APRIL = 231
APRIL_SCHOOL = 128
BACK_BRIDGE_DISTANCE = 620  # distance from helipad to back of bridge line in cm

# TODO: Calibrate distance
BACK_TO_MIDDLE_BRIDGE_DISTANCE = (
    190  # distance from the back of the bridge to the middle where color square is
)

# key, action, description
MANUAL_MODE_COMMANDS = [
    ("q", "Quit Manual Mode"),
    ("Q", "Force quit"),
    ("w", "Moves the Tello drone forward"),
    ("a", "Moves the Tello drone left"),
    ("d", "Moves the Tello drone right"),
    ("s", "Moves the Tello drone backward"),
    ("D", "Rotates the Tello drone counter clockwise"),
    ("A", "Rotates the Tello drone clockwise"),
    ("W", "Moves the Tello drone upward"),
    ("S", "Moves the Tello drone downward"),
    ("l", "Lands the Tello drone"),
    ("t", "Take off!"),
]

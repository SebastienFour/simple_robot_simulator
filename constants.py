# Display management
INVISIBLE = (111, 111, 0)
WHITE = 255, 240, 200
BLACK = 20, 20, 40
gold = [212, 175, 55]
WINSIZE = [1500, 840]
WINCENTER = [WINSIZE[0] / 2, WINSIZE[1] / 2]
OFFSET = [300, 100]
CENTER_COLOR = [200, 0, 0]
CENTER_SIZE = 10
WHEEL_COLOR = [0, 0, 150]
WHEEL_SIZE = 10
GOAL_COLOR = [0, 150, 0]
GOAL_SIZE = 5
FAKE_COLOR = [100, 100, 100]
FAKE_SIZE = CENTER_SIZE / 4
# 1 meter is METERS_TO_PIXEL pixels
METERS_TO_PIXEL = 1000

# Control management
WHEEL_SPEED_INC = 0.0002 * 60
XY_TOL = 5 / 1000.0
TURN_P = 0.03 * 60
SPEED_P = 0.01 * 60

# Mecanical values
# Distance between the wheels in meters
L = 0.120
# Radius of the wheels in meters
R = 0.0325

# Modes management
XY_GOAL = "XY_GOAL"
WHEEL_CONTROL = "WHEEL_CONTROL"

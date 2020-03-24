import sys


class Motor(object):
    """
    Represents the state of one motor 
    """

    def __init__(self):
        # Usually each motor has an encoder. Differentiating the encoder gives an estimation of the rotational speed in steps/s.
        # The formula to calculate the linear speed in m/s would then be : (rot_speed_steps_per_s / STEPS_PER_FULL_ROTATION) * 2 * math.pi * wheel_radius
        # For now, the speed control is assumed perfect and instantaneous. This 'speed' is the linear speed of the wheel in m/s.
        self.speed = 0

    def __repr__(self):
        s = "speed : {}".format(self.speed)
        return s


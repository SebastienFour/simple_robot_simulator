#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, math, pygame
import pygame.draw
from pygame.locals import *
import sys
import os
import copy
import motor
import model
from constants import *


class SimpleRobotControl:
    def __init__(self):
        self.control_modes = [XY_GOAL, WHEEL_CONTROL]
        self.control_mode_id = 0
        self.m = model.Model()
        self.m.x_goal = 0.05
        self.m.y_goal = 0.05
        self.mode = self.get_mode()
        self.clock = pygame.time.Clock()
        self.t0 = pygame.time.get_ticks() / 1000.0
        self.is_artist = False
        self.update_period = 1 / 60.0
        # initialize and prepare screen
        pygame.init()
        self.screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption("Simple Robot simulator")
        # Font init
        self.font = pygame.font.SysFont("monospace", 30)
        self.small_font = pygame.font.SysFont("monospace", 20)
        self.screen.fill(BLACK)

    def get_mode(self):
        return self.control_modes[self.control_mode_id]

    def set_next_mode(self):
        self.control_mode_id = (self.control_mode_id + 1) % len(self.control_modes)

    def draw_robot(self, m=None, fake=False):
        if m == None:
            m = self.m
        # Usually, we have X in front of us and Y to the left. Let's keep that : y = -y, theta = theta-pi/2
        center_pos = [
            int(m.x * METERS_TO_PIXEL + WINCENTER[0]),
            int(-m.y * METERS_TO_PIXEL + WINCENTER[1]),
        ]
        color = CENTER_COLOR
        size = CENTER_SIZE
        if fake:
            color = FAKE_COLOR
            size = int(FAKE_SIZE)
        pygame.draw.circle(self.screen, color, center_pos, int(size), 0)

        r = m.l / 2.0
        theta = m.theta - math.pi / 2
        wheel_pos = [
            int(
                m.x * METERS_TO_PIXEL
                + WINCENTER[0]
                + r * METERS_TO_PIXEL * math.cos(theta)
            ),
            int(
                -m.y * METERS_TO_PIXEL
                + WINCENTER[1]
                - r * METERS_TO_PIXEL * math.sin(theta)
            ),
        ]
        color = WHEEL_COLOR
        size = WHEEL_SIZE
        if fake:
            color = FAKE_COLOR
            size = FAKE_SIZE
        pygame.draw.circle(self.screen, color, wheel_pos, int(size), 0)

        wheel_pos = [
            int(
                m.x * METERS_TO_PIXEL
                + WINCENTER[0]
                - r * METERS_TO_PIXEL * math.cos(theta)
            ),
            int(
                -m.y * METERS_TO_PIXEL
                + WINCENTER[1]
                + r * METERS_TO_PIXEL * math.sin(theta)
            ),
        ]
        pygame.draw.circle(self.screen, color, wheel_pos, int(size), 0)

    def draw_goal(self):
        # Usually, we have X in front of us and Y to the left. Let's keep that : y = -y, theta = theta-pi/2
        center_pos = [
            int(self.m.x_goal * METERS_TO_PIXEL + WINCENTER[0]),
            int(-self.m.y_goal * METERS_TO_PIXEL + WINCENTER[1]),
        ]
        pygame.draw.circle(self.screen, GOAL_COLOR, center_pos, int(GOAL_SIZE), 0)

    def draw_state(self):
        self.draw_robot()
        self.draw_goal()

    def play(self):
        """ An inifinite loop that manages the display and the robot interactions
        """
        print("Current mode is '{}'".format(self.get_mode()))
        speed_multiplier = 1
        while True:
            mode = self.get_mode()
            # 'e' for 'event'
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                elif e.type == KEYUP:
                    if e.key == pygame.K_LCTRL:
                        speed_multiplier = 1
                elif e.type == KEYDOWN:
                    key = e.dict["unicode"]
                    if e.key == pygame.K_LCTRL:
                        speed_multiplier = 10
                    if key == "q":
                        print("Rage quit!")
                        return 0
                    if key == "a":
                        self.is_artist = not (self.is_artist)
                        if self.is_artist:
                            self.screen.fill(BLACK)
                    if e.key == pygame.K_TAB:
                        self.set_next_mode()
                    if e.key == pygame.K_SPACE:
                        self.m.m1.speed = 0
                        self.m.m2.speed = 0
                    if e.key == pygame.K_UP:
                        self.m.m1.speed = (
                            self.m.m1.speed + WHEEL_SPEED_INC * speed_multiplier
                        )
                    if e.key == pygame.K_DOWN:
                        self.m.m1.speed = (
                            self.m.m1.speed - WHEEL_SPEED_INC * speed_multiplier
                        )
                    if e.key == pygame.K_RIGHT:
                        self.m.m2.speed = (
                            self.m.m2.speed + WHEEL_SPEED_INC * speed_multiplier
                        )
                    if e.key == pygame.K_LEFT:
                        self.m.m2.speed = (
                            self.m.m2.speed - WHEEL_SPEED_INC * speed_multiplier
                        )
                elif e.type == pygame.MOUSEMOTION:
                    mx, my = e.pos
                elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                    self.m.x_goal = (mx - WINCENTER[0]) / METERS_TO_PIXEL
                    self.m.y_goal = -(my - WINCENTER[1]) / METERS_TO_PIXEL
            if not (self.is_artist):
                self.screen.fill(BLACK)
            if mode == XY_GOAL:
                self.asserv()
            elif mode == WHEEL_CONTROL:
                None
            else:
                print("ERROR: mode '{}' is unknown".format(mode))
                sys.exit()
            self.m.update(self.update_period)

            # Creating a fake robot to trace the future :)
            fake_m = copy.deepcopy(self.m)
            for i in range(30):
                if mode == XY_GOAL:
                    self.asserv(m=fake_m)
                fake_m.update(10 * self.update_period)
                self.draw_robot(m=fake_m, fake=True)

            self.draw_state()
            # print(self.m)
            t = pygame.time.get_ticks() / 1000.0 - self.t0
            linear_speed, rotation_speed = self.m.dk()

            # Writing new text
            self.screen.blit(
                self.font.render("Simple Robot Simulator", 1, gold), [0, 0]
            )
            if self.is_artist:
                self.screen.blit(
                    self.font.render("Artist mode!", 1, (0, 150, 0)), [20, 30]
                )
            else:
                self.screen.blit(
                    self.small_font.render(
                        "q: quit, tab: next mode, mouse: goal position, arrows: wheel speed control, space: speed 0 to wheels, a: artist toggle",
                        1,
                        (0, 150, 0),
                    ),
                    [20, 30],
                )
                self.screen.blit(
                    self.small_font.render("Time: {0:.2f}".format(t), 1, (0, 150, 0)),
                    [20, 60],
                )
                self.screen.blit(
                    self.small_font.render(
                        "Mode: {}, artist: {}".format(
                            self.get_mode(), "True" if self.is_artist else "False"
                        ),
                        1,
                        (0, 150, 0),
                    ),
                    [20, 90],
                )
                self.screen.blit(
                    self.small_font.render(
                        "Left wheel speed: {0:.2f} mm/s".format(1000 * self.m.m1.speed),
                        1,
                        (0, 150, 0),
                    ),
                    [20, 120],
                )
                self.screen.blit(
                    self.small_font.render(
                        "Right wheel speed: {0:.2f} mm/s".format(
                            1000 * self.m.m2.speed
                        ),
                        1,
                        (0, 150, 0),
                    ),
                    [20, 150],
                )
                self.screen.blit(
                    self.small_font.render(
                        "Linear speed: {0:.2f} mm/s".format(1000 * linear_speed),
                        1,
                        (0, 150, 0),
                    ),
                    [20, 180],
                )
                self.screen.blit(
                    self.small_font.render(
                        "Angular speed: {0:.3f} rad/s".format(rotation_speed),
                        1,
                        (0, 150, 0),
                    ),
                    [20, 210],
                )

            pygame.display.update()
            # That juicy 60 Hz :D
            self.clock.tick(1 / self.update_period)

    def asserv(self, m=None):
        """Sets the speeds of the 2 motors to get the robot to its destination point
        """
        if m == None:
            m = self.m
        distance = math.sqrt(
            (m.x_goal - m.x) * (m.x_goal - m.x) + (m.y_goal - m.y) * (m.y_goal - m.y)
        )

        # TODO
        local_speed = 0
        local_turn = 0

        m1_speed, m2_speed = m.ik(local_speed, local_turn)
        m.m1.speed = m1_speed
        m.m2.speed = m2_speed

    def angle_diff(self, a, b):
        """Returns the smallest distance between 2 angles
        """
        # TODO
        d = 0
        return d


def main():
    robot = SimpleRobotControl()

    result = robot.play()

    sys.exit()


# if python says run, then we should run
if __name__ == "__main__":
    main()

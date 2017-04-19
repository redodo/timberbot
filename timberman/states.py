# -*- coding: utf-8 -*-
from time import sleep
from evdev import ecodes as e
from .colors import Color
from .core import State
from .utils import avg, contrast, sample

from pprint import pprint


class StartState(State):
    def cycle(self):
        if self.screen[0.442, 0.923] == Color.RED:
            self.game.enter(SinglePlayerGameState)
        elif self.screen[930, 480] == Color.WHITE and \
                self.screen[930, 490] == Color.BLACK and \
                self.screen[1000, 540] == Color.BLACK and \
                self.screen[988, 488] == Color.BLACK and \
                self.screen[931, 501] == Color.WHITE:
            if sum(self.screen[310, 800]) < 30 and \
                    sum(self.screen[705, 800]) < 30 and \
                    sum(self.screen[1495, 800]) < 30:
                self.game.enter(FourMPGameState)
            else:
                self.game.enter(TwoMPGameState)


class GameState(State):
    LX, RX = 0, 1
    FY, TY = 0, 1
    MOVE_LEFT = e.KEY_A
    MOVE_RIGHT = e.KEY_D

    def enter(self):
        self.last_move = self.MOVE_LEFT
        self.pre_last_move = self.MOVE_LEFT

    def cycle(self):
        if self.screen[0.5, 0.5] == Color.BLACK:
            return

        # have we failed? (this should never happen)
        if self.has_failed():
            self.game.enter(StartState)
            return

        move = self.last_move
        if self.last_move == self.MOVE_LEFT:
            # we are on the left side
            line = self.read_line(self.LX)
            if any(line):
                # obstacle incoming, move right
                move = self.MOVE_RIGHT
        else:
            # we are on the right side
            line = self.read_line(self.RX)
            if any(line):
                # obstacle incoming, move left
                move = self.MOVE_LEFT

        # error correction
        if self.pre_last_move == move:
            move = self.last_move

        # perform the move
        self.keyboard.press(move)
        self.pre_last_move = self.last_move
        self.last_move = move

    def read_line(self, x, y1=None, y2=None):
        y1 = self.FY if y1 is None else y1
        y2 = self.TY if y2 is None else y2
        fresh_buffer = []
        # get fresh pixels
        pixels = [self.screen[x, y] for y in range(y1, y2)]
        for pixel in pixels:
            # apply grayscale, contrast, and invert
            value = 1 if avg(pixel) < 10 else 0
            fresh_buffer.append(value)
        return sample(fresh_buffer, 6)

    def has_failed(self):
        return False


class SinglePlayerGameState(GameState):
    LX, RX = 750, 1170
    FY, TY = 450, 660

    def has_failed(self):
        return self.screen[0.5, 0.9] == Color.RED


class TwoMPGameState(SinglePlayerGameState):
    LX, RX = 505, 715
    FY, TY = 455, 660


class FourMPGameState(SinglePlayerGameState):
    LX, RX = 308, 426
    FY, TY = 650, 750

    def has_failed(self):
        return self.screen[0.5, 0.676] == Color.RED

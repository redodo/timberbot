# -*- coding: utf-8 -*-
import time
from .core import Keyboard, ScreenBuffer
from .states import StartState


class Timberman(object):
    def __init__(self, mps=10):
        """
        Maximum scores for each mps:

            1 mps -> 8
            2 mps -> 22
            3 mps -> 59
            4 mps -> 157
            5 mps -> 327
            6 mps -> 627
            8 mps -> 3552
        """
        self.screen = ScreenBuffer()
        self.keyboard = Keyboard()
        self.state = None
        self.state_acc = 0
        self._clock = 1 / mps

    def run(self):
        self.enter(StartState)
        self.running = True
        while self.running:
            start = time.time()
            self.cycle()
            sleeplen = self._clock - (time.time() - start)
            time.sleep(max(sleeplen, 0))

    def enter(self, state):
        if self.state is not None:
            self.state.leave()
        self.state = state(self)
        self.state_acc += 1
        print('{:02}: Entering {}'.format(self.state_acc, self.state))
        self.state.enter()

    def cycle(self):
        self.screen.refresh()
        self.state.cycle()

    def exit(self):
        self.running = False
        self.state.leave()

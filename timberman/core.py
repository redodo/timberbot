# -*- coding: utf-8 -*-
import time
import copy
from evdev import UInput, ecodes as e
from mss import mss
from PIL import Image


class ScreenBuffer(object):
    CHANNELS = 3

    def __init__(self, monitor=1):
        self.monitor = monitor
        self._monitors = None
        self.refresh()

    def _nth(self, x, y):
        if isinstance(x, float):
            x = int(self.width * x)
        if isinstance(y, float):
            y = int(self.height * y)
        return (x + self.width * y) * self.CHANNELS

    def __getitem__(self, position):
        n = self._nth(*position)
        return list(self._buffer[n:n+self.CHANNELS])

    def __setitem__(self, position, value):
        n = self._nth(*position)
        self._buffer[n:n+self.CHANNELS] = bytes(value)

    def refresh(self):
        sct = mss()
        if self._monitors is None:
            self._monitors = list(sct.enum_display_monitors())
        if isinstance(self.monitor, dict):
            monitor = self.monitor
        else:
            monitor = self._monitors[self.monitor]
        self.width = monitor['width']
        self.height = monitor['height']
        self._buffer = sct.get_pixels(monitor)
        return True

    def dump(self):
        with Image.frombytes('RGB', self.size, self._buffer) as image:
            image.save('dumps/{}.png'.format(time.time()))

    @property
    def size(self):
        return self.width, self.height


class Keyboard(object):
    def __init__(self):
        self.ui = UInput()

    def press(self, key):
        self.ui.write(e.EV_KEY, key, 1)
        self.ui.write(e.EV_KEY, key, 0)
        self.ui.syn()

    def __del__(self):
        self.ui.close()


class State(object):
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.keyboard = self.game.keyboard

    def enter(self):
        pass

    def cycle(self):
        pass

    def leave(self):
        pass

    def __str__(self):
        return self.__class__.__name__

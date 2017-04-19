# -*- coding: utf-8 -*-


def avg(numbers):
    return sum(numbers) / len(numbers)


def contrast(x, a, b=0):
    x -= b
    f = (259 * (a + 255)) / (255 * (259 - a))
    v = int(f * (x - 128) + 128)
    return min(max(v, 0), 255)


def sample(l, a):
    v = []
    for i in range(0, len(l), a):
        v.append(l[i])
    return v

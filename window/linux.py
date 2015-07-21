import autopy
import numpy
import time
import re
import wnck
from pyscreenshot import grab
from subprocess import check_output, CalledProcessError


def get_windowsize():
    name = 'Mines'
    try:
        out = check_output(['xwininfo', '-name', name])
    except CalledProcessError:
        return None, None, None, None

    pattern = r'.*Absolute upper-left X:  (?P<x>\d+).*' \
              r'Absolute upper-left Y:  (?P<y>\d+).*' \
              r'Width: (?P<w>\d+).*Height: (?P<h>\d+)'
    m = re.match(pattern, out, re.DOTALL)
    if m is None:
        return None
    d = m.groupdict()
    return int(d['x']), int(d['y']), int(d['w']), int(d['h'])


def set_focus(name):
    screen = wnck.screen_get_default()
    screen.force_update()
    windows = screen.get_windows()
    for w in windows:
        if name == w.get_name():
            w.activate(int(time.time()))
            break


def get_game_screen():
    name = 'Mines'
    x, y, w, h = get_windowsize()
    set_focus(name)
    autopy.mouse.smooth_move(x-1, 0)
    im = grab(bbox=(x, y, x+w, y+h), backend='imagemagick')
    # im.save('/home/avraham/screen.png')
    return im
    # array = numpy.asarray(im)
    # array = numpy.reshape(array, 516*678*3)
    # return array

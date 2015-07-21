import win32gui
import pyscreenshot as ImageGrab


def get_windowsize():
    win = win32gui.FindWindow(None, 'Minesweeper')
    return _get_windowsize(win)


def _get_windowsize(win):
    rect = win32gui.GetWindowRect(win)
    x = rect[0]
    y = rect[1]
    x2 = rect[2]
    y2 = rect[3]
    return x, y, y2, x2


def get_game_screen():
    win = win32gui.FindWindow(None, 'Minesweeper')
    x, y, x2, y2 = _get_windowsize(win)
    win32gui.SetForegroundWindow(win)
    im = ImageGrab.grab(bbox=(x, y, y2, x2))  # X1,Y1,X2,Y2
    # im.show()
    return im

import cv2
import numpy
import autopy

# from pybrain import TanhLayer
from pybrain.tools.shortcuts import buildNetwork
# from pybrain.supervised.trainers import BackpropTrainer
# from pybrain.datasets import SupervisedDataSet
#
# net = buildNetwork(2, 3, 1)
#
# print(net.activate([2, 1]))
#
# ds = SupervisedDataSet(2, 1)
# ds.addSample((0, 0), (0,))
# ds.addSample((0, 1), (1,))
# ds.addSample((1, 0), (1,))
# ds.addSample((1, 1), (0,))
#
# net = buildNetwork(2, 3, 1, bias=True, hiddenclass=TanhLayer)
# trainer = BackpropTrainer(net, ds)
# trainer.train()
import time
from window import get_game_screen, get_windowsize


def kp_to_array(kp):
    return numpy.array([[p.pt[0], p.pt[1], p.response] for p in kp])


def opencv_feature(image):
    """Use opencv to convert the image to a feature map
    """
    # convert from pillow image to opencv image

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    fast = cv2.FastFeatureDetector()
    kp = fast.detect(image, None)
    array = kp_to_array(kp)
    img2 = cv2.drawKeypoints(image, kp, color=(255, 0, 0))

    cv2.imshow('dst', img2)
    return array


def think(image):
    feature = opencv_feature(image)

    cv2.waitKey(0)
    # decide where to click, return x, y coordination
    return 1, 1

def click(x, y):
    x, y = int(x), int(y)
    x1, y1, w, h = get_windowsize()
    print(x1, y1, w, h)
    print(x, y)
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    # add game window offset
    x += x1
    y += y1
    # check boundries, can only click within game window
    if x >= x1 + w:
        x = x1 + w - 1
    if y >= y1 + h:
        y = y1 + h - 1
    print(x, y)
    # autopy.mouse.move(x, y)
    autopy.mouse.smooth_move(x, y)
    autopy.mouse.click()

def play():
    net = buildNetwork(475*600*3, 30, 2)
    # net = buildNetwork(409*364*3, 3, 2)
    prev_state = None
    while True:
        time.sleep(1)
        # get screenshot from game window
        screen = get_game_screen()
        # convert pillow image to numpy array
        array = numpy.array(screen)
        print(len(array))
        # array = numpy.reshape(array, 409*364*3)
        array = array.flatten()
        print(len(array))
        if prev_state is not None and numpy.array_equal(prev_state, array):
            # game stalled, previous state equals to current state
            # losing would get to this point also, no difference
            # between stalling and losing
            break
        prev_state = array
        # crop to only game area
        # turn screenshot to black/white
        # get decision from brain
        # decision = think(img)
        # print(len(screen))
        decision = net.activate(array)
        print(decision)
        # execute decision
        click(decision[0], decision[1])

        # decide if game finished or stalled
        # break

if __name__ == '__main__':
    # start game
    play()
import glob


def a():
    return glob.Joystick.get_button(8)


def b():
    return glob.Joystick.get_button(1)


def c():
    return glob.Joystick.get_button(4)


def d():
    return glob.Joystick.get_axis(1) < - .5


def e():
    return glob.Joystick.get_axis(1) > .5


def f():
    return glob.Joystick.get_axis(0) < -.5


def g():
    return glob.Joystick.get_axis(0) > .5


def h():
    return glob.Joystick.get_button(1)


def i():
    return glob.Joystick.get_button(0)


def j():
    return glob.Joystick.get_button(2)


def k():
    return glob.Joystick.get_button(4)


def l():
    return glob.Joystick.get_button(5)


def m():
    return glob.Joystick.get_button(9)

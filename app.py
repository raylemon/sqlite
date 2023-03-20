from controller import TodoControl
from data import TodoStorage
from gui import MainGui

if __name__ == '__main__':
    view = MainGui()
    data = TodoStorage()

    control = TodoControl(view, data)

    view.controller = control

    view.start()

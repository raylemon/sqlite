from data import TodoStorage
from gui import MainGui


class TodoControl:
    def __init__(self, view: MainGui, data: TodoStorage):
        self.view = view
        self.data = data

    # TODO need some code

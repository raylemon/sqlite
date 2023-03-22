from data import TodoStorage, TodoItem
from gui import MainGui


class TodoControl:
    def __init__(self, view: MainGui, data: TodoStorage):
        self.view = view
        self.data = data

    def add_item(self, text:str):
        if text != "":
            item = TodoItem(text)
            item = self.data.add_item(item)
            self.view.insert(item.tid, item.status, item.text)

    def load_items(self):
        items = self.data.load_items()
        for item in items:
            self.view.insert(item.tid, item.status, item.text)

    def delete_item(self, tid:int) -> bool:
        return self.data.delete_item(tid)

    def update_item(self, tid:int) -> bool:
        item = self.data.get_item(tid)
        item = self.data.update_item(item)
        return item.status
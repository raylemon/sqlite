import tkinter as tk
from tkinter import ttk, PhotoImage
from tkinter.messagebox import showerror


class MainGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Todo List")

        # Internal vars
        self._sv_todo = tk.StringVar()
        self._empty_img = PhotoImage(file="empty.png")
        self._fill_img = PhotoImage(file="fill.png")

        top_frame = ttk.Frame(self)
        button_frame = ttk.Frame(self)

        # TODO implement Treeview and scrollbar
        self.tree = None
        scroll = None

        # Buttons
        bt_new = ttk.Button(self, text="New", command=self.do_new)
        bt_mark = ttk.Button(button_frame, text="Mark/Unmark", command=self.do_mark)
        bt_delete = ttk.Button(button_frame, text="Delete", command=self.do_delete)
        bt_quit = ttk.Button(self, text="Exit", command=self.quit)
        entry_todo = ttk.Entry(self, textvariable=self._sv_todo)

        # Placing widgets
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scroll.pack(side=tk.RIGHT, expande=False, fill=tk.Y)

        top_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=1)

        bt_mark.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        bt_delete.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)

        button_frame.pack(expand=True, fill=tk.X, pady=1)
        entry_todo.pack(expand=True, fill=tk.X, pady=1)
        bt_new.pack(expand=True, fill=tk.X, pady=1)
        bt_quit.pack(expand=True, fill=tk.X, pady=1)

    # Optional but useful, virtual event <<treevievSelect>>
    def on_tree_select(self, event):
        """ On tree selection """
        pass

    def insert(self):
        """ Insert item to tree """
        pass

    def do_new(self):
        """ Add item """
        pass

    def do_mark(self):
        """ Mark/unmark item as done """
        pass

    def do_delete(self):
        """ Remove item """
        pass

    def start(self):
        """ Start loop """
        self.mainloop()

    @property
    def controller(self):
        """ Controller """
        try:
            return self._controller
        except AttributeError as aer:
            showerror("Error", "No controller set")

    @controller.setter
    def controller(self, value):
        self._controller = value
        self._controller.load_items()

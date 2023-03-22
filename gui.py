import tkinter as tk
from tkinter import ttk, PhotoImage
from tkinter.messagebox import showerror, showinfo


class MainGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Todo List")

        # Internal vars
        self._sv_todo = tk.StringVar()
        self._empty_img = PhotoImage(file="empty.png")
        self._fill_img = PhotoImage(file="fill.png")

        # Widgets

        top_frame = ttk.Frame(self)
        button_frame = ttk.Frame(self)

        # TODO implement Treeview and scrollbar
        self.tree = ttk.Treeview(top_frame,
                                 columns=("id","text"),
                                 selectmode=tk.BROWSE,
                                 height=10)
        self.tree.column(0,width=10, stretch=False, anchor=tk.CENTER) # image
        self.tree.column("id", width=0, stretch=False, anchor=tk.CENTER) # id
        self.tree.column("text", width=250, stretch=True, anchor=tk.CENTER) # text

        self.tree.heading(0,anchor=tk.CENTER)
        self.tree.heading("text",text="Todo item", anchor=tk.CENTER)

        scroll = ttk.Scrollbar(top_frame,orient=tk.VERTICAL,command=self.tree.yview)
        self.tree["yscrollcommand"] = scroll.set

        # Optional
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Buttons
        bt_new = ttk.Button(self, text="New", command=self.do_new)
        bt_mark = ttk.Button(button_frame, text="Mark/Unmark", command=self.do_mark)
        bt_delete = ttk.Button(button_frame, text="Delete", command=self.do_delete)
        bt_quit = ttk.Button(self, text="Exit", command=self.quit)
        entry_todo = ttk.Entry(self, textvariable=self._sv_todo)

        # Placing widgets
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scroll.pack(side=tk.RIGHT, expand=False, fill=tk.Y)

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
        try:
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                # TREATMENT
                showinfo(title="Todo List",
                         message=f"id = {item['values'][0]} message={item['values'][1]}")
        except IndexError:
            return

    def insert(self, todo_id: int, status:bool, text:str):
        """ Insert item to tree """
        self.tree.insert("", tk.END,
                         image=self._fill_img if status else self._empty_img,
                         values=(todo_id,text))

    def do_new(self):
        """ Add item """
        self.controller.add_item(self._sv_todo.get())

    def do_mark(self):
        """ Mark/unmark item as done """
        selection = self.tree.selection()
        for sel_item in selection:
            item = self.tree.item(sel_item)
            status = self.controller.update_item(item["values"][0])
            self.tree.item(sel_item, image= self._fill_img if status else self._empty_img)


    def do_delete(self):
        """ Remove item """
        selection = self.tree.selection()
        for sel_item in selection:
            item = self.tree.item(sel_item)
            if self.controller.delete_item(item["values"][0]):
                self.tree.delete(sel_item)

    def start(self):
        """ Start loop """
        self.mainloop()

    @property
    def controller(self):
        """ Controller """
        try:
            return self._controller
        except AttributeError:
            showerror("Error", "No controller set")
            self.quit()

    @controller.setter
    def controller(self, value):
        self._controller = value
        self._controller.load_items()

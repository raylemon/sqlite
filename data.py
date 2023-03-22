from dataclasses import dataclass, field
import sqlite3
from contextlib import closing

@dataclass
class TodoItem:
    text: str
    status: bool = field(default=False)
    tid: int = field(default=-1)


class TodoStorage:
    def __init__(self):
        self.database = sqlite3.connect("todos.db")
        self.create_table()

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.database.cursor()

    def commit(self):
        self.database.commit()

    def create_table(self):
        sql = """ CREATE TABLE IF NOT EXISTS T_Items (
            tid INTEGER PRIMARY KEY AUTOINCREMENT ,
            text TEXT NOT NULL ,
            status INTEGER CHECK ( status IN (0,1) ) DEFAULT 0
        )"""

        with closing(self.cursor) as cursor:
            cursor.execute(sql)
            self.commit( )

    def add_item(self, item:TodoItem) -> TodoItem:
        sql = """ INSERT INTO T_Items (text) VALUES ( ? ) """

        with closing(self.cursor) as cursor:
            result = cursor.execute(sql,[item.text])
            item.tid = result.lastrowid
            self.commit()
            return item

    def load_items(self) -> list[TodoItem]:
        sql = """ SELECT * FROM T_Items """

        with closing(self.cursor) as cursor:
            result = cursor.execute(sql)
            result.row_factory = lambda cursor, row: TodoItem(tid=row[0],
                                                              text=row[1],
                                                              status=row[2])

            return result.fetchall()

    def delete_item(self, tid: int) -> bool:
        sql = """ DELETE FROM T_Items WHERE tid = ? """

        with closing(self.cursor) as cursor:
            result = cursor.execute(sql, [tid])
            self.commit()
            return result.rowcount >= 1

    def get_item(self, tid:int) -> TodoItem:
        sql= """ SELECT * FROM T_Items WHERE tid = ? """

        with closing(self.cursor) as cursor:
            result = cursor.execute(sql, [tid])
            result.row_factory = lambda cursor, row: TodoItem(tid=row[0],
                                                              text=row[1],
                                                              status=row[2])

            return result.fetchone()

    def update_item(self, item:TodoItem) -> TodoItem:
        sql = """ UPDATE T_Items SET status = ? WHERE tid = ? """

        with closing(self.cursor) as cursor:
            result = cursor.execute(sql, [not item.status, item.tid])
            if result.rowcount >= 1 :
                item.status = not item.status
            self.commit()
            return item
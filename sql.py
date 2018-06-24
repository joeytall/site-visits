import sqlite3
DB = "data.db"


class SQL(object):
  def __init__(self):
    self._init_db()

  def _init_db(self):
    self.con = sqlite3.connect(DB)
    self.cur = self.con.cursor()

  def _cleanup(self):
    self.con.commit()
    self.con.close()

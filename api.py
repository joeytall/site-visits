import sqlite3
from loader import DB


class API(object):
  def __init__(self):
    self._init_db()
    return

  def _init_db(self):
    self.con = sqlite3.connect(DB)
    self.cur = self.con.cursor()

  def unique(self, os, device):
    start = 'SELECT count(distinct(user)) FROM visit '
    sql, count = self._query(start, os, device)

    return {
      'sql': sql,
      'count': count,
    }

  def loyal(self, os, device):
    start = 'SELECT count(c) FROM (SELECT count(user) as c from visit '
    end = ' group by user) where c >= 10;'
    sql, count = self._query(start, os, device, end)

    return {
      'sql': sql,
      'count': count,
    }

  def _query(self, start, os, device, end = ';'):
    sql = self._gen_sql(start, os, device, end)
    self.cur.execute(sql)
    count = self.cur.fetchone()[0]
    self._cleanup()
    return sql, count

  def _gen_sql(self, start, os, device, end):
    sql = start
    if os:
      sql += 'WHERE os in (' + os + ') '
    if device:
      sql += 'AND ' if os else 'WHERE '
      sql += 'device in (' + device + ')'
    sql += end

    return sql

  def _cleanup(self):
    self.con.commit()
    self.con.close()

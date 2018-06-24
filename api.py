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
    start = 'SELECT count(*) FROM visit '
    sql, count = self._query(start, os, device)

    return {
      # 'sql': sql,
      'count': count,
    }

  def loyal(self, os, device):
    start = 'SELECT count(*) FROM visit'
    end = 'count >= 10;'
    sql, count = self._query(start, os, device, end)

    return {
      # 'sql': sql,
      'count': count,
    }

  def _query(self, start, os, device, end = ';'):
    sql = self._gen_sql(start, os, device, end)
    try:
      self.cur.execute(sql)
    except:
      print (sql)
    count = self.cur.fetchone()[0]
    self._cleanup()
    return sql, count

  def _gen_sql(self, start, os, device, end):
    sql = start
    os = self._to_bits(os)
    device = self._to_bits(device)

    if int(os) > 0:
      sql += ' WHERE os & ' + os + ' > 0 '
      if int(device) > 0:
        sql += ' AND device & ' + device + ' > 0 '
    elif int(device) > 0:
      sql += ' WHERE device & ' + device + ' > 0 '

    if end != ';':
      sql += ' AND ' if 'WHERE' in sql else ' WHERE '
    sql += end

    return sql

  def _to_bits(self, items):
    bits = 0
    if items:
      for i in items.split(','):
        bits |= 2 ** int(i)
    return str(bits)

  def _cleanup(self):
    self.con.commit()
    self.con.close()

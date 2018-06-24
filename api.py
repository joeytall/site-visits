from sql import SQL


class API(SQL):
  def unique(self, os, device):
    start = 'SELECT count(*) FROM visit '
    sql, count = self._query(start, os, device)

    return {
      'count': count,
    }

  def loyal(self, os, device):
    start = 'SELECT count(*) FROM visit'
    end = 'count >= 10;'
    sql, count = self._query(start, os, device, end)

    return {
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

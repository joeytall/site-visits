import os, csv, time
from sql import SQL, DB


class Loader(SQL):
  def __init__(self):
    st = time.time()
    if os.path.exists(DB):
      return

    self.users = {}
    self._load_csv()
    self._init_db()
    self._gen_table()
    self._dump_db()
    self._cleanup()

    print("--- Total: %s seconds ---" % (int(time.time() - st)))

  def _load_csv(self):
    print ("--- Start Loading CSV --- ")
    st = time.time()
    with open('data/xab','rt') as f:
      count = 0
      dr = csv.reader(f)
      table = []
      for r in dr:
        count += 1
        if count % 1000000 == 0:
          print (str(count // 1000000) + ' million rows read')
        try:
          self._init_user(r)
        except:
          print (r)

    print("--- CSV loading: %s seconds ---" % (int(time.time() - st)))

  def _init_user(self, r):
    user = int(r[1])
    os = self._to_bits(int(r[2]))
    device = self._to_bits(int(r[3]))
    if user in self.users:
      self.users[user]['count'] += 1
      self.users[user]['os'] |= os
      self.users[user]['device'] |= device
    else:
      self.users[user] = {
        'count': 1,
        'os': os,
        'device': device,
      }

  def _to_bits(self, item):
    return 2 ** item

  def _gen_table(self):
    print("--- Start Analysing ---")
    st = time.time()
    self.table = [(u, v['os'], v['device'], v['count']) for u, v in self.users.items()]
    print("--- Analysing: %s seconds ---" % (int(time.time() - st)))

  def _dump_db(self):
    print("--- Start Dumping DB ---")
    st = time.time()
    self.cur.execute("CREATE TABLE visit (user, os, device, count);")
    self.cur.executemany("INSERT INTO visit (user, os, device, count) VALUES (?, ?, ?, ?);", self.table)
    print("--- DB Dumping: %s seconds ---" % (int(time.time() - st)))

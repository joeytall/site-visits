import os, csv, sqlite3, time


start_time = time.time()
DB = "data.db"
OS_BITS = 7


class Loader(object):
  def __init__(self):
    if os.path.exists(DB):
      print ("DB exists.")
      return

    self.users = {}
    self._load_csv()
    self._init_db()
    self._analysis()
    self._dump_db()
    self._cleanup()

    print("--- Total: %s seconds ---" % (int(time.time() - start_time)))

  def _init_db(self):
    self.con = sqlite3.connect(DB)
    self.cur = self.con.cursor()
    self.cur.execute("CREATE TABLE visit (user, os, device, count);")

  def _load_csv(self):
    print ("--- Start Loading CSV --- ")
    with open('data.csv','rt') as f:
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

    print("--- CSV loading: %s seconds ---" % (int(time.time() - start_time)))

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

  def _analysis(self):
    print("--- Start Analysing ---")
    st = time.time()
    self.table = [(u, v['os'], v['device'], v['count']) for u, v in self.users.items()]
    print("--- Analysing: %s seconds ---" % (int(time.time() - st)))

  def _dump_db(self):
    print("--- Start Dumping DB ---")
    st = time.time()
    self.cur.executemany("INSERT INTO visit (user, os, device, count) VALUES (?, ?, ?, ?);", self.table)
    print("--- DB Dumping: %s seconds ---" % (int(time.time() - st)))

  def _cleanup(self):
    self.con.commit()
    self.con.close()


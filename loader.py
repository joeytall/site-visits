import os, csv, sqlite3, time


start_time = time.time()
DB = "data.db"


class Loader(object):
  def __init__(self):
    if os.path.exists(DB):
      print ("DB exists.")
      return

    self._load_csv()
    self._init_db()
    self._dump_db()
    self._cleanup()

    print("--- Total: %s seconds ---" % (int(time.time() - start_time)))

  def _init_db(self):
    self.con = sqlite3.connect(DB)
    self.cur = self.con.cursor()
    self.cur.execute("CREATE TABLE visit (user, os, device);")

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
          table.append((int(r[1]), int(r[2]), int(r[3])))
        except:
          print (r)

    self.table = table
    print("--- CSV loading: %s seconds ---" % (int(time.time() - start_time)))

  def _dump_db(self):
    print("--- Start Dumping DB ---")
    db_st = time.time()
    self.cur.executemany("INSERT INTO visit (user, os, device) VALUES (?, ?, ?);", self.table)
    print("--- DB Dumping: %s seconds ---" % (int(time.time() - db_st)))

  def _cleanup(self):
    self.con.commit()
    self.con.close()


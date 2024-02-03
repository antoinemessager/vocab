import pymysql

timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="vocable-vocable.a.aivencloud.com",
  password="AVNS_PuVJXwhe3IbdGZFJG_k",
  read_timeout=timeout,
  port=27109,
  user="avnadmin",
  write_timeout=timeout,
)
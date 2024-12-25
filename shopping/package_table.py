import sqlite3

def create_db():
  conn = sqlite3.connect('shopping.db')
  c = conn.cursor()

  # Create Goods table
  c.execute('''CREATE TABLE IF NOT EXISTS Goods(
      good_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name VARCHAR(128) NOT NULL,
      price INTEGER NOT NULL,
      img TEXT NOT NULL,
      description TEXT)''')

  # Create Package table
  c.execute('''CREATE TABLE IF NOT EXISTS Packages(
      package_id VARCHAR(128),
      status_id INTEGER,
      status_time DATETIME DEFAULT (datetime('now', 'localtime')),
      FOREIGN KEY (status_id) REFERENCES Status(status_id)
  )''')

  # FOR status
  c.execute('''CREATE TABLE IF NOT EXISTS Status(
      status_id INTEGER PRIMARY KEY AUTOINCREMENT,
      status VARCHAR(64) NOT NULL,
      place VARCHAR(128) NOT NULL
  )''')


  conn.commit()
  conn.close()

create_db()

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
      package_id INTEGER PRIMARY KEY AUTOINCREMENT,
      place VARCHAR(128),
      -- place VARCHAR(128) NOT NULL,
      -- status VARCHAR(64) NOT NULL,
      -- status_time DATETIME DEFAULT (datetime('now', 'localtime')),
      good_id INTEGER,
      FOREIGN KEY (good_id) REFERENCES Goods(good_id)
  )''')

  # FOR status
  c.execute('''CREATE TABLE IF NOT EXISTS Status(
      status_id INTEGER PRIMARY KEY AUTOINCREMENT,
      status VARCHAR(64) NOT NULL,
      status_time DATETIME DEFAULT (datetime('now', 'localtime')),
      package_id INTEGER NOT NULL,
      FOREIGN KEY (package_id) REFERENCES Packages(package_id)
  )''')


  conn.commit()
  conn.close()
create_db()

import sqlite3

def create_db():
  conn = sqlite3.connect('shopping.db')
  c = conn.cursor()
  
  # Create Goods table
  c.execute('''CREATE TABLE IF NOT EXISTS Goods(
      id INTEGER PRIMARY KEY AUTOINCREMENT, 
      name VARCHAR(128) NOT NULL,
      price INTEGER NOT NULL,
      description TEXT)''')
  
  # Create Package table
  c.execute('''CREATE TABLE IF NOT EXISTS Packages(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      place VARCHAR(128) NOT NULL,
      status_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- Use DEFAULT for status_time
      status VARCHAR(64) NOT NULL,
      goods_id INTEGER REFERENCES Goods(id))''') # Reference Goods table
      
  conn.commit()
  conn.close()


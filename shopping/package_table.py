
def create_db():
  conn = sqlite3.connect('shopping.db')
  c = conn.cursor()
  
  # Create Goods table
  c.execute('''CREATE TABLE IF NOT EXISTS Goods(
      id VARCHAR(32) PRIMARY KEY, 
      name VARCHAR(128) NOT NULL,
      price INTEGER NOT NULL,
      description TEXT)''')
  
  # Create Package table
  c.execute('''CREATE TABLE IF NOT EXISTS Packages(
      id VARCHAR(32) PRIMARY KEY,
      place VARCHAR(128) NOT NULL,
      status VARCHAR(64) NOT NULL,
      status_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- Use DEFAULT for status_time)''')
  conn.commit()
  conn.close()

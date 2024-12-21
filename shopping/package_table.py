# schema for goods
import sqlite3

def create_db():
  conn = sqlite3.connect('shopping.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE Goods(
      id SERIAL PRIMARY KEY,
      name VARCHAR(128),
      price INTEGER),
      description TEXT)

  #schema for package
  CREATE TABLE Package(
      id SERIAL PRIMARY KEY,
      place VARCHAR(128),
      status_time DATETIME,
      status VARCHAR(64),
      goods_id INTEGER REFERENCES shopping(id))'''
  )
  conn.commit()
  conn.close()

def insert_status(status, package_id):
  c = connect_db()
  package_data = [
    ("Delivered", "Customer Address, Los Angeles", "2023-05-14 10:15"),
    ("Out for Delivery", "Local Courier, Los Angeles", "2023-05-14 08:30"),
    ("In Transit", "Distribution Center, San Francisco", "2023-05-13 20:00"),
    ("Processing", "LSA Shop", " ")
  ]

  for status, place, time in package_data:
    c.execute("INSERT INTO Status (status, place) VALUES (?, ?)", (status, place))


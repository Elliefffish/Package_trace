import sqlite3

def insert_goods():
    conn = sqlite3.connect('shopping.db')
    cursor = conn.cursor()

    print("Insert Packages:\n")

    while True:

        place = input("(If enter 'exit', then over)place: ").strip()
        if place == "exit":
            break

        status = input("status: ").strip()


        try:
            cursor.execute(
                "INSERT INTO Goods (place, status) VALUES (?, ?)",
                (place, status)
            )
            conn.commit()
            print(f"'{place}' Success insert！\n")
        except Exception as e:
            print(f"error：{e}\n")

    conn.close()
    print("End")

if __place__ == "__main__":
    insert_goods()

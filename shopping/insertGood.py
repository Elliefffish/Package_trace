import sqlite3

def insert_goods():
    conn = sqlite3.connect('shopping.db')
    cursor = conn.cursor()
    
    print("Insert goods:\n")

    while True:
        
        name = input("(If enter 'exit', then over)name: ").strip()
        if name == "exit":
            break

        price = input("price: ").strip()
        
        # folder : good_img
        img = "./good_img/"
        img += input("img(./good_img): ").strip()

        
        description = input("description: ").strip()
        
        try:
            cursor.execute(
                "INSERT INTO Goods (name, price, img, description) VALUES (?, ?, ?, ?)",
                (name, float(price), img, description)
            )
            conn.commit()
            print(f"'{name}' Success insert！\n")
        except Exception as e:
            print(f"error：{e}\n")
    
    conn.close()
    print("End")

if __name__ == "__main__":
    insert_goods()


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
from datetime import datetime
import uvicorn
from update_status import update_package_periodically 
import threading

# 初始化 FastAPI 應用
app = FastAPI()

# model
class Package(BaseModel):
    # 訂單編號
    package_id: Optional[str] = None
    # 取貨門市
    #place: str
    # 狀態
    status_id: Optional[int] = None
    # 狀態時間
    status_time: Optional[datetime] = None

    #good_id: Optional[int] = None
    #good_name: Optional[str] = None

class Good(BaseModel):
    # 商品編號
    good_id: Optional[int] = None
    # 商品名稱
    name: str
    # 價格
    price: int
    # 圖片
    img: str
    # 介紹
    description: str

class Status(BaseModel):
    #status_id: Optional[int] = None
    status_id: int
    status: str
    #status_time: Optional[datetime] = None
    place: str
    # package_id: int

class PackageStatus(BaseModel):
    package_id: str
    place: Optional[str] = None
    status: Optional[str] = None
    status_time: Optional[datetime] = None

# connect sqlite
def get_db_connection():
    connection = sqlite3.connect("shopping.db")
    connection.row_factory = sqlite3.Row
    return connection

# Post packages 測試: insert 包裹資料
'''
{
    "package_id": 1234,
    "status_id": 1 
}
'''
@app.post("/packages", response_model=Package)
def create_package(package: Package):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            # first column : id -> auto
            "INSERT INTO Packages (package_id, status_id) VALUES (?, ?)",
            (package.package_id, package.status_id)
        )
        connection.commit()
        thread = threading.Thread(target=update_package_periodically, args=(package.package_id, 1))
        thread.start()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Order ID already exists.")
    finally:
        connection.close()
    return package

'''
{
    "status": "送達",
    "package_id": "1"
}
'''
@app.post("/status", response_model=Status)
def update_status(status: Status):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        # check
        cursor.execute("SELECT 1 FROM Packages WHERE package_id = ?", (status.package_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Package ID not found.")
        # insert new status
        cursor.execute(
            "INSERT INTO Status (status, package_id) VALUES (?, ?)",(status.status,status.package_id))
        
        connection.commit()
    except sqlite3.IntegrityError as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail="Failed to update status.") from e
    finally:
        connection.close()
    return status
'''
{
    "package_id:"
    "place":
    "status":
    "status_time"
}
'''
# Get packages search
@app.get("/packages/{package_id}", response_model=PackageStatus)
def get_package(package_id: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    package = cursor.execute('''
        SELECT p.package_id, s.place AS place, s.status AS status, p.status_time
        FROM Packages p
        LEFT JOIN Status s ON p.status_id = s.status_id
        WHERE p.package_id = ?
        ORDER BY p.status_time DESC
        LIMIT 1
    ''', (package_id,)).fetchone()

    if package is None:
        raise HTTPException(status_code=404, detail="Package not found.")
    
    package_dict = {
        "package_id": package[0],
        "place": package[1],
        "status": package[2],
        "status_time": package[3]
    }

    connection.close()

    return package_dict


# search all packages
@app.get("/packages", response_model=List[Package])
def list_packages():
    connection = get_db_connection()
    cursor = connection.cursor()
    packages = cursor.execute('''
        SELECT p.package_id, p.place, p.good_id, g.name AS good_name
        FROM Packages p
        LEFT JOIN Goods g ON p.good_id = g.good_id
    ''').fetchall()

    #for package in packages:
    #    print(dict(package))
    package_list = []
    for package in packages:
        package_dict = {
            "package_id": package[0],
            "place": package[1],
            "good_id": package[2],
            "good_name": package[3]
        }

        statuses = cursor.execute('''
            SELECT status, status_time
            FROM Status
            WHERE package_id = ?
            ORDER BY status_time DESC
        ''', (package[0],)).fetchall()
        '''
        if statuses:  
            package_dict["status"] = statuses[0]
            package_dict["status_time"] = statuses[1]
        else:  
            package_dict["status"] = None
            package_dict["status_time"] = None
        '''       
        
        if statuses:
            package_dict["statuses"] = [{"status": status[0], "status_time": status[1]} for status in statuses]
        else:
            package_dict["statuses"] = []
        
        package_list.append(package_dict)

    connection.close()

    return package_list
"""
@app.get("/packages", response_model=List[Package])

def list_packages():
    connection = get_db_connection()
    cursor = connection.cursor()

    packages = cursor.execute('''
        SELECT p.package_id, p.place, p.good_id, g.name AS good_name, s.status AS status, s.status_time AS status_time
        FROM Packages p
        LEFT JOIN Goods g ON p.good_id = g.good_id,
        LEFT JOIN Status s ON s.package_id = p.package_id
    ''').fetchall()

    package_list = []
    for package in packages:
        package_dict = {
            "package_id": package[0],
            "place": package[1],
            "good_id": package[2],
            "good_name": package[3],
            "status": package[4],
            "status_time": package[5]
        }
        
        statuses = cursor.execute('''
            SELECT status, status_time
            FROM Status
            WHERE package_id = ?
            ORDER BY status_time DESC
        ''', (package[0],)).fetchall()
         

        package_list.append(package_dict)

    connection.close()

    return package_list
"""
# Post goods 測試: insert 商品資料
@app.post("/goods", response_model=Good)
def create_good(good: Good):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Goods (name, price, img, description) VALUES (?, ?, ?, ?)",
            (good.name, good.price, good.img, good.description)
        )
        connection.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Good ID already exists.")
    finally:
        connection.close()
    return good


# Get good
@app.get("/goods/{good_id}", response_model=Good)
def get_good(good_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    good = cursor.execute(
        "SELECT good_id, name, price, img, description FROM Goods WHERE good_id = ?",
        (good_id,)
    ).fetchone()
    connection.close()
    if good is None:
        raise HTTPException(status_code=404, detail="Good not found.")
    return {
        "good_id": good["good_id"],
        "name": good["name"],
        "price": good["price"],
        "img": good["img"],
        "description": good["description"],
    }

# Get all goods
@app.get("/goods", response_model=List[Good])
def list_goods():
    connection = get_db_connection()
    cursor = connection.cursor()
    goods = cursor.execute(
        "SELECT good_id, name, price, img, description FROM Goods"
    ).fetchall()
    connection.close()
    return [
        {
            "good_id": good["good_id"],
            "name": good["name"],
            "price": good["price"],
            "img": good["img"],
            "description": good["description"],
        }
        for good in goods
    ]


if __name__ == '__main__':
    uvicorn.run(app='api:app', host='127.0.0.1', port=8000, reload=True)

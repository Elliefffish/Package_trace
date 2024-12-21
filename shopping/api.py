from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional
from datetime import datetime
import uvicorn

# 初始化 FastAPI 應用
app = FastAPI()

# model
class Package(BaseModel):
    # 訂單編號
    id: str
    # 取貨門市
    place: str
    # 狀態
    status: str
    # 狀態時間
    status_time: Optional[datetime] = None

class Good(BaseModel):
    # 商品編號
    id: str
    # 商品名稱
    name: str
    # 價格
    price: int
    # 圖片
    img: str
    # 介紹
    description: str


# connect sqlite
def get_db_connection():
    connection = sqlite3.connect("shopping.db")
    connection.row_factory = sqlite3.Row
    return connection

# Post packages 測試: insert 包裹資料
@app.post("/packages", response_model=Package)
def create_package(package: Package):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            # first column : id -> auto
            "INSERT INTO Packages (id, place, status) VALUES (?, ?, ?)",
            (package.id, package.place, package.status)
        )
        connection.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Order ID already exists.")
    finally:
        connection.close()
    return package


# Get pakages search 
@app.get("/packages/{id}", response_model=Package)
def get_package(id: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    package = cursor.execute(
        "SELECT id, place, status, status_time FROM Packages WHERE id = ?",
        (id,),
    ).fetchone()
    connection.close()
    if package is None:
        raise HTTPException(status_code=404, detail="Package not found.")
    return {
        "id": package["id"],
        "place": package["place"],
        "status": package["status"],
        "status_time": package["status_time"],
    }


# search all
@app.get("/packages", response_model=List[Package])
def list_packages():
    connection = get_db_connection()
    cursor = connection.cursor()
    packages = cursor.execute(
        "SELECT id, place, status, status_time FROM Packages"
    ).fetchall()
    connection.close()
    return [
        {
            "id": package["id"],
            "place": package["place"],
            "status": package["status"],
            "status_time": package["status_time"],
        }
        for package in packages
    ]

# Post packages 測試: insert 包裹資料
@app.post("/goods", response_model=Good)
def create_good(good: Good):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            # first column : id -> auto
            "INSERT INTO Goods (id, name, price, img, description) VALUES (?, ?, ?, ?, ?)",
            (good.id, good.name, good.price, good.img, good.description)
        )
        connection.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Good ID already exists.")
    finally:
        connection.close()
    return good


# Get goods
@app.get("/goods/{id}", response_model=Good)
def get_good(id: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    good = cursor.execute(
        "SELECT id, name, price, img, description FROM Goods WHERE id = ?",
        (id,),
    ).fetchone()
    connection.close()
    if good is None:
        raise HTTPException(status_code=404, detail="Good not found.")
    return {
        "id": good["id"],
        "name": good["name"],
        "price": good["price"],
        "img": good["img"],
        "description": good["description"],
    }

# Get all goods
@app.get("/goods", response_model=List[Good])
def list_good():
    connection = get_db_connection()
    cursor = connection.cursor()
    goods = cursor.execute(
        "SELECT id, name, price, img, description FROM Goods"
    ).fetchall()
    connection.close()
    return [
        {
            "id": good["id"],
            "name": good["name"],
            "price": good["price"],
            "img": good["img"],
            "description": good["description"],
        }
        for good in goods
    ]



if __name__ == '__main__':
    uvicorn.run(app='api:app', host='127.0.0.1', port=8000, reload=True)

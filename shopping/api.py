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

# connect sqlite
def get_db_connection():
    connection = sqlite3.connect("shopping.db")
    connection.row_factory = sqlite3.Row
    return connection

# 測試: insert 包裹資料
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


# search 
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

if __name__ == '__main__':
    uvicorn.run(app='api:app', host='127.0.0.1', port=8000, reload=True)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
import os

app = FastAPI(title="Todo List API")

# MongoDB连接配置
MONGODB_URL = "mongodb+srv://huguao777:5kuRgTIaPZlLGKBi@clustertodolist.xhwhgkb.mongodb.net/"
DATABASE_NAME = "todolist"
COLLECTION_NAME = "todos"

# MongoDB客户端
client = None
db = None

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://localhost:5174"],  # React开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class TodoItem(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    description: Optional[str] = ""
    completed: bool = False
    created_at: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "完成项目文档",
                "description": "编写详细的项目说明文档",
                "completed": False
            }
        }

# MongoDB连接初始化
async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    print("Connected to MongoDB!")

async def close_mongo_connection():
    if client:
        client.close()
        print("MongoDB connection closed!")

# 启动和关闭事件
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# API路由
@app.get("/")
def read_root():
    return {"message": "Todo List API with MongoDB"}

@app.get("/todos", response_model=List[TodoItem])
async def get_todos():
    try:
        todos_collection = db[COLLECTION_NAME]
        cursor = todos_collection.find().sort("created_at", -1)
        todos = []
        async for document in cursor:
            document["_id"] = str(document["_id"])
            todos.append(TodoItem(**document))
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    try:
        todos_collection = db[COLLECTION_NAME]
        todo_dict = todo.dict(exclude={"id"})
        todo_dict["created_at"] = datetime.now().isoformat()
        
        result = await todos_collection.insert_one(todo_dict)
        todo_dict["_id"] = str(result.inserted_id)
        
        return TodoItem(**todo_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: str, todo: TodoItem):
    try:
        todos_collection = db[COLLECTION_NAME]
        
        # 验证ObjectId格式
        if not ObjectId.is_valid(todo_id):
            raise HTTPException(status_code=400, detail="Invalid todo ID format")
        
        # 检查待办事项是否存在
        existing_todo = await todos_collection.find_one({"_id": ObjectId(todo_id)})
        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # 更新待办事项
        update_data = todo.dict(exclude={"id"})
        await todos_collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": update_data}
        )
        
        # 返回更新后的数据
        updated_todo = await todos_collection.find_one({"_id": ObjectId(todo_id)})
        updated_todo["_id"] = str(updated_todo["_id"])
        
        return TodoItem(**updated_todo)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    try:
        todos_collection = db[COLLECTION_NAME]
        
        # 验证ObjectId格式
        if not ObjectId.is_valid(todo_id):
            raise HTTPException(status_code=400, detail="Invalid todo ID format")
        
        # 检查待办事项是否存在
        existing_todo = await todos_collection.find_one({"_id": ObjectId(todo_id)})
        if not existing_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # 删除待办事项
        await todos_collection.delete_one({"_id": ObjectId(todo_id)})
        
        return {"message": "Todo deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime

app = FastAPI(title="Todo List API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    completed: bool = False
    created_at: Optional[str] = None

# 数据库初始化
def init_db():
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# API路由
@app.get("/")
def read_root():
    return {"message": "Todo List API"}

@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos ORDER BY created_at DESC')
    todos = cursor.fetchall()
    conn.close()
    
    return [
        TodoItem(
            id=todo[0],
            title=todo[1],
            description=todo[2],
            completed=bool(todo[3]),
            created_at=todo[4]
        )
        for todo in todos
    ]

@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoItem):
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)',
        (todo.title, todo.description, todo.completed)
    )
    conn.commit()
    todo_id = cursor.lastrowid
    conn.close()
    
    return TodoItem(
        id=todo_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=datetime.now().isoformat()
    )

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, todo: TodoItem):
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE todos SET title = ?, description = ?, completed = ? WHERE id = ?',
        (todo.title, todo.description, todo.completed, todo_id)
    )
    conn.commit()
    conn.close()
    
    return TodoItem(
        id=todo_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = sqlite3.connect('todos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    
    return {"message": "Todo deleted successfully"}

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

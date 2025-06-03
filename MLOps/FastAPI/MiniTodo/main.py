from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import IntEnum
import uvicorn
api = FastAPI()


class Priority(IntEnum):
    low = 1
    medium = 2
    high = 3

class TodoBase(BaseModel):
    description: str = Field(..., min_length=3, max_length=100, description="The description of the todo")
    priority: Priority = Field(default=Priority.low, description="The priority of the todo")

class Todo(TodoBase):
    index: int = Field(..., description="The index of the todo")

class TodoUpdate(TodoBase):
    description: Optional[str] = Field(None, min_length=3, max_length=100, description="The description of the todo")
    priority: Optional[Priority] = Field(None, description="The priority of the todo")


todo_list = [
    Todo(index = 1, description="Do the homework", priority=Priority.medium),
    Todo(index = 2, description="Do the dishes", priority=Priority.medium),
    Todo(index = 3, description="Do the laundry", priority=Priority.high),
    Todo(index= 4,description="Do the groceries", priority=Priority.low)
]

@api.get("/todos", response_model=List[Todo])
def get_todos():
    return todo_list

@api.get("/todos/{index}", response_model=Todo)
def get_todo(index: int):
    if index < 0 or index >= len(todo_list):
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_list[index]

@api.post("/todos", response_model=List[Todo])
def add_todo(todo : TodoBase):
    todo_list.append(Todo(
                          index= len(todo_list), 
                          description=todo.description, 
                          priority=todo.priority))
    return todo_list[-1]

@api.put("/todos/{index}", response_model=List[Todo])
def update_todo(todo : TodoUpdate, index: int):
    if index < 0 or index >= len(todo_list):
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_list[index] = Todo(
        index=index,
        description=todo.description,
        priority=todo.priority
    )
    return todo_list[index]

@api.delete("/todos/{index}")
def delete_todo(index: int):
    if index < 0 or index >= len(todo_list):
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_list.pop(index)
    return todo_list

if __name__ == "__main__":
    uvicorn.run("main:api", host="127.0.0.1", port=8000, reload=True)
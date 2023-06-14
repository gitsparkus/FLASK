"""
Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. Для каждой
задачи должна быть возможность указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку
Pydantic.
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


class Task(BaseModel):
    id: int
    name: str
    details: str
    done: bool


tasks = []

for i in range(5):
    b = Task(id=i, name=f'task{i}', details=f'details for task{i}', done=False)
    tasks.append(b)

app = FastAPI()


@app.get('/tasks/', response_model=List[Task])
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')


@app.post("/tasks/", response_model=Task)
def new_task(task: Task):
    new_id = max((task.id for task in tasks)) + 1
    task.id = new_id
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def edit_task(task_id: int, data: Task):
    for n, task in enumerate(tasks):
        if task.id == task_id:
            data.id = task_id
            tasks[n] = data
            return tasks[n]
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')


@app.delete('/tasks/{task_id}', response_model=Task)
def delete_task(task_id: int):
    for n, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(n)
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

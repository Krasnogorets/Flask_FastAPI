import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from typing import Optional
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="hw5/templates")
tasks = []


class Task(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str] = None
    status: Optional[bool] = False


@app.get("/", response_class=HTMLResponse)
async def index():
    return "<h1>Список задач</h1>"


@app.get("/tasks/", response_class=HTMLResponse)
async def get_all_tasks(request: Request):
    if tasks:
        task_table = pd.DataFrame([vars(task) for task in tasks])
        task_table['status'] = np.where(task_table.status, "выполнено", "не выполнено")
        task_table.set_index('id', inplace=True)
    else:
        task_table = pd.DataFrame(columns=['id', 'title', 'description', 'status'])
        task_table.set_index('id', inplace=True)
    return templates.TemplateResponse("tasks.html",
                                      {'request': request, 'table': task_table.to_html(col_space='150px')})


@app.get('/tasks/{task_id}', response_model=Task)
async def get_task_by_id(task_id: int, request: Request):
    for task in tasks:
        if task_id == task.id:
            task_table = pd.DataFrame([vars(task)])
            task_table.set_index('id', inplace=True)
            task_table['status'] = np.where(task_table.status, "выполнено", "не выполнено")
            return templates.TemplateResponse("tasks.html",
                                              {'request': request,
                                               'table': task_table.to_html(col_space='150px')})
    return templates.TemplateResponse("not_found.html",
                                              {'request': request, 'task_id':task_id})


@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task.id = len(tasks) + 1
    task.title = f"task{task.id}"
    task.description = f"smth to do_{task.id}"
    tasks.append(task)
    return task


@app.put('/tasks/{task_id}', response_model=Task)
async def update_data(task_id: int, task: Task):
    for old_task in tasks:
        if task_id == old_task.id:
            if task.title != "string":
                old_task.title = task.title
            if task.description != "string":
                old_task.description = task.description
            if task.status:
                old_task.status = task.status
            return task


@app.get('/tasks/{task_id}', response_class=HTMLResponse)
@app.delete('/tasks/{task_id}', response_class=HTMLResponse)
async def delete_data(task_id: int, request: Request):
    for i, cur_task in enumerate(tasks):
        if task_id == cur_task.id:
            return templates.TemplateResponse("del.html",
                                              {'request': request,
                                               'user': pd.DataFrame([vars(tasks.pop(i))]).to_html()})

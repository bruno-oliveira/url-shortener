import os
from datetime import datetime as dt
from urllib import request

from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from uvicorn import run
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


import db_loader
from model.url import Url

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request : Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": id})


@app.get("/hello/{name}")
async def say_hello(name: str):
    print("aaaaa")
    return JSONResponse(content={"message": f"Hello, {name}"})


@app.post("/short")
async def say_hello2(request: Request, long_url: str = Form(...)):
    x = Url(url=long_url, hash_key=os.urandom(10).hex(), created_at=None)
    while True:
        try:
            print("Inserting... with hash ", x.hash_key)
            db_loader.c.execute("INSERT INTO url_mapping VALUES (?,?,?)", (x.hash_key, x.url, dt.now().timestamp()))
            db_loader.conn.commit()
            break
        except Exception as e:
            print(e)
            x.hash_key = os.urandom(10).hex()
    short_url = "https://small-meadow-3457.fly.dev/"+x.hash_key  # Placeholder
    return templates.TemplateResponse("index.html", {"request": request, "short_url": short_url})


@app.get("/{hash_key}")
async def redirect(hash_key: str):
    url = db_loader.c.execute("select url from url_mapping where hash_key=(?)", (hash_key,))
    redirect_result = url.fetchone()
    if redirect_result is not None:
        return RedirectResponse(url=redirect_result[0], status_code=308)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080)

import os
from datetime import datetime as dt
from urllib import request

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from uvicorn import run

import db_loader
from model.url import Url

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    print("aaaaa")
    return JSONResponse(content={"message": f"Hello, {name}"})


@app.post("/short")
async def say_hello2(url: Url):
    while True:
        try:
            print("Inserting... with hash ", url.hash_key)
            db_loader.c.execute("INSERT INTO url_mapping VALUES (?,?,?)", (url.hash_key, url.url, dt.now().timestamp()))
            db_loader.conn.commit()
            break
        except Exception as e:
            print(e)
            url.hash_key = os.urandom(10).hex()
    return {"message": f"Hello, {url.hash_key}"}


@app.get("/{hash_key}")
async def redirect(hash_key: str):
    url = db_loader.c.execute("select url from url_mapping where hash_key=(?)", (hash_key,))
    redirect_result = url.fetchone()
    print(redirect_result[0])
    return RedirectResponse(url=redirect_result[0], status_code=308)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080)

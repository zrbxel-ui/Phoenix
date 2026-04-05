from fastapi import FastAPI, UploadFile, Form
import sqlite3
import os
from datetime import datetime

app = FastAPI()

conn = sqlite3.connect("app.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
    email TEXT,
    password TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS videos (
    filename TEXT,
    user TEXT,
    script TEXT
)""")

conn.commit()

# -------------------------------
# Register
# -------------------------------
@app.post("/register")
def register(email: str = Form(...), password: str = Form(...)):
    c.execute("INSERT INTO users VALUES (?, ?)", (email, password))
    conn.commit()
    return {"msg": "ok"}

# -------------------------------
# Login
# -------------------------------
@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    if c.fetchone():
        return {"msg": "ok"}
    return {"msg": "fail"}

# -------------------------------
# Upload
# -------------------------------
@app.post("/upload")
def upload(file: UploadFile, script: str = Form(...), email: str = Form(...)):
    os.makedirs("videos", exist_ok=True)
    path = f"videos/{{file.filename}}"

    with open(path, "wb") as f:
        f.write(file.file.read())

    c.execute("INSERT INTO videos VALUES (?, ?, ?)", (path, email, script))
    conn.commit()

    return {"msg": "uploaded", "file": path}

# -------------------------------
# Feed
# -------------------------------
@app.get("/videos")
def get_videos():
    c.execute("SELECT filename FROM videos")
    return {"videos": [v[0] for v in c.fetchall()]}

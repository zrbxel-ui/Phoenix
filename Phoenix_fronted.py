import gradio as gr
import requests

API = "https://phoenix-puas.onrender.com"

current_user = {"email": None}

# -------------------------------
# Login
# -------------------------------
def login(email, password):
    r = requests.post(f"{API}/login", data={"email": email, "password": password})
    if r.json()["msg"] == "ok":
        current_user["email"] = email
        return "Eingeloggt"
    return "Fehler"

def register(email, password):
    requests.post(f"{API}/register", data={"email": email, "password": password})
    return "Registriert"

# -------------------------------
# Upload
# -------------------------------
def upload(file, script):
    if not current_user["email"]:
        return "Login nötig", None

    files = {"file": open(file.name, "rb")}
    data = {"script": script, "email": current_user["email"]}

    r = requests.post(f"{API}/upload", files=files, data=data)
    return "Uploaded", r.json()["file"]

# -------------------------------
# Feed
# -------------------------------
def load():
    r = requests.get(f"{API}/videos")
    return r.json()["videos"]

# -------------------------------
# UI
# -------------------------------
with gr.Blocks() as app:

    gr.Markdown("# 🚀 ULTRA KI APP")

    with gr.Tab("Login"):
        email = gr.Textbox()
        pw = gr.Textbox(type="password")
        out = gr.Textbox()

        gr.Button("Login").click(login, [email, pw], out)
        gr.Button("Register").click(register, [email, pw], out)

    with gr.Tab("Upload"):
        script = gr.Textbox()
        file = gr.File()
        out = gr.Textbox()
        vid = gr.Video()

        gr.Button("Upload").click(upload, [file, script], [out, vid])

    with gr.Tab("Feed"):
        gal = gr.Gallery()
        gr.Button("Load").click(load, outputs=gal)

app.launch()

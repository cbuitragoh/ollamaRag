from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from src.helpers import respond_to_message
from fastapi.middleware.cors import CORSMiddleware
from src.logger import create_logger
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = create_logger("app_logger")
app.mount("/static", StaticFiles(directory="static"), name="static")
logger.info("Static files mounted")
templates = Jinja2Templates(directory="templates")
logger.info("Templates loaded")


upload_dir = "./uploads"
os.makedirs(upload_dir, exist_ok=True)

class Message(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    for file in files:
        file_location = os.path.join(upload_dir, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())
            
    return JSONResponse(content={"message": "Files successfully uploaded"})


@app.get("/files")
async def list_files():
    files = os.listdir(upload_dir)
    return JSONResponse(content={"files": files})


@app.post("/send-message", response_class=HTMLResponse)
async def send_message(message: Message):
    # Process the incoming message
    user_message = message.message
    bot_response = respond_to_message(user_message, "veterinarian")
    return JSONResponse(content={"message": bot_response})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

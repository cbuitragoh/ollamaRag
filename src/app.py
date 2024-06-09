from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from src.logger import create_logger
import os
from src.helpers import (
    respond_to_message,
    load_docs,
    create_pinecone_index,
    create_embeddings,
    add_embeddings_to_pinecone
)

from dotenv import load_dotenv
load_dotenv()

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

# Create a directory to store uploaded files
upload_dir = "./uploads"
os.makedirs(upload_dir, exist_ok=True)

class Message(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        for file in files:
            file_location = os.path.join(upload_dir, file.filename)
            with open(file_location, "wb") as f:
                f.write(file.file.read())

            # Load the document --TODO
                documents = load_docs(file_location)
                if documents is None:
                    logger.error("Error loading document")
                    raise HTTPException(status_code=400, detail="Error loading document")
            
            # create pinecone index
            try: 
                index_name = os.getenv("PINECONE_INDEX_NAME")
                pinecone_key = os.getenv("PINECONE_API_KEY")
                create_pinecone_index(index_name, pinecone_key)
                try:
                    # create embeddings and add to pinecone
                    namespace = os.getenv("PINECONE_NAMESPACE")
                    embeddings = create_embeddings(documents)
                    add_embeddings_to_pinecone(index_name, embeddings, namespace)
                except Exception as e:
                    logger.error(f"Error adding embeddings to Pinecone index: {str(e)}")
                    raise HTTPException(status_code=500, detail="Error adding embeddings to Pinecone index")

            except Exception as e:
                logger.error(f"Error creating Pinecone index: {str(e)}")
                raise HTTPException(status_code=500, detail="Error creating Pinecone index")



        return {"filename": file.filename, "content": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/files")
async def list_files():
    files = os.listdir(upload_dir)
    return JSONResponse(content={"files": files})


@app.post("/send-message", response_class=HTMLResponse)
async def send_message(message: Message):
    # Process the incoming message
    user_message = message.message
    bot_response = respond_to_message(user_message, "formal")
    return JSONResponse(content={"message": bot_response})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

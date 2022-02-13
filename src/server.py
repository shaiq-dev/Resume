from functools import lru_cache
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .functions import get_resume_from_artifact

# Load all the environment variables from .env
load_dotenv()

app = FastAPI()
# To allow cross origin request to the app
# we need to add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/resume", response_class=FileResponse)
async def get_resume():
    pdf_name, pdf_path, *_ = get_resume_from_artifact()
    return FileResponse(pdf_path, media_type="application/pdf", filename=pdf_name)


@app.get("/resume/version")
async def get_resume_version():
    *_, _v = get_resume_from_artifact()
    return JSONResponse(content={"version": _v})

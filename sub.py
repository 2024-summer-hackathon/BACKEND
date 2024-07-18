# REST API 호출, 이미지 파일 처리에 필요한 라이브러리
import requests
from io import StringIO
import json
import urllib
from typing import Annotated
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import pyqrcode
import base64
from PIL import Image
import PIL.Image
import io
from pydantic import BaseModel
import cv2
import numpy as np
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from io import BytesIO

# fastapi 설정
from fastapi import FastAPI, Form
app = FastAPI()

origins = [
	"*"
]

IMAGES_DIR = "./static"
app.mount("/static", StaticFiles(directory=IMAGES_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def upload(string: str = ""):
    return string

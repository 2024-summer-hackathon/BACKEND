# REST API 호출, 이미지 파일 처리에 필요한 라이브러리
import requests
import json
import urllib
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import pyqrcode
import base64
from PIL import Image
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from io import BytesIO
from fastapi.responses import Response

# fastapi 설정
from fastapi import FastAPI, Form
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
	"*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [내 애플리케이션] > [앱 키] 에서 확인한 REST API 키 값 입력
REST_API_KEY = '00349452a2cfec272f15fa75083b880b'

tema = \
{
    "설렘":"flutter", 
    "사랑":"love",
    "힙합":"hiphop",
    "우정":"friendship",
    "에너지 넘치는":"full of energy",
    "콘서트":"concert",
    "축하":"congrats",
    "다정한":"fond"
}
    
def base64_to_image(base64_data):
    base64_data = base64_data.split(',')[1]

    image_data = base64.b64decode(base64_data)

    with open('static/images/out.jpg', 'wb') as img:
        img.write(image_data)

    image_stream = BytesIO(image_data)

    img = Image.open(image_stream)

    return ['static/images/out.jpg', img]

# 이미지 생성하기 요청
def t2i(prompt, negative_prompt):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            "version": "v2.1", 
            "prompt": prompt,
            "image_quality": 100,
            "prior_num_inference_steps": 30,
            "prior_guidance_scale": 3.0,
            "num_inference_steps": 30,
            "guidance_scale": 3.0,
            "negative_prompt": negative_prompt, 
            "height": 1024,
            "width": 1024
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response

@app.get("/pose/")
def pose(string: str = "cute cat", people=2, type: int = 1):
    # 프롬프트에 사용할 제시어
    if(type == 1):
        prompt = "A photo of two high school girls posing for the camera from a distance, using the theme of "+string+" in a american cartoon style."
    elif(type == 2):
        prompt = string
    negative_prompt = ""

    # 이미지 생성하기 REST API 호출
    response = t2i(prompt, negative_prompt)

    # 응답의 첫 번째 이미지 생성 결과 출력하기
    result = Image.open(urllib.request.urlopen(response.get("images")[0].get("image")))
    return response.get("images")[0].get("image")

@app.get("/background/")
def pose(string: str = "cute cat", people=2):
    # 프롬프트에 사용할 제시어
    prompt = "Background photo with the theme of " + string
    negative_prompt = ""

    # 이미지 생성하기 REST API 호출
    response = t2i(prompt, negative_prompt)

    # 응답의 첫 번째 이미지 생성 결과 출력하기
    result = Image.open(urllib.request.urlopen(response.get("images")[0].get("image")))
    return response.get("images")[0].get("image")

class Item(BaseModel):
    string: str

@app.post("/upload")
def upload(item: Item):
    item = dict(item)
    # base64 문자열 디코딩
    print(item['string'])

    base64_data = item['string']

    file_name, image = base64_to_image(base64_data)

    print(image)

    image.show()

    qr_img = pyqrcode.create('http://10.150.151.171:8000/static/images/out.jpg')
    qr_img.svg(file='qr_code.svg', scale=10)
    
    with open("qr_code.svg", "r") as svg_file:
        svg_content = svg_file.read()
    return Response(content=svg_content, media_type="image/svg+xml")

def get_image_url(image_name: str):
    base_url = "http://127.0.0.1:8000"  # 실제 서버 주소로 변경해야 합니다
    image_url = f"{base_url}/{image_name}"
    return {"image_url": image_url}
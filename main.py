# REST API 호출, 이미지 파일 처리에 필요한 라이브러리
import requests
import json
import urllib
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

# fastapi 설정
from fastapi import FastAPI
app = FastAPI()

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
    


# 이미지 생성하기 요청
def t2i(prompt, negative_prompt):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            "version": "v2.1", 
            "prompt": prompt,
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
def pose(string: str = "cute cat", people=2):
    # 프롬프트에 사용할 제시어
    prompt = "A photo of two high school girls posing for the camera from a distance, using the theme of "+string+" in a american cartoon style."
    negative_prompt = ""

    # 이미지 생성하기 REST API 호출
    response = t2i(prompt, negative_prompt)

    # 응답의 첫 번째 이미지 생성 결과 출력하기
    result = Image.open(urllib.request.urlopen(response.get("images")[0].get("image")))
    return response.get("images")[0].get("image")


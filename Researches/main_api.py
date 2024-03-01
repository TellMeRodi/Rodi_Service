from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from fx import *

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Django 서버의 주소
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

traveler = pd.read_csv('./recom_dataset.csv').iloc[:, :-3]
like_city = pd.read_csv('./recom_dataset.csv').iloc[:, [0] + list(range(-3, 0))]


@app.get("/")
# 메인화면
def root():
    return {"message": "Hello World"}

# 추천 api 화면
@app.post("/home/recommendations/")  # POST 메소드로 변경
async def get_recommendations(request: Request):
    try:
        # 요청 본문을 JSON으로 파싱
        data = await request.json()
        recommended_cities = recommend_for_user(data, traveler, like_city)
        traveler_type, traveler_type_cities = find_most_common_type_and_cities(data, recommended_cities)
        return {"recommended_cities": recommended_cities,
                "traveler_type": traveler_type, 
                "traveler_type_cities": traveler_type_cities}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"JSON 파싱 오류: {str(e)}")
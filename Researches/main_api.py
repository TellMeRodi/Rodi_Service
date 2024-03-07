from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from fx import *

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000", # 로컬 서버 
        "http://13.208.95.65:8908", # HHJ
        "http://13.208.95.65:8909", # BHJ
        "http://13.208.95.65:8910", # YGY 
        "http://13.208.95.65:8911", # LDH
        "http://13.208.95.65:8912", # LSH
        "http://13.208.95.65:8913", # CHE
        ], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

traveler = pd.read_csv('./recom_dataset.csv').iloc[:, 1:-3]
like_city = pd.read_csv('./recom_dataset.csv').iloc[:, [1] + list(range(-3, 0))]

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
        additional_recommended_cities = [recommended_city for recommended_city in recommended_cities if recommended_city not in traveler_type_cities][:2]
        return {"recommended_cities": additional_recommended_cities,
                "traveler_type": traveler_type, 
                "traveler_type_cities": traveler_type_cities}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"JSON 파싱 오류: {str(e)}")
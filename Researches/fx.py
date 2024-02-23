import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def rec_data(rawdata):
    age = rawdata['age']
    gender = [0, 1] if rawdata['gender'] == 1 else [1, 0]
    style = []
    for i in range(1, 9):
        if rawdata[f'style{i}'] == 0:
            style.extend([1, 0])
        else:
            style.extend([0, 1])
    MBTI = rawdata['MBTI']
    info= [age] + gender + style + [MBTI]
    return info

def generate_MBTI_list(MBTI):
    MBTI_list = ['MBTI_ENFJ', 'MBTI_ENFP', 'MBTI_ENTJ', 'MBTI_ENTP', 'MBTI_ESFJ', 'MBTI_ESFP', 'MBTI_ESTJ', 'MBTI_ESTP', 'MBTI_INFJ', 'MBTI_INFP', 'MBTI_INTJ', 'MBTI_INTP', 'MBTI_ISFJ', 'MBTI_ISFP', 'MBTI_ISTJ', 'MBTI_ISTP']
    result_list = [0] * len(MBTI_list)  # 초기에는 모든 요소를 0으로 설정

    MBTI_prefix = 'MBTI_' + MBTI
    if MBTI_prefix in MBTI_list:
        index = MBTI_list.index(MBTI_prefix)
        result_list[index] = 1  # 해당 MBTI에 대응하는 인덱스에 1을 할당

    return result_list

# 코사인 유사도 계산
def cos_similarity(info, traveler):
    traveler_X = traveler.loc[traveler[f'MBTI_{info[-1]}']==1]
    target_X = np.array(info[:-1]+generate_MBTI_list(info[-1])).reshape(1, -1)
    similarity_matrix = cosine_similarity(traveler_X.drop('TRAVELER_ID', axis=1).values, target_X)
    similarity_df = pd.DataFrame(similarity_matrix, index=traveler_X['TRAVELER_ID'], columns=['target'])
    return similarity_df

# 가장 유사한 5명의 사용자 선호 여행지 추출
def get_user_preference(top_similar_ids, preference_df):
    # 상위 유사 사용자들의 선호 여행지 목록
    similar_users_cities = preference_df[preference_df['TRAVELER_ID'].isin(top_similar_ids)]

    # 상위 유사 사용자들의 선호 여행지 중 타겟 사용자의 선호 여행지와 겹치지 않는 것만 추출
    recommended_cities_list = []
    for _, row in similar_users_cities.iterrows():
        recommended_cities_list.append(row[['TRAVEL_LIKE_SIDOGUNGU_1', 'TRAVEL_LIKE_SIDOGUNGU_2', 'TRAVEL_LIKE_SIDOGUNGU_3']].tolist())

    # 중복된 여행지를 제거하고 추천 여행지 리스트 반환
    return list(set(np.array(recommended_cities_list).flatten().tolist()))


# 특정 사용자에게 여행지 추천
def recommend_for_user(rawdata, traveler_df, like_city_df):

    info=rec_data(rawdata)
    # 유사도 df 만들기
    similarity_df = cos_similarity(info, traveler_df)

    # 자기 자신을 제외하고, 가장 유사도가 높은 상위 5명의 사용자 찾기
    top_5_similar_ids = similarity_df.nlargest(5, 'target').index

    # 추천 여행지 도출
    # 5명의 유사 사용자 배열
    top_5_ids = top_5_similar_ids.values
    # get_user_preference 함수사용,
    recommended_cities = get_user_preference(top_5_ids, like_city_df)
    # 테스트용

    print(recommended_cities)
    # 결과 반환
    return recommended_cities
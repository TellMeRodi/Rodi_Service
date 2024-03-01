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
    # 결과 반환
    return recommended_cities

def calculate_distance(type_coordinates, type1, type2):
    x1, y1 = type_coordinates[type1]
    x2, y2 = type_coordinates[type2]
    return abs(x1 - x2) + abs(y1 - y2) * 0.7

def create_distance_dataframe():
    # 격자(grid) 정의
    grid = [['USE', 'SLE', 'SSE', 'TLE', 'TSE'],
            ['USR', 'SLR', 'SSR', 'TLR', 'TSR'],
            ['USC', 'SLC', 'SSC', 'TLC', 'TSC'],
            ['USP', 'SLP', 'SSP', 'TLP', 'TSP']]

    # 유형 이름 리스트 생성
    type_names = [type for row in grid for type in row]

    # 유형 간의 거리를 저장할 데이터프레임 생성
    distance_df = pd.DataFrame(index=type_names, columns=type_names)

    # 격자 상의 유형을 좌표로 변환하는 딕셔너리 생성
    type_coordinates = {}
    for i, row in enumerate(grid):
        for j, type_name in enumerate(row):
            type_coordinates[type_name] = (i, j)

    # 모든 유형 쌍에 대해 거리를 계산하여 데이터프레임에 저장
    for type1 in type_names:
        for type2 in type_names:
            distance_df.at[type1, type2] = calculate_distance(type_coordinates, type1, type2)

    return distance_df

def find_most_common_type(data, recommended_cities):
    # 관광유형 거리 df 생성
    distance_df = create_distance_dataframe()
    # MBTI, 관광유형 연결
    mbti_traveltype = {
        'ESTJ': 'SLE', 'ESTP': 'TSP', 'ESFJ': 'SSC', 'ESFP': 'TSE',
        'ENTJ': 'TLR', 'ENTP': 'SLE', 'ENFJ': 'SLR', 'ENFP': 'TSC',
        'ISTJ': 'SLP', 'ISTP': 'SSP', 'ISFJ': 'SSR', 'ISFP': 'TLE',
        'INTJ': 'TLP', 'INTP': 'SSE', 'INFJ': 'TLC', 'INFP': 'TSC'
    }
    # 사용자의 MBTI 조사
    mbti_based_type = mbti_traveltype[data['MBTI']]
    # 관광유형별 관광지 연결
    matrics_20={
      'USE': ['서울특별시'],
      'USR': ['김해시', '대구광역시', '부천시', '시흥시', '인천광역시'],
      'USC': ['서울특별시', '남양주시', '성남시'],
      'USP': ['인천광역시', '평택시', '화성시'],
      'SLE': ['광양시', '광주광역시', '부산광역시', '서울특별시', '대구광역시', '제천시', '청주시', '포항시'],
      'SLR': ['부산광역시', '공주시', '경주시', '논산시', '당진시', '밀양시', '사천시', '서울특별시', '수원시', '순천시', '안동시', '익산시', '전주시', '영천시', '울산광역시', '의왕시', '정읍시'],
      'SLC': ['강릉시', '거제시', '경산시', '광주광역시', '서울특별시', '구미시', '군산시', '김천시', '대구광역시', '대전광역시', '목포시', '부산광역시', '세종시', '양산시', '영주시', '고양시', '울산광역시', '창원시'],
      'SLP': ['광명시', '창원시', '서귀포시', '인천광역시', '여수시', '용인시', '대전광역시', '이천시', '제주시', '춘천시', '충주시', '통영시', '부산광역시'],
      'SSE': ['광주광역시', '나주시', '대전광역시', '서울특별시', '인천광역시', '안양시', '울산광역시', '고양시', '의정부시', '창원시', '천안시', '청주시', '하남시'],
      'SSR': ['고양시', '서산시', '아산시', '양주시', '울산광역시', '진주시', '칠곡군', '포항시'],
      'SSC': ['서울특별시', '광주광역시', '구리시', '군포시', '부산광역시', '대구광역시', '대전광역시', '수원시', '안산시', '안양시', '양평군', '용인시', '원주시', '인천광역시', '전주시', '창원시', '천안시', '청주시'],
      'SSP': ['서울특별시', '인천광역시', '광주시', '김포시', '대전광역시', '성남시', '안성시', '여주시', '오산시', '용인시', '파주시', '포천시'],
      'TLE': ['고성군', '양양군', '영월군', '정선군', '태백시'],
      'TLR': ['고창군', '곡성군', '금산군', '봉화군', '상주시', '서천군', '순창군', '신안군', '영광군', '영동군', '영양군', '예천군', '옥천군', '완도군', '임실군', '장수군', '진도군', '진안군', '함양군', '화천군'],
      'TLC': ['강진군', '고흥군', '구례군', '남원시', '남해군', '단양군', '동해시', '무주군', '문경시', '보령시', '보성군', '부안군', '부여군', '속초시', '양구군', '영덕군', '영암군', '장성군', '장흥군', '청송군', '하동군', '해남군'],
      'TLP': ['삼척시', '울진군', '평창군', '함평군'],
      'TSE': ['대구광역시', '부산광역시', '증평군'],
      'TSR': ['거창군', '계룡시', '고령군', '고성군', '과천시', '괴산군', '대구광역시', '김제시', '담양군', '동두천시', '무안군', '산청군', '연천군', '예산군', '의령군', '의성군', '진천군', '청양군', '함안군', '홍성군'],
      'TSC': ['가평군', '보은군', '성주군', '인천광역시', '완주군', '울릉군', '음성군', '창녕군', '청도군', '태안군', '철원군', '합천군', '화순군', '횡성군'],
      'TSP': ['인천광역시', '인제군', '홍천군']
    }
    # 추천된 여행지 중 해당 관광유형에 카운트하여 사용자에게 가장 가까운 관광유형 찾기
    category_counts = {}
    for city in recommended_cities:
          for category, cities in matrics_20.items():
              if city in cities:
                  category_counts[category] = category_counts.get(category, 0) + 1
    # 사용자에게 가장 가까운 관광유형 출력
    max_category =[k for k,v in category_counts.items() if max(category_counts.values()) == v]
    # 만약 가까운 관광유형이 2개 이상 나온다면 MBTI와 관광유형을 연결한 df(distance_df)를 이용하여 관광유형 찾기
    if len(max_category)>1:
        most_closet_types = distance_df['TSR'].loc[distance_df.index.isin(max_category)].sort_values().index[0]
        return most_closet_types
    else:
        return max_category
    
def find_most_common_type_and_cities(data, recommended_cities):
    matrics_20={
        'USE': ['서울특별시'],
        'USR': ['김해시', '대구광역시', '부천시', '시흥시', '인천광역시'],
        'USC': ['서울특별시', '남양주시', '성남시'],
        'USP': ['인천광역시', '평택시', '화성시'],
        'SLE': ['광양시', '광주광역시', '부산광역시', '서울특별시', '대구광역시', '제천시', '청주시', '포항시'],
        'SLR': ['부산광역시', '공주시', '경주시', '논산시', '당진시', '밀양시', '사천시', '서울특별시', '수원시', '순천시', '안동시', '익산시', '전주시', '영천시', '울산광역시', '의왕시', '정읍시'],
        'SLC': ['강릉시', '거제시', '경산시', '광주광역시', '서울특별시', '구미시', '군산시', '김천시', '대구광역시', '대전광역시', '목포시', '부산광역시', '세종시', '양산시', '영주시', '고양시', '울산광역시', '창원시'],
        'SLP': ['광명시', '창원시', '서귀포시', '인천광역시', '여수시', '용인시', '대전광역시', '이천시', '제주시', '춘천시', '충주시', '통영시', '부산광역시'],
        'SSE': ['광주광역시', '나주시', '대전광역시', '서울특별시', '인천광역시', '안양시', '울산광역시', '고양시', '의정부시', '창원시', '천안시', '청주시', '하남시'],
        'SSR': ['고양시', '서산시', '아산시', '양주시', '울산광역시', '진주시', '칠곡군', '포항시'],
        'SSC': ['서울특별시', '광주광역시', '구리시', '군포시', '부산광역시', '대구광역시', '대전광역시', '수원시', '안산시', '안양시', '양평군', '용인시', '원주시', '인천광역시', '전주시', '창원시', '천안시', '청주시'],
        'SSP': ['서울특별시', '인천광역시', '광주시', '김포시', '대전광역시', '성남시', '안성시', '여주시', '오산시', '용인시', '파주시', '포천시'],
        'TLE': ['고성군', '양양군', '영월군', '정선군', '태백시'],
        'TLR': ['고창군', '곡성군', '금산군', '봉화군', '상주시', '서천군', '순창군', '신안군', '영광군', '영동군', '영양군', '예천군', '옥천군', '완도군', '임실군', '장수군', '진도군', '진안군', '함양군', '화천군'],
        'TLC': ['강진군', '고흥군', '구례군', '남원시', '남해군', '단양군', '동해시', '무주군', '문경시', '보령시', '보성군', '부안군', '부여군', '속초시', '양구군', '영덕군', '영암군', '장성군', '장흥군', '청송군', '하동군', '해남군'],
        'TLP': ['삼척시', '울진군', '평창군', '함평군'],
        'TSE': ['대구광역시', '부산광역시', '증평군'],
        'TSR': ['거창군', '계룡시', '고령군', '고성군', '과천시', '괴산군', '대구광역시', '김제시', '담양군', '동두천시', '무안군', '산청군', '연천군', '예산군', '의령군', '의성군', '진천군', '청양군', '함안군', '홍성군'],
        'TSC': ['가평군', '보은군', '성주군', '인천광역시', '완주군', '울릉군', '음성군', '창녕군', '청도군', '태안군', '철원군', '합천군', '화순군', '횡성군'],
        'TSP': ['인천광역시', '인제군', '홍천군']
    }
    # 사용자의 관광유형 타입
    traveler_type = find_most_common_type(data, recommended_cities)[0]
    # 관광유형타입 중 도시 3개만 출력
    traveler_type_cities = matrics_20[traveler_type][:2]
    return traveler_type, traveler_type_cities
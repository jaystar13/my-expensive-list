MERCHANT_CATEGORY_MAP = {
    "의료비": ["아인치과"],
    "생활비": [
        "빵꾸똥꾸문구야",
        "투썸플레이스",
        "스타벅스",
        "키위스파랜드",
        "족발야시장",
        "키위식당",
        "세라젬",
        "빽다방",
        "친정찬",
        "다이소",
        "몽키청과",
        "떡 하나",
        "보배반점",
        "파리바게뜨",
        "훈남외양간",
    ],
    "교통비": ["KTX", "서울지하철", "버스", "주유소"],
    "저축": ["주택청약"],
    # 필요에 따라 계속 추가
}


def get_category_by_merchant(merchant_name: str) -> str:
    for category, keywords in MERCHANT_CATEGORY_MAP.items():
        if any(keyword in merchant_name for keyword in keywords):
            return category
    return "기타"  # 매칭 안되면 기본값

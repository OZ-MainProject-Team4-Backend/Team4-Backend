import random
from typing import Any, Dict, List, TypedDict


class RecommendRule(TypedDict):
    min: float
    max: float
    combo: List[str]
    tip: str


RECOMMENDATION_RULES: List[RecommendRule] = [
    {
        "min": 30,
        "max": 99,
        "combo": ["민소매+반바지", "반팔+린넨팬츠", "린넨셔츠+반바지"],
        "tip": "매우 더운 날씨에는 통풍이 잘 되는 옷을 착용하세요.",
    },
    {
        "min": 27,
        "max": 29,
        "combo": ["반팔+반바지", "반팔+청바지", "얇은 셔츠+반바지"],
        "tip": "햇빛이 강하니 모자나 선크림을 챙기세요.",
    },
    {
        "min": 23,
        "max": 26,
        "combo": ["반팔+슬랙스", "얇은 셔츠+청바지", "가디건+반팔"],
        "tip": "낮에는 덥지만, 아침저녁으로는 선선할 수 있습니다.",
    },
    {
        "min": 20,
        "max": 22,
        "combo": ["긴팔티+청바지", "맨투맨+면바지", "얇은 가디건+셔츠"],
        "tip": "아침 저녁 일교차에 대비해 겉옷을 챙기세요.",
    },
    {
        "min": 16,
        "max": 19,
        "combo": ["셔츠+가디건", "니트+청바지", "후드티+슬랙스"],
        "tip": "얇은 니트나 후드티로 체온을 유지하세요.",
    },
    {
        "min": 12,
        "max": 15,
        "combo": ["니트+자켓", "맨투맨+청바지", "후드+조거팬츠"],
        "tip": "겉옷을 꼭 챙기세요. 낮엔 덥지만 밤엔 쌀쌀합니다.",
    },
    {
        "min": 6,
        "max": 11,
        "combo": ["코트+니트", "자켓+맨투맨", "후드+패딩조끼"],
        "tip": "바람막이나 코트를 착용하세요.",
    },
    {
        "min": -99,
        "max": 5,
        "combo": ["패딩+니트", "두꺼운 코트+머플러", "후드+패딩"],
        "tip": "두꺼운 외투와 장갑, 머플러로 체온을 유지하세요.",
    },
]


def get_recommendation(feels_like: float) -> Dict[str, Any]:
    for rule in RECOMMENDATION_RULES:
        if rule["min"] <= feels_like <= rule["max"]:
            combo: List[str] = random.sample(
                rule["combo"], k=min(3, len(rule["combo"]))
            )
            return {
                "feels_like": feels_like,
                "rec_1": combo[0],
                "rec_2": combo[1] if len(combo) > 1 else None,
                "rec_3": combo[2] if len(combo) > 2 else None,
                "tip": rule["tip"],
            }
    # 예외 처리
    return {
        "feels_like": feels_like,
        "rec_1": "데이터 없음",
        "rec_2": None,
        "rec_3": None,
        "tip": "체감온도 데이터를 확인할 수 없습니다.",
    }

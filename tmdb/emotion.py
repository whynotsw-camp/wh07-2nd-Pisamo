# 감정 분석(score_emotions)

import re

# emotions.id 매핑:
# 1: 기쁨, 2: 분노, 3: 슬픔, 4: 상처, 5: 당황, 6: 불안
EMO_KEYWORDS = {
    1: ["행복", "유쾌", "사랑", "감동", "희망", "축제", "웃음", "따뜻", "해피"],
    2: ["복수", "분노", "격노", "분개", "증오", "대립", "분쟁", "폭력"],
    3: ["슬픔", "눈물", "비극", "상실", "외로움", "그리움", "우울"],
    4: ["배신", "상처", "가혹", "트라우마", "학대", "괴롭힘", "모욕"],
    5: ["당황", "실수", "어색", "난처", "혼란", "황당", "우왕좌왕"],
    6: ["불안", "공포", "위기", "긴장", "위협", "두려움", "의심", "초조"],
}

def score_emotions(text: str) -> dict:
    """
    간단 키워드 매칭으로 6감정 점수(0~1) 계산.
    KoBERT로 교체시 이 함수만 변경하면 됨.
    """
    if not text:
        return {eid: 0.0 for eid in EMO_KEYWORDS.keys()}

    t = re.sub(r"\s+", " ", text.lower())
    raw = {}
    for eid, kws in EMO_KEYWORDS.items():
        s = 0
        for kw in kws:
            s += t.count(kw.lower())
        raw[eid] = float(s)

    total = sum(raw.values()) or 1.0
    return {eid: round(raw[eid] / total, 4) for eid in raw}

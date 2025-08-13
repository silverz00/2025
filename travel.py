import streamlit as st
from dataclasses import dataclass, field
from typing import List, Dict
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Trip Concept → Destinations", page_icon="🧭", layout="wide")

# -------------------- Helpers --------------------
SEED_BASE = 42  # 기본 시드(사이드바에서 변경 가능)

def photo(query: str, seed: int = 0, w: int = 900, h: int = 600) -> str:
    """Return a stable-ish Unsplash image URL for a keyword.
    사이드바의 시드 값을 더해 이미지 구성을 고정할 수 있습니다.
    """
    random.seed(hash(query) + seed + SEED_BASE)
    sig = random.randint(1, 10_000)
    return f"https://source.unsplash.com/{w}x{h}/?{query}&sig={sig}"

@dataclass
class Food:
    name: str
    note: str
    img_query: str

@dataclass
class Destination:
    name: str
    country: str
    region: str
    coords: tuple  # (lat, lon)
    concepts: List[str]
    best_months: List[int]
    budget: str  # $, $$, $$$
    blurb: str
    gallery_queries: List[str]
    foods: List[Food] = field(default_factory=list)
    activities: List[str] = field(default_factory=list)

# -------------------- Data --------------------
CONCEPTS = [
    "휴양/힐링 (Relaxation)",
    "모험/액티비티 (Adventure)",
    "역사·문화 (Culture & History)",
    "자연 풍경 (Nature)",
    "도시 야경·쇼핑 (City Nightlife)",
    "가족 여행 (Family)",
    "가성비 (Budget)",
    "럭셔리 (Luxury)",
    "로맨틱 (Romantic)",
    "미식 투어 (Foodie)",
]

DSTS: List[Destination] = [
    Destination(
        name="제주도 (Jeju)", country="대한민국", region="East Asia", coords=(33.4996, 126.5312),
        concepts=["휴양/힐링 (Relaxation)", "자연 풍경 (Nature)", "가족 여행 (Family)", "미식 투어 (Foodie)"],
        best_months=[4,5,6,9,10], budget="$$", 
        blurb="오름, 해변, 한라산까지 다양한 자연과 흑돼지, 갈치회 등 먹거리가 풍부한 섬.",
        gallery_queries=["Jeju island coast", "Hallasan", "Jeju oreum", "Jeju beach", "Jeju tangerine farm", "Jeju cafe view"],
        foods=[
            Food("흑돼지", "숯불에 구워 먹는 제주 대표 고기", "Jeju black pork"),
            Food("갈치회/구이", "신선한 갈치 요리", "hairtail fish dish"),
            Food("한치물회", "시원한 해산물 냉채", "korean seafood mulhoe"),
        ],
        activities=["오름 트래킹", "용머리해안 산책", "우도 자전거", "한라산 등반"],
    ),
    Destination(
        name="오사카 (Osaka)", country="일본", region="East Asia", coords=(34.6937, 135.5023),
        concepts=["미식 투어 (Foodie)", "가족 여행 (Family)", "도시 야경·쇼핑 (City Nightlife)"],
        best_months=[3,4,10,11], budget="$$", 
        blurb="타코야키와 오코노미야키의 성지. 유니버설 스튜디오와 도톤보리 야경.",
        gallery_queries=["Osaka Dotonbori night", "Osaka castle", "Kuromon market", "USJ Osaka", "Shinsaibashi", "Osaka street food"],
        foods=[
            Food("타코야키", "문어볼 간식", "osaka takoyaki"),
            Food("오코노미야키", "일본식 부침", "okonomiyaki"),
            Food("규카츠", "겉바속촉 소고기 카츠", "gyukatsu"),
        ],
        activities=["도톤보리 산책", "유니버설 스튜디오", "쿠로몬 시장"],
    ),
    Destination(
        name="교토 (Kyoto)", country="일본", region="East Asia", coords=(35.0116, 135.7681),
        concepts=["역사·문화 (Culture & History)", "로맨틱 (Romantic)", "미식 투어 (Foodie)"],
        best_months=[3,4,11,12], budget="$$$",
        blurb="사찰과 정원이 살아있는 천년 고도. 와가시와 말차 디저트가 유명.",
        gallery_queries=["Kyoto Fushimi Inari", "Arashiyama bamboo", "Kiyomizu-dera", "Gion street", "Kyoto garden", "matcha dessert"],
        foods=[
            Food("카이세키", "계절 코스 요리", "kaiseki cuisine"),
            Food("말차 디저트", "녹차의 달콤쌉싸름", "matcha parfait"),
            Food("유바", "두유 껍질 요리", "yuba tofu skin"),
        ],
        activities=["아라시야마 대나무숲", "후시미 이나리 신사", "기온 거리"],
    ),
    Destination(
        name="방콕 (Bangkok)", country="태국", region="Southeast Asia", coords=(13.7563, 100.5018),
        concepts=["도시 야경·쇼핑 (City Nightlife)", "미식 투어 (Foodie)", "가성비 (Budget)"],
        best_months=[11,12,1,2,3], budget="$",
        blurb="활기찬 야시장과 루프탑 바, 그리고 세계적 수준의 길거리 음식.",
        gallery_queries=["Bangkok skyline night", "Bangkok street food", "Chatuchak market", "Wat Arun sunset", "Rooftop bar Bangkok", "Chao Phraya boat"],
        foods=[
            Food("팟타이", "태국식 볶음면", "pad thai"),
            Food("똠얌꿍", "매콤한 새우 수프", "tom yum goong"),
            Food("망고 스티키 라이스", "달콤한 디저트", "mango sticky rice"),
        ],
        activities=["왓 아룬/왓 포 사원", "짜오프라야 보트", "야시장 쇼핑"],
    ),
    Destination(
        name="다낭 (Da Nang)", country="베트남", region="Southeast Asia", coords=(16.0544, 108.2022),
        concepts=["휴양/힐링 (Relaxation)", "가성비 (Budget)", "가족 여행 (Family)"],
        best_months=[2,3,4,5,8,9], budget="$",
        blurb="한적한 해변과 바나힐, 호이안 접근성 좋은 휴양 도시.",
        gallery_queries=["Da Nang beach", "Ba Na Hills", "Hoi An lanterns", "Marble Mountains Vietnam", "My Khe beach", "Golden Bridge Vietnam"],
        foods=[
            Food("미꽝", "다낭 지역 쌀국수", "mi quang"),
            Food("반쎄오", "바삭한 베트남 전", "banh xeo"),
            Food("까페 쓰어다", "연유 아이스커피", "Vietnamese iced coffee"),
        ],
        activities=["바나힐/골든브릿지", "호이안 야경", "마블 마운틴"]
    ),
    Destination(
        name="발리 (Bali)", country="인도네시아", region="Southeast Asia", coords=(-8.4095, 115.1889),
        concepts=["휴양/힐링 (Relaxation)", "로맨틱 (Romantic)", "미식 투어 (Foodie)"],
        best_months=[4,5,6,7,8,9], budget="$$",
        blurb="비치와 우붓의 논밭 풍경, 카페 문화까지 즐기는 감성 휴양지.",
        gallery_queries=["Bali beach", "Ubud rice terrace", "Bali cafe", "Bali swing", "Nusa Penida", "Bali sunset temple"],
        foods=[
            Food("바비굴링", "수꾸돼지 구이", "babi guling"),
            Food("나시고렝", "인도네시아 볶음밥", "nasi goreng"),
            Food("사테", "꼬치구이", "satay Indonesia"),
        ],
        activities=["해변 휴양", "요가/스파", "논밭 뷰 카페"]
    ),
    Destination(
        name="타이베이 (Taipei)", country="대만", region="East Asia", coords=(25.0330, 121.5654),
        concepts=["미식 투어 (Foodie)", "가성비 (Budget)", "가족 여행 (Family)"],
        best_months=[10,11,12,3,4], budget="$",
        blurb="야시장 중심의 먹거리 천국. 근교 지우펀/예류도 매력적.",
        gallery_queries=["Taipei night market", "Taipei 101", "Jiufen old street", "Yehliu geopark", "Taipei street food", "Ximending"],
        foods=[
            Food("소고기면", "진한 국물의 우육면", "taiwan beef noodle"),
            Food("샤오롱바오", "육즙 가득 만두", "xiao long bao"),
            Food("버블티", "대만 밀크티", "bubble tea"),
        ],
        activities=["스린 야시장", "지우펀 당일치기", "온천"]
    ),
    Destination(
        name="파리 (Paris)", country="프랑스", region="Europe", coords=(48.8566, 2.3522),
        concepts=["로맨틱 (Romantic)", "역사·문화 (Culture & History)", "미식 투어 (Foodie)"],
        best_months=[4,5,6,9,10], budget="$$$",
        blurb="예술과 카페 문화의 도시. 세느 강변 산책과 미슐랭 베이커리.",
        gallery_queries=["Paris Eiffel sunrise", "Seine river walk", "Louvre museum", "Montmartre", "Paris cafe", "Paris croissant"],
        foods=[
            Food("크루아상", "겹겹의 버터 향", "croissant paris"),
            Food("스테이크 프리츠", "감튀와 스테이크", "steak frites"),
            Food("마카롱", "달콤한 한입", "macaron paris"),
        ],
        activities=["루브르/오르세", "세느강 크루즈", "몽마르트 언덕"]
    ),
    Destination(
        name="로마 (Rome)", country="이탈리아", region="Europe", coords=(41.9028, 12.4964),
        concepts=["역사·문화 (Culture & History)", "미식 투어 (Foodie)", "로맨틱 (Romantic)"],
        best_months=[4,5,10,11], budget="$$$",
        blurb="유적과 골목의 낭만. 젤라또와 카르보나라의 본고장.",
        gallery_queries=["Rome Colosseum", "Trevi fountain", "Trastevere", "Roman Forum", "Pantheon interior", "Rome gelato"],
        foods=[
            Food("카르보나라", "계란·치즈의 풍미", "carbonara pasta"),
            Food("젤라또", "쫀득한 아이스크림", "gelato italy"),
            Food("피자 알 타글리오", "조각 피자", "pizza al taglio"),
        ],
        activities=["콜로세움 투어", "바티칸/성베드로", "트라스테베레 산책"]
    ),
    Destination(
        name="이스탄불 (Istanbul)", country="튀르키예", region="Europe/Asia", coords=(41.0082, 28.9784),
        concepts=["역사·문화 (Culture & History)", "미식 투어 (Foodie)", "도시 야경·쇼핑 (City Nightlife)"],
        best_months=[4,5,9,10], budget="$$",
        blurb="동서양의 관문. 시장과 모스크, 보스포루스의 야경.",
        gallery_queries=["Istanbul Hagia Sophia", "Blue Mosque", "Grand Bazaar", "Bosphorus night", "Istanbul street food", "Galata tower"],
        foods=[
            Food("케밥", "불향 가득", "turkish kebab"),
            Food("로쿰", "터키시 딜라이트", "turkish delight lokum"),
            Food("시미트", "참깨 베이글", "simit"),
        ],
        activities=["보스포루스 크루즈", "그랜드 바자르", "모스크 방문"]
    ),
    Destination(
        name="퀸스타운 (Queenstown)", country="뉴질랜드", region="Oceania", coords=(-45.0312, 168.6626),
        concepts=["모험/액티비티 (Adventure)", "자연 풍경 (Nature)"],
        best_months=[12,1,2,3], budget="$$$",
        blurb="번지점프와 트레킹, 남알프스의 절경.",
        gallery_queries=["Queenstown bungee", "Milford Sound", "Queenstown lake wakatipu", "New Zealand hiking", "Glenorchy", "Queenstown skyline"],
        foods=[
            Food("램", "뉴질랜드산 양고기", "new zealand lamb dish"),
            Food("피시앤칩스", "바삭한 생선튀김", "fish and chips"),
        ],
        activities=["번지/스카이다이빙", "밀포드 사운드 크루즈", "레이크 와카티푸"]
    ),
    Destination(
        name="인터라켄 (Interlaken)", country="스위스", region="Europe", coords=(46.6863, 7.8632),
        concepts=["모험/액티비티 (Adventure)", "자연 풍경 (Nature)", "로맨틱 (Romantic)"],
        best_months=[6,7,8,9], budget="$$$",
        blurb="융프라우 요흐, 패러글라이딩, 호수 뷰.",
        gallery_queries=["Interlaken paragliding", "Jungfraujoch", "Lake Brienz", "Lake Thun", "Swiss Alps hiking", "Grindelwald"],
        foods=[
            Food("퐁뒤", "치즈의 나라", "cheese fondue"),
            Food("뢰스티", "감자 요리", "rosti swiss"),
        ],
        activities=["패러글라이딩", "융프라우 철도", "하이킹"]
    ),
    Destination(
        name="밴프 (Banff)", country="캐나다", region="North America", coords=(51.1784, -115.5708),
        concepts=["자연 풍경 (Nature)", "모험/액티비티 (Adventure)"],
        best_months=[6,7,8,9], budget="$$$",
        blurb="터키석 호수와 웅장한 로키산맥.",
        gallery_queries=["Banff Lake Louise", "Moraine Lake", "Banff National Park", "Icefields Parkway", "Johnston Canyon", "Banff gondola"],
        foods=[
            Food("푸틴", "그레이비 감자", "poutine"),
        ],
        activities=["호수 카누", "국립공원 드라이브", "캐니언 트레킹"]
    ),
    Destination(
        name="싱가포르 (Singapore)", country="싱가포르", region="Southeast Asia", coords=(1.3521, 103.8198),
        concepts=["가족 여행 (Family)", "도시 야경·쇼핑 (City Nightlife)", "미식 투어 (Foodie)"],
        best_months=[2,3,6,7,8], budget="$$$",
        blurb="쾌적한 도시, 센토사와 가든스 바이 더 베이.",
        gallery_queries=["Singapore Marina Bay night", "Gardens by the Bay", "Sentosa beach", "Jewel Changi", "Chinatown Singapore", "Hawker centre"],
        foods=[
            Food("치킨라이스", "국민 음식", "hainanese chicken rice"),
            Food("칠리크랩", "매콤한 게 요리", "singapore chili crab"),
            Food("락사", "코코넛 누들 수프", "laksa"),
        ],
        activities=["가든스 바이 더 베이", "센토사", "호커센터 투어"]
    ),
    Destination(
        name="두바이 (Dubai)", country="UAE", region="Middle East", coords=(25.2048, 55.2708),
        concepts=["럭셔리 (Luxury)", "도시 야경·쇼핑 (City Nightlife)", "모험/액티비티 (Adventure)"],
        best_months=[11,12,1,2,3,4], budget="$$$",
        blurb="초고층 스카이라인, 사막 사파리, 대형 쇼핑몰.",
        gallery_queries=["Dubai skyline night", "Burj Khalifa", "Dubai desert safari", "Palm Jumeirah", "Dubai marina", "Dubai mall"],
        foods=[
            Food("메즈", "중동 전채 요리", "arabic mezze"),
            Food("만디", "향신료 쌀요리", "mandi rice"),
        ],
        activities=["버즈 칼리파 전망", "사막 사파리", "요트 크루즈"]
    ),
    Destination(
        name="산토리니 (Santorini)", country="그리스", region="Europe", coords=(36.3932, 25.4615),
        concepts=["로맨틱 (Romantic)", "휴양/힐링 (Relaxation)", "럭셔리 (Luxury)"],
        best_months=[5,6,9,10], budget="$$$",
        blurb="하얀 집과 파란 돔, 석양 맛집.",
        gallery_queries=["Santorini sunset", "Oia blue domes", "Santorini cliff hotel", "Santorini alley", "Ammoudi Bay", "Santorini wine"],
        foods=[
            Food("수블라키", "그리스식 꼬치", "souvlaki"),
            Food("무사카", "가지 그라탱", "moussaka"),
        ],
        activities=["오이아 일몰", "요트 투어", "와이너리"]
    ),
    Destination(
        name="프라하 (Prague)", country="체코", region="Europe", coords=(50.0755, 14.4378),
        concepts=["로맨틱 (Romantic)", "역사·문화 (Culture & History)", "가성비 (Budget)"],
        best_months=[5,6,9,10,12], budget="$$",
        blurb="고딕과 중세의 동화 도시. 야경과 맥주.",
        gallery_queries=["Prague Charles Bridge sunrise", "Prague old town square", "Prague castle", "Prague night view", "Prague trdelnik", "Prague streets"],
        foods=[
            Food("굴라쉬", "빵 그릇 스튜", "goulash bread bowl"),
            Food("트르들로", "굴레 디저트", "trdelnik"),
        ],
        activities=["카를교 일출", "프라하 성", "맥주 투어"]
    ),
]

# -------------------- Sidebar Controls --------------------
st.sidebar.title("여행 컨셉 선택")
concept = st.sidebar.selectbox("원하는 여행 컨셉을 고르세요", CONCEPTS)
month = st.sidebar.select_slider("여행 예정 월(선택)", options=list(range(1,13)), value=datetime.now().month)
count = st.sidebar.slider("추천 개수", min_value=3, max_value=8, value=5)

st.sidebar.markdown("---")
st.sidebar.subheader("추가 필터")
budget_filter = st.sidebar.multiselect("예산(중복 선택)", options=["$","$$","$$$"], default=["$","$$","$$$"])
region_pref = st.sidebar.multiselect("지역 선호", options=sorted({d.region for d in DSTS}), default=[])
kr_only = st.sidebar.checkbox("대한민국 내 추천만", value=False)

st.sidebar.markdown("---")
st.sidebar.subheader("이미지 고정 옵션")
seed_in = st.sidebar.number_input("이미지 시드", min_value=0, max_value=99999, value=42, step=1)

# 시드 업데이트
SEED_BASE = int(seed_in)

st.sidebar.markdown("---")
st.sidebar.subheader("일정 생성기")
days = st.sidebar.slider("여행 일수", min_value=2, max_value=7, value=3)
pace = st.sidebar.select_slider("여행 템포", options=["여유", "보통", "빡빡"], value="보통")

# -------------------- Ranking --------------------
scored: List[Dict] = []
for d in DSTS:
    if concept not in d.concepts:
        continue
    if d.budget not in budget_filter:
        continue
    if kr_only and d.country != "대한민국":
        continue
    score = 1.0
    if month in d.best_months:
        score += 0.6
    if region_pref:
        if d.region in region_pref:
            score += 0.3
        else:
            score -= 0.2
    rnd = (hash(d.name) % 100) / 1000.0  # small tie-breaker
    score += rnd
    scored.append({"dest": d, "score": score})

scored.sort(key=lambda x: x["score"], reverse=True)
results = [s["dest"] for s in scored][:count]

# -------------------- Itinerary Generator --------------------
def generate_itinerary(d: Destination, days: int, pace: str) -> List[Dict]:
    """간단 일정 생성: 오전/오후/저녁 × days
    활동과 음식 추천을 섞어 구성합니다.
    pace: 여유(1~2 활동), 보통(2 활동), 빡빡(2~3 활동)
    """
    blocks = []
    act_pool = d.activities if d.activities else ["도시 산책", "포토 스팟", "현지 시장"]
    food_pool = d.foods if d.foods else [Food("현지 식당", "로컬 맛집 탐방", d.gallery_queries[0] if d.gallery_queries else d.name)]
    for day in range(1, days+1):
        if pace == "여유":
            num_act = 1 if day % 2 == 0 else 2
        elif pace == "빡빡":
            num_act = 3 if day % 2 == 0 else 2
        else:
            num_act = 2
        acts = [act_pool[(day+i) % len(act_pool)] for i in range(num_act)]
        food = food_pool[day % len(food_pool)]
        blocks.append({
            "day": day,
            "morning": acts[0],
            "afternoon": acts[1] if len(acts) > 1 else "자유 시간",
            "evening": "야경/바" if "도시" in " ".join(d.concepts) else "휴식",
            "must_eat": food.name,
        })
    return blocks

# -------------------- Header --------------------
st.title("🧭 여행 컨셉 기반 추천")
st.caption("컨셉만 고르면, 사진과 먹거리까지 한 번에!  — *Streamlit demo* ")

if not results:
    st.warning("선택한 조건에 맞는 추천이 없습니다. 필터를 조정해 보세요.")
    st.stop()

export_rows = []

# -------------------- Cards --------------------
for d in results:
    st.markdown("---")
    head_cols = st.columns([1.2, 2])
    with head_cols[0]:
        st.image(photo(d.gallery_queries[0], seed=1), caption=d.name)
        st.metric("베스트 시즌", ", ".join(f"{m}월" for m in sorted(set(d.best_months))))
        st.write(f"예산대: **{d.budget}** · 지역: **{d.region}**")
    with head_cols[1]:
        st.subheader(f"{d.name} — {d.country}")
        st.write(d.blurb)
        tag_cols = st.columns(len(d.concepts))
        for i, c in enumerate(d.concepts):
            with tag_cols[i]:
                st.button(c, key=f"tag-{d.name}-{i}")
        if d.activities:
            st.write("**추천 액티비티**: " + ", ".join(d.activities))
        # 빠른 검색 버튼(구글 맵)
        q = f"{d.name} best restaurants"
        st.link_button("🍴 지도에서 맛집 검색", url=f"https://www.google.com/maps/search/{q}")

    with st.expander("📸 사진 더 보기 / 🍽️ 대표 음식 보기 / 🗓️ 일정 제안", expanded=True):
        # Gallery
        st.markdown("#### 📸 갤러리")
        gallery_cols = st.columns(3)
        for i, q in enumerate(d.gallery_queries[:6]):
            with gallery_cols[i % 3]:
                st.image(photo(q, seed=i+2), use_column_width=True)

        # Foods
        st.markdown("#### 🍽️ 현지 맛집 메뉴")
        fcols = st.columns(3)
        for i, f in enumerate(d.foods):
            with fcols[i % 3]:
                st.image(photo(f.img_query, seed=i+20, w=600, h=400))
                # 지도 빠른 검색
                maps_q = f"{d.name} {f.name}"
                st.markdown(f"**{f.name}** — {f.note}  ")
                st.link_button("지도에서 찾기", url=f"https://www.google.com/maps/search/{maps_q}")

        # Itinerary
        st.markdown("#### 🗓️ 자동 일정 (초안)")
        plan = generate_itinerary(d, days, pace)
        for blk in plan:
            st.write(f"**Day {blk['day']}** — 오전: {blk['morning']} · 오후: {blk['afternoon']} · 저녁: {blk['evening']} · *Must Eat*: {blk['must_eat']}")

    # Map
    if d.coords:
        st.markdown("#### 🗺️ 위치")
        df = pd.DataFrame({"lat": [d.coords[0]], "lon": [d.coords[1]]})
        st.map(df, zoom=6)

    # 수집: 내보내기용
    export_rows.append({
        "Destination": d.name,
        "Country": d.country,
        "Region": d.region,
        "Budget": d.budget,
        "Concepts": ", ".join(d.concepts),
        "Best Months": ", ".join(map(str, sorted(set(d.best_months)))),
        "Foods": ", ".join(f.name for f in d.foods),
        "Activities": ", ".join(d.activities) if d.activities else "",
    })

# -------------------- Export --------------------
st.markdown("---")
export_df = pd.DataFrame(export_rows)
st.download_button(
    label="⬇️ 추천 목록 CSV로 저장",
    data=export_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="trip_recommendations.csv",
    mime="text/csv",
)

st.markdown(
    """
    **Tip**: 사이드바에서 예산/지역/월/시드를 바꾸면 추천과 이미지가 즉시 업데이트됩니다.  
    이미지는 Unsplash 키워드를 활용하여 자동으로 가져옵니다. 상업 사용 시 각 장소/음식 정확성은 직접 확인해 주세요.
    """
)

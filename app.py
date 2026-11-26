import streamlit as st
import pandas as pd

# 1. 데이터 구조 (리스트 활용 - 맵기 낮은 순: 육개장 -> 신라면 -> 불닭볶음면)
spicy_food_list = ["육개장", "신라면", "불닭볶음면"]

# 음식별 맵찔이 단계 기준 및 이유 데이터 (이중 리스트: 변수명 수정)
no_hot_food_level = [
    ["육개장", "1단계 (하)", "청양고추가 있어도 잘 먹는 입문 단계로 적당한 칼칼함"],
    ["신라면", "2단계 (중)", "한 번 먹을 때 못 먹을 정도는 아니지만 땀이 송글송글 맺히는 단계"],
    ["불닭볶음면", "3단계 (상)", "매운맛에 매우 취약하면 위장에 무리가 가는 극한의 매운맛 단계"]
]

# 2. 함수 정의 (def 및 snake_case 준수: 함수명 및 매개변수 수정)
def check_lists(spicy_food, ages):
    # 음식별 기본 위험도 점수, 경고 메시지, 상세 이유, 맞춤 추천 설정 (선택구조 if-elif-else)
    if spicy_food == "육개장":
        risk_score = 35
        warning_msg = "가벼운 주의가 필요합니다. (부담 없는 입문용 얼큰함)"
        reason_text = "고추기름과 후추의 가벼운 알싸함이 있는 수준으로, 매운 음식을 잘 못 먹는 초보 맵찔이도 무난하게 도전할 수 있습니다."
        recommend_text = "뜨거운 국물을 한 번에 들이켜지만 않으면 충분히 맛있게 즐길 수 있으며, 단무지를 곁들이면 더욱 깔끔합니다."
    elif spicy_food == "신라면":
        risk_score = 65
        warning_msg = "중간 수준의 주의가 필요합니다. (한국인 평균 맵기 자극)"
        reason_text = "스코빌 지수 약 3,400 SHU로, 평소 매운 음식을 즐기지 않는 사람에게는 혀가 얼얼하고 땀이 맺힐 수 있는 맵기입니다."
        recommend_text = "계란을 풀거나 치즈 1장을 올려 먹으면 매운맛이 중화되어 훨씬 부드럽게 즐길 수 있습니다."
    else:  # 불닭볶음면
        risk_score = 90
        warning_msg = "매우 각별한 주의가 필요합니다! (맵찔이 경보 발령)"
        reason_text = "스코빌 지수 약 4,400 SHU 이상의 강렬한 캡사이신 소스로, 속쓰림과 복통을 유발할 가능성이 매우 높습니다."
        recommend_text = "액상 소스를 절반만 먼저 넣고 비벼 드시거나, 우유·계란찜·참치마요 삼각김밥과 반드시 함께 드세요!"

    # 나이에 따른 추가 위험도 가산 (선택구조 if-elif-else)
    if ages <= 10:
        risk_score += 50
        warning_msg += " [10세 이하 어린이 고위험 주의: 매운 성분이 위장에 매우 강하게 자극을 줄 수 있습니다]"
    elif ages >= 60:
        risk_score += 10
        warning_msg += " [60세 이상 고령자 주의: 소화 기능 보호를 위해 섭취량을 줄이세요]"
    else:
        warning_msg += " [일반 연령: 본인의 컨디션에 맞게 조절하세요]"

    # 최대 점수 100점 제한
    if risk_score > 100:
        risk_score = 100

    return risk_score, warning_msg, reason_text, recommend_text

# --- 3. Streamlit 웹 화면 UI 구성 ---
st.title("🌶️ 맞춤형 매운음식 섭취 가이드")
st.write("선택한 매운 음식과 나이를 바탕으로 나의 맵찔이 위험도와 맞춤 꿀팁을 확인해보세요!")

st.divider()

# 사용자 입력 받기 (드롭다운 & 숫자 직접 입력 칸)
selected_food = st.selectbox("매운 음식 선택:", spicy_food_list)
user_age = st.number_input("나이 입력 (숫자를 직접 입력하세요):", min_value=1, max_value=100, value=17, step=1)

# 결과 확인 버튼
if st.button("위험도 및 맞춤 추천 확인하기"):
    # 수정된 함수 호출하여 4가지 결과 받아오기
    final_score, final_message, final_reason, final_recommend = check_lists(selected_food, user_age)

    st.subheader(f"📊 '{selected_food}' 맞춤 분석 결과 (입력 나이: {user_age}세)")

    # 강조 수치 (Metric) 형태로 위험도 점수 출력
    st.metric(label="나의 매운음식 위험도 점수", value=f"{final_score} 점")

    # 텍스트 경고 메시지 출력
    st.warning(final_message)

    # 선택한 음식에 따른 상세 이유 및 추천 문구 출력
    st.info(f"💡 위험도 산정 이유: {final_reason}")
    st.success(f"🍽️ 맞춤 섭취 추천: {final_recommend}")

    st.divider()

    # 4. 반복문 (for)과 조건문(if)을 이용한 표 생성용 데이터 변환 및 출력
    st.subheader("📋 매운음식별 맵찔이 단계 주의표")

    table_data = []
    for item in no_hot_food_level:
        # 현재 선택한 음식인지 표시해주기 (선택구조 활용)
        if item[0] == selected_food:
            food_name = f"👉 {item[0]} (현재 선택)"
        else:
            food_name = item[0]

        table_data.append({
            "음식 이름": food_name,
            "맵찔이 위험도": item[1],
            "단계별 기준 및 이유": item[2]
        })

    # DataFrame 표 형태로 화면에 출력
    df = pd.DataFrame(table_data)
    st.table(df)

import streamlit as st
import random

# 저녁 메뉴 리스트
menus = [
    "김치찌개",
    "된장찌개",
    "삼겹살",
    "치킨",
    "피자",
    "초밥",
    "제육볶음",
    "떡볶이",
    "햄버거",
    "파스타"
]

st.title("🍽️ 저녁 메뉴 추천")

st.write("버튼을 누르면 오늘 저녁 메뉴를 추천해드립니다!")

if st.button("추천 받기"):
    menu = random.choice(menus)
    st.success(f"오늘 저녁은 👉 {menu}")

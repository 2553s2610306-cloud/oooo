import streamlit as tf
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="달콤살벌 연애상담소", page_icon="💌", layout="centered")
st.title("💌 달콤살벌 연애상담소")
st.caption("연애 고민, 썸, 이별... 누구에게도 말 못 한 속마음을 털어놓으세요. (Gemini 2.5 Flash-Lite 구동)")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Streamlit Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. 설정 후 다시 시도해주세요.")
    st.stop()

try:
    # 최신 google-genai SDK 초기화 방식
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error(f"클라이언트 초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 3. 세션 상태(Session State)로 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. 기존 채팅 기록 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 받기
if prompt := st.chat_input("연애 고민을 입력하세요... (예: 썸남이 선톡을 안 해요...)"):
    # 사용자 메시지 화면에 표시 및 세션 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 6. Gemini 모델을 통한 답변 생성 (오류 처리 포함)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🤔 고민을 분석하며 답변을 생각 중이에요...")
        
        try:
            # 연애상담사 페르소나 부여를 위한 시스템 지침 (원하는 대로 수정 가능)
            system_instruction = (
                "당신은 공감 능력이 뛰어나면서도 때로는 뼈 때리는 조언을 해주는 전문 연애 상담사입니다. "
                "친근하고 다정한 말투(반말과 존댓말을 적절히 섞거나 친근한 대화체)로 답변해 주세요. "
                "사용자의 감정에 깊이 공감해 주되, 현실적인 해결책이나 생각해 볼 점을 함께 제시해 주세요. "
                "이모지를 적절히 섞어서 답변을 지루하지 않게 만들어 주세요."
            )
            
            # API 호출용 이전 대화 기록 가공 (Gemini Content 형식에 맞춤)
            contents = []
            for m in st.session_state.messages:
                contents.append(
                    types.Content(
                        role="user" if m["role"] == "user" else "model",
                        parts=[types.Part.from_text(text=m["content"])]
                    )
                )

            # gemini-2.5-flash-lite 모델 호출
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7, # 창의적인 답변을 위해 약간 높임
                )
            )
            
            # 답변 출력 및 세션 저장
            ai_response = response.text
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

        except APIError as e:
            # 구글 API 관련 에러 처리
            message_placeholder.markdown("❌ **API 오류가 발생했습니다.** 잠시 후 다시 시도해 주세요.")
            st.error(f"상세 API 오류: {e}")
        except Exception as e:
            # 기타 일반 에러 처리
            message_placeholder.markdown("❌ **알 수 없는 오류가 발생했습니다.**")
            st.error(f"상세 오류: {e}")

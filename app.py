import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Streamlit UI 설정
st.set_page_config(page_title="💬 AI 챗봇", layout="wide")
st.title("🤖 AI 챗봇")
st.write("💬 질문을 입력하면 AI가 답변합니다. ('exit' 입력 시 종료)")

# 로컬 서버 설정
SERVER_IP = "http://127.0.0.1:4444"
MODEL_NAME = "deepseek-coder-v2-lite-instruct"

chat = ChatOpenAI(
    openai_api_base=f"{SERVER_IP}/v1",
    openai_api_key="dummy",
    model=MODEL_NAME,
    temperature=0.7
)

# 프롬프트 설정
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "아주 짧게 말해."),
    ("user", "{user_input}"),
])

# 체인 구성
chain = chat_prompt | chat

# 세션 상태 초기화 (대화 기록 저장)
if "messages" not in st.session_state:
    st.session_state.messages = []  # 대화 로그

# 기존 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기 (엔터로 입력)
query = st.chat_input("💡 질문을 입력하세요:")

if query:
    # 사용자 메시지 기록
    st.session_state.messages.append({"role": "user", "content": query})

    # Streamlit 채팅 UI 업데이트 (사용자 입력)
    with st.chat_message("user"):
        st.markdown(query)

    try:
        # AI 응답 생성
        response = chain.invoke({"user_input": query})

        # 응답 문자열로 변환
        if isinstance(response, dict):
            response_text = response.get("text", "")
        elif hasattr(response, "content"):
            response_text = response.content
        else:
            response_text = str(response)

    except Exception as e:
        response_text = "❌ 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        print(f"❌ [오류] {e}")

    # AI 응답 저장
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    # Streamlit 채팅 UI 업데이트 (AI 응답)
    with st.chat_message("assistant"):
        st.markdown(response_text)

# 대화 초기화 버튼
if st.button("🔄 대화 초기화"):
    st.session_state.messages = []
    st.success("대화가 초기화되었습니다!")

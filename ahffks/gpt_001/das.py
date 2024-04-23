from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
#from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
import openai



os.environ['AZURE_OPENAI_API_KEY'] = 'ddfea391b0014142a4b829ab480a1fd2'
os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://kwanku-openai-001.openai.azure.com/'
os.environ['OPENAI_API_VERSION'] = '2023-05-15'
os.environ['OPENAI_API_TYPE'] = 'azure'


# 실행 코드 uvicorn main:app --reload
app = FastAPI()
# 채팅 기록을 저장할 딕셔너리
chat_history = {"User": {}, "AI": {}}
# 기본 역할 설정
messages = [{"role": "system", "content": "연애코치가 되었습니다."}]
# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. ChatGPT API 설정하기
OPENAI_API_KEY = "나의 api키"
openai.api_key = OPENAI_API_KEY
model = "gpt-3.5-turbo"

class MBTIInput(BaseModel):
    user_type: str
    partner_type: str
    situation_type: str
    Relationship: str

class QuestionInput(BaseModel):
    question: str

@app.post("/mbti_setting")
async def get_mbti_setting(data: MBTIInput):
    partner_type = f"{data.partner_type}".upper()
    user_type = f"{data.user_type}".upper()
    situation_type = f"{data.situation_type}"
    Relationship = f"{data.Relationship}"
    messages.append(
        {
            "role": "user",
            "content": f"""
            partner_type = {partner_type}
            user_type = {user_type}
            situation_type = {situation_type}
            Relationship = {Relationship}
            Please refer to this situation in future questions
            And tell me the exact way you talk as if you're giving advice
            ~ Do it! Say it like this
            When you are asked to write a letter, please write it softly as if you are a couple
            Please answer in Korean. """,
        },
    )
    print(messages)

    return {"answer": "ok"}

@app.get("/mbti_answer")
def get_mbti_answer():
    return {"chat_history": chat_history}

@app.post("/mbti_answer")
async def post_mbti_compatibility(data: QuestionInput):
    user_question = f"{data.question}"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_history["User"][current_time] = user_question

    messages.append(
        {
            "role": "user",
            "content": f"""
            question : {user_question}
            """,
        },
    )
    print(messages)

    # GPT-3 호출과 관련된 코드
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.6,
    )
    answer = response["choices"][0]["message"]["content"]

    # 사용자의 질문과 AI의 응답을 채팅 기록에 추가
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_history["AI"][current_time] = answer
    messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
    print(chat_history)
    return {"chat_history": chat_history}

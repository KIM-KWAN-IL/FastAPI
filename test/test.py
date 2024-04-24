# 필요한 라이브러리를 임포트합니다
import openai
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import os
import json

json_file_path = "./chat_config.json"

# JSON 파일을 읽습니다.
with open(json_file_path, "r") as file:
    chat_config = json.load(file)


os.environ['AZURE_OPENAI_API_KEY'] = chat_config["key"]
os.environ['AZURE_OPENAI_ENDPOINT'] = chat_config["endpoint"]
os.environ['OPENAI_API_VERSION'] = chat_config["version"]
os.environ['OPENAI_API_TYPE'] = chat_config["type"]


from langchain.chat_models import AzureChatOpenAI

from langchain.prompts import(
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.prompts import PromptTemplate, ChatPromptTemplate

chatgpt = AzureChatOpenAI(
     deployment_name = 'gpt-35-turbo-16k',
     max_tokens = 1000
 )


 
app = FastAPI()

#CORS 설정 (HTTP 통신 원활히)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_history = {"User": {}, "AI": {}}

# ChatGPT의 역할을 설정하고 초기 메시지를 만든다
messages = [
    {"role": "system", "content": "너는 심리상담 챗봇이야"}
]




bot_template = '''
너는 심리상담 챗봇이야 아래에 따라서 최대 네문장으로 답변을해줘.
 - 아래

 {아래}
'''

prompt_template = PromptTemplate(
    input_variables = ['아래'],
    template = bot_template
)




system_message_prompt = SystemMessagePromptTemplate.from_template(bot_template)

human_template = '{아래}'
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        human_message_prompt
    ]
)



class QuestionInput(BaseModel):
    question: str





@app.post("/question")
async def post_user_message(data: QuestionInput):
    try:
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

        # GPT-3 호출과 관련된 코드
        answer = chatgpt(chat_prompt.format_prompt(아래=user_question).to_messages())

        # 사용자의 질문과 AI의 응답을 채팅 기록에 추가
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_history["AI"][current_time] = answer
        messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )
        return {"chat_history": answer,
                "time": current_time}
    except Exception as e:
        return {"error": str(e)}


@app.get("/answer")
def get_answer():
    return{"chat_history": chat_history}









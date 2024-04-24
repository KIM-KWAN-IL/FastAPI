# 필요한 라이브러리를 임포트합니다
import openai
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
# OPENAI_API 설정
import sys, os

os.environ['AZURE_OPENAI_API_KEY'] = '**'
os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://kwanku-openai-001.openai.azure.com/'
os.environ['OPENAI_API_VERSION'] = '2023-05-15'
os.environ['OPENAI_API_TYPE'] = 'azure'


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

chat_history = {"User": {}, "AI": {}}

# ChatGPT의 역할을 설정하고 초기 메시지를 만든다
messages = [
    {"role": "system", "content": "너는 심리상담 챗봇이야"}
]




bot_template = '''
너는 심리상담 챗봇이야 아래에 따라서 답변을해줘.
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
        return {"chat_history": chat_history}
    except Exception as e:
        return {"error": str(e)}


@app.get("/answer")
def get_answer():
    return{"chat_history": chat_history}









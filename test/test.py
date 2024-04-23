# 필요한 라이브러리를 임포트합니다
import openai
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import datetime
# OPENAI_API 설정
import sys, os

os.environ['AZURE_OPENAI_API_KEY'] = 'ddfea391b0014142a4b829ab480a1fd2'
os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://kwanku-openai-001.openai.azure.com/'
os.environ['OPENAI_API_VERSION'] = '2023-05-15'
os.environ['OPENAI_API_TYPE'] = 'azure'
from langchain.chat_models import AzureChatOpenAI

chatgpt = AzureChatOpenAI(
     deployment_name = 'gpt-35-turbo-16k',
     max_tokens = 1000
 )
app = FastAPI()
chat_history = {"User": {}, "AI": {}}

# ChatGPT의 역할을 설정하고 초기 메시지를 만듭니다
messages = [
    {"role": "system", "content": "너는 심리상담 챗봇이야"}
]

from langchain.prompts import PromptTemplate, ChatPromptTemplate

# string_prompt = PromptTemplate.from_template('tell me a joke about {subject}')
# string_prompt_value = string_prompt.format_prompt(subject = 'soccer')

# string_prompt_value.text
# chat_prompt = ChatPromptTemplate.from_template('tell me a joke about {subject}')
# chat_prompt_value = chat_prompt.format_prompt(subject = 'soccer')

# chat_prompt_value.messages[0].content


cook_template = '''
너는 심리상담 챗봇이야 아래에 따라서 답변을해줘.
 - 아래

 {아}
'''

prompt_template = PromptTemplate(
    input_variables = ['아'],
    template = cook_template
)

print("input val:" , ['아'])
# result = chatgpt(prompt_template.format(재료 = '감자,쌀,고추장,빵,사과'))
# print(result)

from langchain.prompts import(
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.schema import SystemMessage, HumanMessage, AIMessage

system_message_prompt = SystemMessagePromptTemplate.from_template(cook_template)

human_template = '{아}'
print("*****: ", human_template)
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        human_message_prompt
    ]
)



class QuestionInput(BaseModel):
    question: str










@app.post("/ehlfk")
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
    answer = chatgpt(chat_prompt.format_prompt(아=user_question).to_messages())
    #answer = response["choices"][0]["message"]["content"]

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


@app.get("/answer")
def get_answer():
    return{"chat_history": chat_history}








# while True:
#     # 사용자로부터 질문을 받습니다
#     q = input("질문: ")
#     query = f"Q: {q}"

#     # 질문을 메시지 배열에 추가합니다
#     messages.append({"role": "user", "content": query})

#     # ChatGPT API를 호출하고 응답을 받습니다
#     print("답변을 준비중입니다...")
    

#     answer = chatgpt(chat_prompt.format_prompt(아=q).to_messages())

#     # 응답을 출력합니다
#     print("========================================")
#     print(answer)
#     print("========================================")

#     # 챗봇의 응답을 메시지 배열에 추가합니다
#     messages.append({"role": "assistant", "content": answer})

#     # 사용자가 더 질문하고 싶은지 확인합니다
#     while True:
#         q = input("더 질문 하실건가요(y/n): ").lower()
#         if q in ["y", "n", "ㅛ", "ㅜ"]:
#             break
#         else:
#             print("유효한 입력이 아닙니다. 다시 입력해주세요.")

#     if q in ["n", "ㅜ"]:
#         print("종료합니다.")
#         break
import os
import openai


os.environ['AZURE_OPENAI_API_KEY'] = 'ddfea391b0014142a4b829ab480a1fd2'
os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://kwanku-openai-001.openai.azure.com/'
os.environ['OPENAI_API_VERSION'] = '2023-05-15'
os.environ['OPENAI_API_TYPE'] = 'azure'

# from langchain.llms import AzureOpenAI

# gpt = AzureOpenAI(
#     deployment_name = 'dev-davinci-002',
#     max_tokens = 1000
# )

from langchain.chat_models import AzureChatOpenAI

chatgpt = AzureChatOpenAI(
     deployment_name = 'gpt-35-turbo-16k',
     max_tokens = 1000
 )

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



    
while True:
    print("-" * 30)

    user_input = input("user input: ")
    if user_input.lower() == "exit":
        break

    result = chatgpt(chat_prompt.format_prompt(아=user_input).to_messages())
    print({user_input})
    print(f"bot_resp: {result.content}")




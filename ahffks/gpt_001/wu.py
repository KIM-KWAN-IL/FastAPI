import os 
import openai 
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.prompts import(
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.schema import SystemMessage, HumanMessage, AIMessage

os.environ['AZURE_OPENAI_API_KEY'] = 'aacf85de404249ae865bb3c69d51f77d'
os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://kwanku-openai-001.openai.azure.com/'
os.environ['OPENAI_API_VERSION'] = '2023-05-15'
os.environ['OPENAI_API_TYPE'] = 'azure'

from langchain.chat_models import AzureChatOpenAI

chatgpt = AzureChatOpenAI(
     deployment_name = 'gpt-35-turbo-16k',
     max_tokens = 1000
 )


def ask(text): 
    
    user_input = {"role": "user", "content": text} 
    messages.append(user_input) 
    
    result = chatgpt(chat_prompt.format_prompt(text).to_messages())

    #response = openai.ChatCompletion.create( 
    #  model="gpt-3.5-turbo", 
    #  messages=messages) 
    
    bot_text= result.content
    bot_resp = {"role": "assistant", "content": bot_text} 
    messages.append(bot_resp) 
    return bot_text 

# Load your API key from an environment variable or secret management service 
openai.api_key = "여기에 발급받은 api key를 넣어주세요:)" 

system_instruction = '''
너는 심리상담 챗봇이야 아래에 따라서 답변을해줘.
 - 아래

 {아}
'''

prompt_template = PromptTemplate(
    input_variables = ['아'],
    template = system_instruction
)

system_message_prompt = SystemMessagePromptTemplate.from_template(system_instruction)


human_template = '{아}'
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        system_message_prompt,
        human_message_prompt
    ]
)






messages = [{"role": "system", "content": system_instruction}] 

while True: 
    user_input = input("user input: ") 
    bot_resp = ask(user_input) 
    
    print("-"*30) 
    print(f"user_input: {user_input}") 
    print(f"bot_resp: {bot_resp}")
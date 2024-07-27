from dotenv import load_dotenv
import os
import anthropic 
from halo import Halo 
import pprint
from langchain.memory import ConversationBufferMemory 
from langchain.schema import HumanMessage,AIMessage 

load_dotenv()

pp=pprint.PrettyPrinter(indent=4)

memory=ConversationBufferMemory(return_messages=True)


def generate_function(user_input):
    spinner=Halo(text='Loading...',spinner='dots')
    spinner.start()

    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))

    conversation_history=memory.chat_memory.messages
    messsages=[]

    for message in messsages:
        if isinstance(message,HumanMessage):
            messsages.append({"role":"user","content":"message.content"})
        elif isinstance(message,AIMessage):
            messsages.append({"role":"assistant","content":"message.content"})

    messsages.append({"role":"user","content":user_input})

    response=client.messages.create(
        model=os.getenv("MODEL_NAME"),
        max_tokens=500,
        temperature=0,
        system="Respond in short and clear sentences.",
        messages=messsages
    )
    spinner.stop()

    print("Request: ")
    pp.pprint(user_input)
    print("Response: ")
    pp.pprint(response.content)

    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_user_message(response.content)
def main():
    while True:
        input_text=input("You: ")
        if input_text.lower()=="quit":
            break
        response=generate_function(input_text)
        print(f"Claude: {response}")

if __name__=="__main__":
    main()
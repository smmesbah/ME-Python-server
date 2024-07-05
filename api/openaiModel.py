from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_chat_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
        (
            "You are a helpful assistant. You have tasks informations from database. Answer the question with the tasks informations. If you can't find the answer, you answer with I don't know"
        ),
        (
            """Tasks Informations: 
                    {search_result}
     Question: {question}
     """
        )
        ]
    )
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

prompt = get_chat_prompt_template()
chain = prompt | llm

print(chain.invoke({
    "search_result": """Task infromation: {"user_id":"asdfg","taskTitle":"Change prompt for llm","taskColor":"#D2CCF2","startDate":"Sun Jul 07 2024","endDate":"Sun Jul 07 2024","startTime":"","endTime":"","reminderTime":"","taskType":"","tag":"","label":"In Progress","progress":0,"priority":"Low","redirectURL":"/"}
        score: 0.9280843734741211""",
    "question": "When does the task 'Change prompt for llm' start?"
}))
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from bson import ObjectId
# import sys
# sys.path.append("..")
from config.database import collection_todos

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

chat = ""

def get_chat_response():
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Catch if it's about create, update or delete a task"
            },  

        {
            "role": "user",
            "content": """
            Create a task called 'Kill Mesbah' and add it to my to-do list.
            Answer with: 
            Task Name: task name
            Start Date: start date
            Start Time: start date

            Created/updated/deleted a task
            """
        }
        ],
        model= "gpt-3.5-turbo-0125", # "gpt-3.5-turbo-0125
        temperature=0,
        # stream=True
    )
    chat = chat_completion.choices[0].message.content
    print(chat)
    # for chunk in chat_completion:
    #     print(chunk.choices[0].delta.content or "", end="")
    #     chat.append(chunk.choices[0].delta.content or "")
    
    if "created" in chat.lower(): 
        try: 
            task_name_match = re.search(r"Task Name: (.*?)\n", chat)
            start_date_match = re.search(r"Start Date: (.*?)\n", chat)
            start_time_match = re.search(r"Start Time: (.*?)\n", chat)

            # print(task_name_match.group(1), start_date_match, start_time_match)
            # print(task_name_match.group(1).strip() if task_name_match else "Not specified")
            
            task_name = task_name_match.group(1) if task_name_match else "Not specified"
            start_date = start_date_match.group(1) if start_date_match else "Not specified"
            start_time = start_time_match.group(1) if start_time_match else "Not specified"
            
            collection_todos.insert_one({
                "user_id": "asdfg",
                "taskTitle": task_name,
                "taskColor": "#D2CCF2",
                "startDate": "Mon Jul 15 2024",
                "endDate": "Mon Jul 15 2024",
                "startTime": "",
                "endTime": "",
                "reminderTime": "",
                "taskType": "",
                "tag": "",
                "label": "To Do",
                "redirectURL": "/",
                "progress": 0,
                "priority": "Low"
    })
        except:
            print("Error in parsing the response")
    
    elif "updated" in chat.lower():
        try: 
            task_name_match = re.search(r"Task Name: (.*?)\n", chat)
            start_date_match = re.search(r"Start Date: (.*?)\n", chat)
            start_time_match = re.search(r"Start Time: (.*?)\n", chat)

            # print(task_name_match.group(1), start_date_match, start_time_match)
            # print(task_name_match.group(1).strip() if task_name_match else "Not specified")
            
            task_name = task_name_match.group(1) if task_name_match else "Not specified"
            start_date = start_date_match.group(1) if start_date_match else "Not specified"
            start_time = start_time_match.group(1) if start_time_match else "Not specified"
            
            collection_todos.update_one({"_id": ObjectId(id)}, {"$set": {
                "user_id": "asdfg",
                "taskTitle": task_name,
                "taskColor": "#D2CCF2",
                "startDate": "Mon Jul 15 2024",
                "endDate": "Mon Jul 15 2024",
                "startTime": "",
                "endTime": "",
                "reminderTime": "",
                "taskType": "",
                "tag": "",
                "label": "To Do",
                "redirectURL": "/",
                "progress": 0,
                "priority": "Low"
    }})
        except:
            print("Error in parsing the response")
    
get_chat_response()


# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "What is the capital of the United States?"
#         }
#     ],
#     model = "gpt-3.5-turbo-0125",
#     temperature=0,
#     stream=True
# )

# for chunk in chat_completion:
#     print(chunk.choices[0].delta.content or "", end="")
#     return chunk.choices[0].delta.content or ""
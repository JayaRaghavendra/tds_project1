# import json
# import re
# from app.llm_utils import agent_and_email_model
# from langchain.prompts import PromptTemplate

# from app.phase_a_tasks import *
# from app.llm_utils import *
# from app.function_description import *
# from agent import *

# img_path = "images_test_data/image3.jpg"
# with open(img_path, 'rb') as file:
#     image_base64 = base64.b64encode(file.read()).decode('utf-8')

# # detect the image type
# image_type = os.path.splitext(img_path)[1].lower().replace('.', '')

# # get the model for extracting numbers from the image
# response_json = image_extraction_model_response(image_base64, image_type)
# text = response_json['content']
# numbers = re.findall(r'\d{4}', text)
# print("".join(numbers))

# ============================================================================================================

# email_file = "emails_test_data/email.txt"

# with open(email_file, 'r') as file:
#         email_contents = file.read()
    
# # get the model for extracting the sender's email from the email contents
# email_extract_model = llm_utils.agent_and_email_model()

# # Create the prompt template
# prompt = PromptTemplate(
#     input_variables=["email_content"],
#     template="Extract the sender's email address from the following email content:\n\n{email_content}"
# ).format(email_content=email_contents)

# # Call the model to extract the sender's email from the email contents
# response = email_extract_model.invoke(prompt)
# output = json.loads(response.json())
# text = output['content']
# # email username - can have letters, numbers and (.,_,%,+,-), CANNOT start/end with ".", cannot have ".." and can't hav eother symbols
# # domain name - can have letters, numbers and (-), CANNOT start/end with "-", cannot have "--"
# # domain extension - can have letters only, CANNOT start/end with "."
# email = re.search(r'[^\s]+@[^\s]+.[^\s]{2,}', text, re.IGNORECASE)
# if email:
#     email = email.group(0)
#     print(email)

# ============================================================================================================
# import sqlite3 

# conn = sqlite3.connect("tickets.db")
# cursor = conn.cursor()

# cursor.execute("CREATE TABLE IF NOT EXISTS tickets (type TEXT COLLATE NOCASE, units INTEGER, price REAL)")

# data = [
#     ("Silver", 38, 1.47),
#     ("SILVER", 562, 1.98),
#     ("Silver", 541, 1.74),
#     ("bronze", 224, 0.95),
#     ("BRONZE", 493, 1.82),
# ]

# cursor.executemany("INSERT INTO tickets (type, units, price) VALUES (?, ?, ?)", data)
# conn.commit()
# conn.close()

# ============================================================================================================

# input_str = "/data/contents.log में कितने रविवार हैं? गिनो और /data/contents.dates में लिखो"
# # input_str = "/data/contents.logல எத்தனை ஞாயிறு இருக்குனு கணக்கு போட்டு, அதை /data/contents.datesல எழுது"
# input_str = "The file /data/dates.txt contains a list of dates, one per line. Count the number of Wednesdays in the list, and write just the number to /data/dates-wednesdays.txt"
# # input_str = "The file /data/dates.txt contains a list of dates, one per line. Delete this file"
# prompt = PromptTemplate(template="Translate the input string into english if it is not english. Input string: {input_string}. Return only the translated text.")
# final_prompt = prompt.format(input_string=input_str)
# chat_model = agent_and_email_model()
# response = chat_model.invoke(final_prompt)
# output = json.loads(response.json())
# task_description = output['content']
# print(task_description)

# function_call_prompt = PromptTemplate(template="You have access to the following functions. '''json {functions}'''. \
#                                       Based on input string: {input_string}, extract the arguments and call the right function. \
#                                       If needed, call multiple functions in the order of their execution. Return function and arguments. \
#                                       If the task asks for removal or deletion of any file, return null in function call.")
# final_func_call_prompt = function_call_prompt.format(functions=phase_a_tools,input_string=task_description)
# func_call_response = chat_model.invoke(final_func_call_prompt)
# output = json.loads(func_call_response.json())
# final_text = output['content']
# print(final_text)

# # Extract the JSON part from the text
# json_match = re.search(r'```json(.*?)```', final_text, re.DOTALL)
# if json_match:
#     json_str = json_match.group(1).strip()
#     function_call_details = json.loads(json_str)
#     func = globals()[function_call_details['function']]
#     print(func(**function_call_details['arguments']))
# else:
#     print("No JSON found in the text.")

# ============================================================================================================

# input_str = "/data/contents.log में कितने रविवार हैं? गिनो और /data/contents.dates में लिखो"
# input_str = "/data/contents.logல எத்தனை ஞாயிறு இருக்குனு கணக்கு போட்டு, அதை /data/contents.datesல எழுது"
# input_str = "The file /data/dates.txt contains a list of dates, one per line. Count the number of Wednesdays in the list, and write just the number to /data/dates-wednesdays.txt"
# input_str = "The file /data/dates.txt contains a list of dates, one per line. Delete this file"

# print(agent(input_str))
# "/data/logs/sample2.log में कितने रविवार हैं? गिनो और /data/logs/date-sundays.txt में लिखो"
# ============================================================================================================

# import requests

# url = "http://127.0.0.1:8000/run?task=/test_data/logs/sample2.log में कितने रविवार हैं? गिनो और /test_data/logs/date-sundays.txt में लिखो"  # Example: httpbin.org echoes back the request
# data = {"key1": "value1", "key2": "value2"}  # Data to send in the POST request

# try:
#     response = requests.post(url)  # Use json=data for JSON payload
#     # Or, for form data: response = requests.post(url, data=data)

#     response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

#     print("Status Code:", response.status_code)
#     print("Response Content:", response.json())  # If the response is JSON
#     # Or print("Response Content:", response.text) for other content types

# except requests.exceptions.RequestException as e:
#     print(f"Error: {e}")

# ============================================================================================================
# import requests
# import json

# api_url = "https://catfact.ninja/fact/"
# output_file_path = "test_data/api_data.json"

# response = requests.get(api_url, verify=False)

# if response.status_code == 200:  # Check for successful response
#     print(response.json())  # Or response.text if it's not JSON
#     try:
#         with open(output_file_path, "w") as f:
#             json.dump(response.json(), f, indent=4)  # Write JSON to file
#         print(f"Data saved to {output_file_path}")
#     except Exception as e:
#         print(f"Error saving to file: {e}")

# elif response.status_code == 404:
#     print(f"Error: Not Found - {api_url}")
# elif response.status_code == 500:
#     print(f"Error: Server Error - {api_url}")
# else:
#     print(f"Error: {response.status_code} - {api_url}")

# ============================================================================================================
# import requests
# import subprocess
# import os

# # Install uv if required
# subprocess.run(["pip", "install", "uv"])

# url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
# response = requests.get(url)

# if response.status_code == 200:
#     with open("datagen.py", "wb") as file:
#         file.write(response.content)
    
#     if os.name == 'nt':  # Check if the OS is Windows
#         subprocess.run(["cmd", "/c", "python datagen.py ${user.email}"])
#     else:
#         subprocess.run(["python", "datagen.py", "${user.email}"])
# else:
#     print(f"Failed to download the script. Status code: {response.status_code}")
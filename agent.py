import logging
from app.phase_a_tasks import *
from app.phase_b_tasks import *
from app.filter_csv import *
from app.llm_utils import *
from app.function_description import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

DATA_DIR = "data"
def is_safe(path):
    if path.startswith('/'):
        path = path.strip('/')
    return path.startswith(DATA_DIR)

def agent(input_str,tools):
    logging.info(f"Initial task: {input_str}")
    prompt = PromptTemplate(template="Translate the input string into english if it is not english, else return it as it is. Input string: {input_string}.")
    final_prompt = prompt.format(input_string=input_str)
    chat_model = agent_and_email_model()
    response = chat_model.invoke(final_prompt)
    output = json.loads(response.json())
    task_description = output['content']
    logging.info(f"After translation if needed: {task_description} ")
    
    # Analyse the task description and for valid task extract arguments and call right function

    function_call_prompt = PromptTemplate(template="You have access to the following functions. '''json {functions}'''. \
                                      Based on input string: {input_string}, extract the arguments and call the right function. \
                                      If needed, call multiple functions in the order of their execution. Return function and arguments \
                                        in json format with keys 'function' and 'parameters'. \
                                      If the task asks for removal or deletion of any file, return string 'null' in json")
    final_func_call_prompt = function_call_prompt.format(functions=tools,input_string=task_description)
    func_call_response = chat_model.invoke(final_func_call_prompt)
    output = json.loads(func_call_response.json())
    final_text = output['content']
    logging.info(f"Final formatted task description: {final_text}")

    # Extract the JSON part from the text
    json_match = re.search(r'```json(.*?)```', final_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()
        if json_str=="null":
            return 1 # 400 bad request, deletion/removal of file
        else:
            try:
                function_call_details = json.loads(json_str)
                logging.info(f"Function details loaded: {function_call_details}")
                if function_call_details['function'] == "data_generation":
                    func = globals()[function_call_details['function']]
                    if function_call_details['parameters']['output_path'] == ".":
                        _ = func(function_call_details['parameters']['script_url'])
                    else:
                        _ = func(**function_call_details['parameters'])
                    return function_call_details
                for arg_name, arg_val in function_call_details['parameters'].items():
                    if ("dir" in arg_name) or ("path" in arg_name):
                        if not is_safe(arg_val):
                            return 2 # 400 bad request, access restricted, invalie input/output path
                func = globals()[function_call_details['function']]
                logging.info(f"Executing: {func}")
                _ = func(**function_call_details['parameters'])
                return {func:function_call_details['parameters']}
            except Exception as e:
                return 4 # 500 Internal server error, error in function call
    else:
        return 5 # 400 bad request unknow task request
    
app = FastAPI()

# Add CORS middleware to allow requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class InputData(BaseModel):
    input_str: str

@app.post("/run")
async def agent_post_endpoint(task: str):
    if not task:
        raise HTTPException(status_code=400, detail="No task description provided")
    
    result = agent(task, task_tools)
    if result == 1:
        logging.info("Bad request, Files cannot be deleted")
        raise HTTPException(status_code=400, detail="Bad request, Files cannot be deleted")
    elif result == 2:
        logging.info("Bad request, access restricted for the input/output path")
        raise HTTPException(status_code=400, detail="Bad request, access restricted for the input/output path")
    elif isinstance(result,dict):
        logging.info("Task executed successfully")
        return JSONResponse(content={"detail": "Task executed successfully"}, status_code=200)
    elif result == 4:
        logging.info("Internal server error, could not complete the task")
        raise HTTPException(status_code=500, detail="Internal server error, could not complete the task")
    else:
        logging.info("unknown task description/description not clear")
        raise HTTPException(status_code=400, detail="Bad request, unknown task description/description not clear")

@app.get("/read")
async def get_file_details(path: str):
    try:
        with open(path, 'r') as file:
            content = file.read()
        logging.info("File read succesfully")
        return JSONResponse(content={'file_content': content}, status_code=200)
    except FileNotFoundError:
        logging.info("File not found")
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/run")
async def run_agent_with_filter(task: str):
    if not task:
        raise HTTPException(status_code=400, detail="No task description provided")

    result = agent(task, filter_csv_tool)
    if result == 1:
        logging.info("Bad request, Files cannot be deleted")
        raise HTTPException(status_code=400, detail="Bad request, Files cannot be deleted")
    elif result == 2:
        logging.info("Bad request, access restricted for the input/output path")
        raise HTTPException(status_code=400, detail="Bad request, access restricted for the input/output path")
    elif isinstance(result,dict):
        logging.info("Task executed successfully")
        func, args = list(result.items())[0]
        return func(**args)
    elif result == 4:
        logging.info("Internal server error, could not complete the task")
        raise HTTPException(status_code=500, detail="Internal server error, could not complete the task")
    else:
        logging.info("unknown task description/description not clear")
        raise HTTPException(status_code=400, detail="Bad request, unknown task description/description not clear")
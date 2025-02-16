import base64
import os
import shutil
import subprocess
import json
import re
from langchain.prompts import PromptTemplate
import sklearn
import urllib
from . import llm_utils
import sqlite3
import numpy as np
import pandas as pd
from dateutil import parser
import os, subprocess, urllib.request, sys
import logging

def data_generation(script_url, output_path = os.getcwd()):
    logging.info("Starting data generation...")

    # Convert output_path to absolute path
    output_path = os.path.abspath(output_path)
    data_folder = os.path.join(output_path, "data")

    # Overwrite existing data folder
    if os.path.exists(data_folder):
        logging.info(f"Removing existing data folder: {data_folder}")
        # subprocess.run(["rm", "-rf", data_folder], check=True, shell=True)  # Unix/macOS
        subprocess.run(["rmdir", "/s", "/q", data_folder], shell=True) # Windows

    os.makedirs(data_folder, exist_ok=True)  # Create the folder
    logging.info(f"Created fresh data folder at: {data_folder}")

    # Run datagen.py directly from URL
    email = "daniel.putta@gramener.com.com"  # Modify as needed
    project_root = os.getcwd()
    python_executable = os.path.join(project_root, ".venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join(project_root, ".venv", "bin", "python")

    if not os.path.exists(python_executable):
        logging.error("Python virtual environment not found! Ensure that .venv exists and is set up properly.")
        return

    # Run the script directly from the URL using the venv Python
    subprocess.run([
        python_executable, "-c",
        f"import urllib.request; exec(urllib.request.urlopen('{script_url}').read())",
        email, "--root", data_folder
    ], check=True)

    logging.info("Data generation complete.")


def format_markdown_file(file_path):
    if file_path.startswith('/'):
        file_path = file_path.strip('/')
    # check if the file exists
    if os.path.exists(file_path):
        # format the file using prettier
        try:
            if os.name == 'nt':  # for Windows
                subprocess.run(['cmd', 'npx', 'prettier@3.4.2', '--write', file_path], capture_output=True, text=True)
            else:  # for Unix-based systems
                subprocess.run(['npx', 'prettier@3.4.2', '--write', file_path], capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Prettier formatting failed: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    else:
        return False

def count_specific_days(file_path, day_of_week, output_file_path):
    if file_path.startswith('/'):
        file_path = file_path.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    # check if the file exists
    if os.path.exists(file_path):
        # read the file and count the specific days
        with open(file_path, 'r') as file:
            dates_data = file.readlines()
            # extract and convert the dates to datetime objects using dateutil parser
            dates = [parser.parse(date.strip()) for date in dates_data]
            # map day names to weekday numbers
            days_map = {'monday': 0,'tuesday': 1,'wednesday': 2,'thursday': 3,'friday': 4,'saturday': 5,'sunday': 6}
            # get the weekday number for the specific day
            day_number = days_map.get(day_of_week.lower())
            if day_number is None:
                print(f"Invalid day of week: {day_of_week}")
                return None
            # count the specific days
            count = len([date for date in dates if date.weekday() == day_number])
            
            # write the count to the output file
            with open(output_file_path, 'w') as new_file:
                new_file.write(str(count))
            return True
    
    return False

# define function to read contacts from a .json file and write the sorted contacts to a new json file
def sort_contacts(file_path, output_file_path):
    if file_path.startswith('/'):
        file_path = file_path.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    # check if the file exists
    if os.path.exists(file_path):
        # read the contacts from the file
        with open(file_path, 'r') as file:
            contacts = json.load(file)
            # sort the contacts by last_name then first_name
            sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
            # write the sorted contacts to the output file
            with open(output_file_path, 'w') as new_file:
                json.dump(sorted_contacts, new_file, indent=4)
            return True
    
    return False

# define function to select N most recent .log files and read the first line of each file and write these N lines to a new file
def read_log_files(log_dir, n, output_file_path):
    if log_dir.startswith('/'):
        log_dir = log_dir.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    # get all the .log files in the directory
    log_files = [os.path.join(root, file)
                 for root, _, files in os.walk(log_dir)
                 for file in files if file.endswith('.log')]
    
    # check if there are no log files
    if not log_files:
        print("No log files found in the directory.")
        return False
    
    # sort the files by modification time
    log_files = sorted(log_files, key=lambda x: os.path.getmtime(x), reverse=True)
    # get the first N files
    log_files = log_files[:n]
    # read the first line of each file
    first_lines = []
    for log_file in log_files:
        with open(log_file, 'r') as file:
            first_line = file.readline()
            first_lines.append(first_line)
    # write the first lines to the output file
    with open(output_file_path, 'w') as new_file:
        new_file.writelines(first_lines)
    return True

# define function to read all markdown files and extract the first line with "h1" heading and store all these extracted line into a new file
def extract_h1_headings(markdown_dir, output_file_path):
    if markdown_dir.startswith('/'):
        markdown_dir = markdown_dir.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    # get all the .md files in the directory
    markdown_files = [os.path.join(root, file)
                  for root, _, files in os.walk(markdown_dir)
                  for file in files if file.endswith(".md")]
    
    # check if there are no markdown files
    if not markdown_files:
        print("No markdown files found in the directory.")
        return False
    
    # read the first line with "h1" heading from each file
    extracted_headings = {}
    for markdown_file in markdown_files:
        with open(markdown_file, 'r') as file:
            for line in file:
                if re.match(r'^# .+', line):
                    extracted_headings[markdown_file] = line.strip()
                    break
    # write the extracted headings to the output file
    with open(output_file_path, 'w') as new_file:
        json.dump(extracted_headings, new_file, indent=4)
    return True

# function to extract sender's email from email contents in a .txt file and write to another file with just the sender's email
def extract_email_sender(file_path, output_file_path):
    if file_path.startswith('/'):
        file_path = file_path.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    # check if the file exists
    if os.path.exists(file_path):
        # read the email contents from the file
        with open(file_path, 'r') as file:
            email_contents = file.read()
        
        # get the model for extracting the sender's email from the email contents
        email_extract_model = llm_utils.agent_and_email_model()

        # Create the prompt template
        prompt = PromptTemplate(
            input_variables=["email_content"],
            template="Extract the sender's email address from the following email content:\n\n{email_content}"
        ).format(email_content=email_contents)

        # Call the model to extract the sender's email from the email contents
        response = email_extract_model.invoke(prompt)     
        output = json.loads(response.json())
        text = output['content']
        # email username - can have letters, numbers and (.,_,%,+,-), CANNOT start/end with ".", cannot have ".." and can't hav eother symbols
        # domain name - can have letters, numbers and (-), CANNOT start/end with "-", cannot have "--"
        # domain extension - can have letters only, CANNOT start/end with "."
        email = re.search(r'[^\s]+@[^\s]+.[^\s]{2,}', text, re.IGNORECASE) 
        if email:
            # write the sender's email to the output file
            with open(output_file_path, 'w') as new_file:
                new_file.write(email.group(0))
        
            return True
        else:
            with open(output_file_path, 'w') as new_file:
                new_file.write("No email found")
        
            return True
    
    return False

# function to get a model for extracting numbers from an image and write to a .txt file
def extract_numbers_from_image(image_path, output_file_path):
    if image_path.startswith('/'):
        image_path = image_path.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    # check if the file exists
    if os.path.exists(image_path):
        # read the image file
        with open(image_path, 'rb') as file:
            image_base64 = base64.b64encode(file.read()).decode('utf-8')
        
        # detect the image type
        image_type = os.path.splitext(image_path)[1].lower().replace('.', '')
        
        # get the model for extracting numbers from the image
        response_json = llm_utils.image_extraction_model_response(image_base64, image_type)
        content = response_json['content']

        # regex to keep only numbers
        numbers = re.findall(r'\d{3,6}', content)
        # keep only the first 16 digits
        if numbers:
            card_number = "".join(numbers)
        else:
            return False
        
        # write the numbers to the output file
        with open(output_file_path, 'w') as new_file:
            new_file.write(card_number)
        
        return True
    
    return False

# function to read txt sentences from txt file and find the most similar comments using embedding
def find_similar_comments(file_path, output_file_path):
    if file_path.startswith('/'):
        file_path = file_path.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    # check if the file exists
    if os.path.exists(file_path):
        # read the sentences from the file
        with open(file_path, 'r') as file:
            sentences = file.readlines()
        
        # get the embeddings for each sentence using functions in llm_utils
        sentence_embeddings = llm_utils.get_embeddings(sentences)
        # convert embeddings to numpy arrays, calculate the similarity matrix, get the most similar comments
        converted_embeddings = np.array(sentence_embeddings)
        similarity_matrix = sklearn.metrics.pairwise.cosine_similarity(converted_embeddings)
        np.fill_diagonal(similarity_matrix, -1)

        most_similar_index = np.argmax(similarity_matrix)
        most_similar_comments = [sentences[most_similar_index//len(sentences[0])], sentences[most_similar_index%len(sentences[0])]]

        # write the most similar comments to the output file
        with open(output_file_path, 'w') as new_file:
            new_file.writelines(most_similar_comments)
        
        return True
    
    return False

# function to read the .db file, perform queries and write the results to a new .txt file
def read_db_file(db_file_path, output_file_path, query=None):
    if db_file_path.startswith('/'):
        db_file_path = db_file_path.strip('/')
    if output_file_path.startswith('/'):
        output_file_path = output_file_path.strip('/')
    # check if the file exists
    if os.path.exists(db_file_path):
        # connect to the database
        conn = sqlite3.connect(db_file_path)
        # get the cursor
        cursor = conn.cursor()
        try:
            # if no query is provided, use the default query
            if query is None:
                return False
            # execute the provided query
            cursor.execute(query)
            # fetch the results
            results = cursor.fetchall()
            # write the results to the output file
            with open(output_file_path, 'w') as file:
                for row in results:
                    file.write(f"{row}\n")
            return True
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False
        finally:
            conn.close()
    return False
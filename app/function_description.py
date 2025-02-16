task_tools = [
    {
        "type": "function",
        "function": {
            "name": "data_generation",
            "description": "Generate data using the script url",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_url": {
                        "type": "string",
                        "description": "URL of the script to be downloaded and executed."
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where the generated data should be saved. Current directory is os.getcwd()"
                    }
                },
                "required": ["script_url", "output_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
    ,
    {
        "type": "function",
        "function": {
            "name": "format_markdown_file",
            "description": "Format the contents of markdown using prettier, updating the file in-place",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "filepath for markdown file"
                    }
                },
                "required": ["file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_specific_days",
            "description": "Count the number of occurrences of a specific day of the week in a file containing dates and write the count to a new file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "filepath for the file containing dates"
                    },
                    "day_of_week": {
                        "type": "string",
                        "description": "day of the week to count (e.g., 'monday', 'tuesday')"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "filepath for the output file to write the count"
                    }
                },
                "required": ["file_path", "day_of_week", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sort_contacts",
            "description": "Read contacts from a .json file, sort them by last name and first name, and write the sorted contacts to a new file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "filepath for the .json file containing contacts"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "filepath for the output file to write the sorted contacts"
                    }
                },
                "required": ["file_path", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_log_files",
            "description": "Select N most recent .log files, read the first line of each file, and write these N lines to a new file",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_dir": {
                        "type": "string",
                        "description": "Directory containing the .log files"
                    },
                    "n": {
                        "type": "integer",
                        "description": "Number of most recent .log files to read"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "filepath for the output file to write the first lines"
                    }
                },
                "required": ["log_dir", "n", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_h1_headings",
            "description": "Read all markdown files in a directory, extract the first line with an h1 heading, and store these extracted lines into a new file",
            "parameters": {
                "type": "object",
                "properties": {
                    "markdown_dir": {
                        "type": "string",
                        "description": "Directory containing the markdown files"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "filepath for the output file to write the extracted headings"
                    }
                },
                "required": ["markdown_dir", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_email_sender",
            "description": "Extract the sender's email address from email contents in a .txt file and write to another file with just the sender's email",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the .txt file containing the email contents"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "filepath for the output file to write the sender's email"
                    }
                },
                "required": ["file_path", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_numbers_from_image",
            "description": "Extract numbers from an image and write to a .txt file",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the image file"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "filepath for the output file to write the extracted numbers"
                    }
                },
                "required": ["image_path", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_similar_comments",
            "description": "Read sentences from a .txt file and find the most similar comments using embeddings",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the .txt file containing the sentences"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "filepath for the output file to write the most similar comments"
                    }
                },
                "required": ["file_path", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_db_file",
            "description": "Read the .db file, perform queries and write the results to a new .txt file",
            "parameters": {
                "type": "object",
                "properties": {
                    "db_file_path": {
                        "type": "string",
                        "description": "Path to the .db file"
                    },
                    "query": {
                        "type": "string",
                        "description": "SQL query to execute on the database"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "filepath for the output file to write the query results"
                    }
                },
                "required": ["db_file_path", "query", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
        {
        "type": "function",
        "function": {
            "name": "fetch_and_save_data",
            "description": "Fetch data from an API and save it to a JSON file",
            "parameters": {
                "type": "object",
                "properties": {
                    "api_url": {
                        "type": "string",
                        "description": "URL of the API to fetch data from"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "Filepath for the output JSON file"
                    }
                },
                "required": ["api_url", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clone_and_commit",
            "description": "Clone a git repository, optionally modify a file, and commit the changes",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {
                        "type": "string",
                        "description": "URL of the git repository to clone"
                    },
                    "clone_to_path": {
                        "type": "string",
                        "description": "Path to clone the repository to"
                    },
                    "commit_message": {
                        "type": "string",
                        "description": "Commit message for the changes"
                    },
                    "file_to_modify": {
                        "type": "string",
                        "description": "File to modify in the repository",
                        "nullable": True
                    },
                    "modification_content": {
                        "type": "string",
                        "description": "Content to write to the file being modified",
                        "nullable": True
                    }
                },
                "required": ["repo_url", "clone_to_path", "commit_message"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_web_data",
            "description": "Extract a table from a webpage and save it to a CSV file",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the webpage containing the table"
                    },
                    "table_index": {
                        "type": "integer",
                        "description": "Index of the table to extract (default is 1)"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "Filepath for the output CSV file"
                    }
                },
                "required": ["url", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compress_image",
            "description": "Compress an image and save it to a new file",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_path": {
                        "type": "string",
                        "description": "Filepath of the input image"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Filepath for the compressed image"
                    },
                    "quality": {
                        "type": "integer",
                        "description": "Quality of the compressed image (default is 85)"
                    }
                },
                "required": ["input_path", "output_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "markdown_to_html",
            "description": "Convert a markdown file to HTML and save it to a new file",
            "parameters": {
                "type": "object",
                "properties": {
                    "markdown_file_path": {
                        "type": "string",
                        "description": "Filepath of the input markdown file"
                    },
                    "output_file_path": {
                        "type": "string",
                        "description": "Filepath for the output HTML file"
                    }
                },
                "required": ["markdown_file_path", "output_file_path"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]
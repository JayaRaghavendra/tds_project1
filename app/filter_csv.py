import os
import pandas as pd

filter_csv_tool = [{
    "type": "function",
    "function": {
        "name": "filter_csv",
        "description": "Filter a CSV file based on a column value and return the filtered rows as JSON",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath of the input CSV file"
                },
                "column": {
                    "type": "string",
                    "description": "The column name to filter on"
                },
                "value": {
                    "type": "string",
                    "description": "The value to filter by"
                }
            },
            "required": ["file_path", "column", "value"],
            "additionalProperties": False
        },
        "strict": True
    }
}
]

def filter_csv(file_path, column, value):
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            return False
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Check if the column exists in the DataFrame
        if column not in df.columns:
            return False
        
        # Filter the DataFrame
        filtered_df = df[df[column] == value]
        
        # Convert the filtered DataFrame to JSON
        result = filtered_df.to_json(orient="records")
        return result
    except:
        return False
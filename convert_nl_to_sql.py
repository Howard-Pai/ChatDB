from typing import Tuple, Union
import os
import warnings  # suppress PDF cropbox warnings
warnings.filterwarnings("ignore", message="CropBox missing")

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import json


def convert(NL_query: str) -> Tuple[str, str, str]:
    """
    Convert a natural language query to a SQL or NoSQL command.

    Args:
        NL_query (str): The natural language query.

    Returns:
        Tuple[str, str, str]: A tuple containing the database type ("SQL" or "NoSQL"),
                              the database name, and the command in JSON format.
    """
    # The return value is a tuple (db_type, database_name, command), where db_type is either "SQL" or "NoSQL", database_name should be the name of the database used and command is a JSON-formatted string.
    # If the command is a SQL command, it should specify the operation to be performed. Operaitons include: show_tables, describe_table, sample_data, select, insert, update, delete
    # Sample SQL command: {"operation": "list_tables"}, {"operation": "describe_table", "table": "table_name"}, {"operation": "sample_data", "table": "table_name", "limit": 5}, {"operation": "select", "query": "SELECT * FROM table_name"}
    # If the command is a NoSQL command, it should specify the operation and the collection to be used. Operations include: list_collections, sample_data, find, aggregate, insert, update, delete
    # Sample NoSQL command: {"operation": "list_collections"}, {"operation": "sample_data", "collection": "collection_name", "limit": 5}, {"operation": "find", "query": {"field": "value"}}, {"operation": "aggregate", "pipeline": [{"$match": {"field": "value"}}]}, {"operation": "insert", "data": {"field": "value"}}, {"operation": "update", "query": {"field": "value"}, "update": {"$set": {"field": "new_value"}}}, {"operation": "delete", "query": {"field": "value"}}


    # Load .env file automatically
    dotenv_path = find_dotenv()
    if not dotenv_path:
        print(
            "Warning: .env file not found. Make sure it's in your project root or specify environment variables manually.")
    else:
        load_dotenv(dotenv_path)

    # Import OpenAI client for v1 library

    # Configuration: ensure required environment variables are set
    env_vars = [
        "OPENAI_API_KEY",
    ]
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("Missing required environment variable: OPENAI_API_KEY")

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def read_json_file(file_path: str) -> dict:
        """
        Reads a JSON file and returns its content as a dictionary.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


    def call_openai(prompt,
                    model="gpt-4o-mini",
                    temperature=0.1) -> str:
        """
        Calls the OpenAI chat completion API using v1 client and returns the assistant's reply.
        """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": f""""please change the natural language query to a tuple consists of (db_type, command)：
                    - db_type: "SQL" or "NoSQL"
                    - command: JSON format command, which should be like:
                SQL:
                    {{ "operation": "list_tables" }}
                    {{ "operation": "describe_table", "table": "table_name" }}
                    {{ "operation": "sample_data", "table": "table_name", "limit": 5 }}
                    {{ "operation": "select", "query": "SELECT * FROM table_name WHERE ..." }}
                    {{ "operation": "insert", "table": "table_name", "data": {{...}} }}
                    {{ "operation": "update", "table": "table_name", "query": {{...}}, "update": {{...}} }}
                    {{ "operation": "delete", "table": "table_name", "query": {{...}} }}
                ...
                NoSQL:
                    {{ "operation": "list_collections" }}
                    {{ "operation": "sample_data", "collection": "name", "limit": 5 }}
                    {{ "operation": "find", "collection": "name", "query": {{ "field": "value" }} }}
                    {{ "operation": "aggregate","collection": "name", "pipeline": [{{"$match": {{...}}}}] }}
                    {{ "operation": "insert", "collection": "name", "data": {{...}} }}
                    {{ "operation": "update", "collection": "name", "query": {{...}}, "update": {{...}} }}
                    {{ "operation": "delete", "collection": "name", "query": {{...}} }}
                ...
                Please only return the tuple without any extra explanation. For example:
                ("SQL", {{ "operation": "select", "query": "SELECT * FROM users" }}) 
                
                ...
                data structure:
                
                {read_json_file('pixar_dataset_format.json')} to get the data structure of pixar_films dataset.
                {read_json_file('toys_dataset_format.json')} to get the data structure of toys dataset.
                {read_json_file('restaurant_dataset_format.json')} to get the data structure of restaurant dataset.
                """},

                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    def convert_(NL_query: str) -> Tuple[str, str]:
        """
        Transform a natural language query into a SQL or NoSQL command.

        Args:
            NL_query (str): The natural language query.

        Returns:
            Tuple[str, str]: (db_type, command)
                                  db_type: "SQL" or "NoSQL"
                                  command: JSON format string command
        """
        prompt = f"""
        ---
        Natural language query：
        \"\"\"{NL_query}\"\"\"
        """
        raw = call_openai(prompt)
        try:
            # eval 安全性取决于模型输出，如果环境可控，可考虑用 ast.literal_eval
            db_type, cmd = eval(raw)

            if not isinstance(cmd, str):
                # raise ValueError("Command should be a string.")
                if not isinstance(cmd, dict):
                    raise ValueError("Command should be a JSON format string.")
            
            cmd = json.dumps(cmd, ensure_ascii=False)
            return db_type, cmd
        except Exception as e:
            raise ValueError(f"Error occurs: {e}\noriginal output：{raw}")

    #
    db_type, command = convert_(NL_query)
    return db_type, command


if __name__ == "__main__":
    example = 'please show me the table structure of the "users" table'
    db_type, command = convert(example)
    print("DB type：", db_type)
    print("SQL or NoSQL command：", command)
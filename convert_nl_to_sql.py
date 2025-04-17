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


    def call_openai(prompt,
                    model="gpt-4o-mini",
                    temperature=0.2) -> str:
        """
        Calls the OpenAI chat completion API using v1 client and returns the assistant's reply.
        """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()

    def convert_(NL_query: str) -> Tuple[str, str, Union[dict, str]]:
        """
        将自然语言查询转换为 SQL 或 NoSQL 命令。

        Args:
            NL_query (str): 自然语言查询

        Returns:
            Tuple[str, str, dict]: (db_type, database_name, command_dict)
                                  db_type: "SQL" 或 "NoSQL"
                                  database_name: 例如 "PostgreSQL", "MongoDB" 等
                                  command_dict: 对应的 JSON 格式命令
        """
        prompt = f"""
    请将以下自然语言查询转换成三元组 (db_type, database_name, command)：
    - db_type: "SQL" 或 "NoSQL"
    - database_name: 使用的数据库名称（例如 "PostgreSQL", "MySQL", "MongoDB"）
    - command: JSON 格式的命令，符合下面规范：
      SQL:
        {{ "operation": "list_tables" }}
        {{ "operation": "describe_table", "table": "table_name" }}
        {{ "operation": "sample_data", "table": "table_name", "limit": 5 }}
        {{ "operation": "select", "query": "SELECT * FROM table_name WHERE ..." }}
        ...
      NoSQL:
        {{ "operation": "list_collections" }}
        {{ "operation": "sample_data", "collection": "name", "limit": 5 }}
        {{ "operation": "find", "query": {{ "field": "value" }} }}
        {{ "operation": "aggregate", "pipeline": [{{"$match": {{...}}}}] }}
        ...
    仅返回 Python 风格的三元组，例如：
    ("SQL", "PostgreSQL", {{ "operation": "select", "query": "SELECT * FROM users" }})
    不要做额外解释。
    ---
    自然语言查询：
    \"\"\"{NL_query}\"\"\"
    """
        raw = call_openai(prompt)
        try:
            # eval 安全性取决于模型输出，如果环境可控，可考虑用 ast.literal_eval
            db_type, db_name, cmd = eval(raw)
            if isinstance(cmd, str):
                # 如果模型误输出了字符串，则尝试 JSON 解析
                cmd = json.loads(cmd)
            return db_type, db_name, cmd
        except Exception as e:
            raise ValueError(f"解析模型输出失败: {e}\n输出原文：{raw}")

    #
    db_type, db_name, command = convert_(NL_query)
    return db_type, db_name, command


if __name__ == "__main__":
    example = '请给我一个包含用户信息的表格，表格中包含用户的姓名、年龄和电子邮件地址。'
    db_type, db_name, command = convert(example)
    print("DB 类型：", db_type)
    print("数据库：", db_name)
    print("命令 JSON：", json.dumps(command, ensure_ascii=False, indent=2))


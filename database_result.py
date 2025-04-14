from sqlalchemy import create_engine,text
import pymysql
import pandas as pd
import sys
import pymongo
import json
import getpass

def mysql_runner(sql_query: str) -> str:
    # Connect to the database
    # Enter your database password here
    my_sql_password = input("Enter your MySQL password: ")
    connection = f"mysql+pymysql://root:{my_sql_password}@localhost/chatDB"
    engine = create_engine(connection)

    try:
        with engine.connect() as conn:
            # Check if query starts with SELECT 
            if sql_query.strip().lower().startswith("select"):
                df = pd.read_sql(sql_query, conn)
                print(df)
                return df.to_string(index=False)
            else:
                # Execute non-SELECT query inside a transaction
                with conn.begin():
                    conn.execute(text(sql_query))
                return "Query executed successfully."
    except Exception as e:
        return f"Error executing query: {e}"
    
def mongo_runner(mongo_command: str) -> str:
    # Prompt securely for MongoDB password (if needed)
    # For local development, this may be optional or use default credentials
    mongo_password = getpass.getpass("Enter your MongoDB password (leave blank if not required): ")
    connection = f"mongodb://localhost:27017"

    try:
        client = pymongo.MongoClient(connection)
        db = client.chatDB

        ###########################################################
        collection = db.chatCollection  # Change to your target collection

        # Expecting mongo_command to be a JSON-formatted string with operation details
        command = json.loads(mongo_command)
        ###########################################################
        
        operation = command.get("operation")
        query = command.get("query", {})
        data = command.get("data", {})
        update = command.get("update", {})

        if operation == "find":
            cursor = collection.find(query)
            result = list(cursor)
            return json.dumps(result, indent=2, default=str)

        elif operation == "insert":
            res = collection.insert_one(data)
            return f"Inserted document with _id: {res.inserted_id}"

        elif operation == "update":
            res = collection.update_one(query, {"$set": update})
            return f"Matched: {res.matched_count}, Modified: {res.modified_count}"

        elif operation == "delete":
            res = collection.delete_one(query)
            return f"Deleted: {res.deleted_count}"

        else:
            return "Unsupported MongoDB operation."

    except Exception as e:
        return f"Error executing MongoDB command: {e}"
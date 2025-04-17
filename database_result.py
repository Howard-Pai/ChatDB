from sqlalchemy import create_engine,text
import pymysql
import pandas as pd
import sys
import pymongo
import json
import getpass

def mysql_runner(sql_command: str) -> str:
    # Connect to the database
    my_sql_password = input("Enter your MySQL password: ")
    connection = f"mysql+pymysql://root:{my_sql_password}@localhost/chatDB"
    engine = create_engine(connection)

    sql_command = json.loads(sql_command)
    try:
        with engine.connect() as conn:
            # Check if query starts with SELECT 
            operation = sql_command.get("operation")

            if operation == "list_tables":
                df = pd.read_sql("SHOW TABLES;", conn)
                return df.to_string(index=False)

            elif operation == "describe_table":
                table = sql_command.get("table")
                if not table:
                    return "Missing 'table' key in command."
                df = pd.read_sql(f"DESCRIBE {table};", conn)
                return df.to_string(index=False)

            elif operation == "sample_data":
                table = sql_command.get("table")
                limit = sql_command.get("limit", 5)
                df = pd.read_sql(f"SELECT * FROM {table} LIMIT {limit};", conn)
                return df.to_string(index=False)

            elif operation == "select":
                df = pd.read_sql(sql_command, conn)
                return df.to_string(index=False)
            else:
                with conn.begin():
                    conn.execute(text(sql_command))
                return "Query executed successfully."

    except Exception as e:
        return f"Error executing query: {e}"
    
def mongo_runner(mongo_command: str) -> str:
    mongo_password = getpass.getpass("Enter your MongoDB password: ")
    connection = f"mongodb://localhost:27017"

    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(connection)
        db = client.get_database("chatDB")

        command = json.loads(mongo_command)
        operation = command.get("operation")

        # Handle schemas & data exploration operations:
        if operation == "list_collections":
            collections = db.list_collection_names()
            return json.dumps(collections, indent=2)

        elif operation == "sample_data":
            collection_name = command.get("collection")
            limit = command.get("limit", 5)
            if not collection_name:
                return "Error: 'collection' is required for sample_data operation."
            collection = db[collection_name]
            cursor = collection.find().limit(limit)
            return json.dumps(list(cursor), indent=2, default=str)
        
        # Handle CRUD operations:
        collection_name = command.get("collection")
        collection = db[collection_name]

        if operation == "find":
            query = command.get("query", {})
            projection = command.get("projection")
            cursor = collection.find(query, projection) if projection else collection.find(query)
            return json.dumps(list(cursor), indent=2, default=str)

        elif operation == "aggregate":
            pipeline = command.get("pipeline", [])
            if not isinstance(pipeline, list):
                return "Error: 'pipeline' must be a list of aggregation stages."
            result = list(collection.aggregate(pipeline))
            return json.dumps(result, indent=2, default=str)

        elif operation == "insert":
            data = command.get("data")
            if isinstance(data, list):
                res = collection.insert_many(data)
                return f"Inserted {len(res.inserted_ids)} documents."
            elif isinstance(data, dict):
                res = collection.insert_one(data)
                return f"Inserted document with _id: {res.inserted_id}"
            else:
                return "Error: 'data' must be a dict or list of dicts."

        elif operation == "update":
            query = command.get("query", {})
            update = command.get("update", {})
            res = collection.update_one(query, {"$set": update})
            return f"Matched: {res.matched_count}, Modified: {res.modified_count}"

        elif operation == "delete":
            query = command.get("query", {})
            res = collection.delete_one(query)
            return f"Deleted: {res.deleted_count}"

        else:
            return "Unsupported MongoDB operation."

    except Exception as e:
        return f"Error executing MongoDB command: {e}"
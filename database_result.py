from sqlalchemy import create_engine, text
import pymysql
import pandas as pd
import sys
import pymongo
import json
import getpass

IPV4_DNS = "ec2-3-149-5-70.us-east-2.compute.amazonaws.com"
MYSQL_PASSWORD = "DSCI551"
DATABASE_NAME = "chatDB"


def mysql_runner(sql_command: str) -> str:
    # Connect to the database
    connection = f"mysql+pymysql://root:{MYSQL_PASSWORD}@{IPV4_DNS}/{DATABASE_NAME}"
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
                sql_query = sql_command.get("query")
                df = pd.read_sql(sql_query, conn)
                return df.to_string(index=False)
            elif operation == "insert":
                table = sql_command.get("table")
                data = sql_command.get("data")

                if not table or not data:
                    return "Missing 'table' or 'data' key in command."

                # Construct the INSERT SQL with bind parameters
                columns = ", ".join(data.keys())
                placeholders = ", ".join([f":{k}" for k in data.keys()])
                insert_query = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})")

                with conn.begin():
                    conn.execute(insert_query, data)

                return "Insert executed successfully."
            elif operation == "update":
                table = sql_command.get("table")
                query = sql_command.get("query")
                update = sql_command.get("update")
                if not (table and query and update):
                    return "Missing required fields for update."

                # Build SET clause
                set_clause = ", ".join(f"{k} = :set_{k}" for k in update.keys())
                # Build WHERE clause
                where_clause = " AND ".join(f"{k} = :where_{k}" for k in query.keys())

                sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
                params = {f"set_{k}": v for k, v in update.items()}
                params.update({f"where_{k}": v for k, v in query.items()})

                with conn.begin():
                    conn.execute(text(sql), params)
                return "Update executed successfully."
            elif operation == "delete":
                table = sql_command.get("table")
                query = sql_command.get("query")
                if not (table and query):
                    return "Missing required fields for delete."

                where_clause = " AND ".join(f"{k} = :{k}" for k in query.keys())
                sql = f"DELETE FROM {table} WHERE {where_clause}"
                with conn.begin():
                    conn.execute(text(sql), query)
                return "Delete executed successfully."
            else:
                return "Unsupported SQL operation."

    except Exception as e:
        return f"Error executing query: {e}"


def mongo_runner(mongo_command: str) -> str:
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(f"mongodb://{IPV4_DNS}:27017/")
        db = client.get_database(DATABASE_NAME)

        command = json.loads(mongo_command)
        operation = command.get("operation")
        print(operation)

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
        print("collection_name {}".format(collection_name))
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
            res = collection.update_one(query, update)
            return f"Matched: {res.matched_count}, Modified: {res.modified_count}"

        elif operation == "delete":
            query = command.get("query", {})
            res = collection.delete_one(query)
            return f"Deleted: {res.deleted_count}"

        else:
            return "Unsupported MongoDB operation."

    except Exception as e:
        return f"Error executing MongoDB command: {e}"
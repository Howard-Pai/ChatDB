import sys
import convert_nl_to_sql
import database_result

if __name__ == "__main__":
    # sample input: python3 main.py "NL comand"
    if len(sys.argv) != 2:
        print("Please provide a command in natural language.")
        sys.exit(1)
    
    command = sys.argv[1]
    print(f"Command: {command}")

    # Call the function to convert NL command to SQL
    # The return value is a tuple (db_type, command), where db_type is either "SQL" or "NoSQL" and command is a JSON-formatted string.
    # If the command is a SQL command, it should specify the operation to be performed. operaitons include: show_tables, describe_table, sample_data, select, insert, update, delete
    # Sample SQL command: {"operation": "list_tables"}, {"operation": "describe_table", "table": "table_name"}, {"operation": "sample_data", "table": "table_name", "limit": 5}, {"operation": "select", "query": "SELECT * FROM table_name"}
    # If the command is a NoSQL command, it should specify the operation and the collection to be used. Operations include: list_collections, sample_data, find, aggregate, insert, update, delete
    # Sample NoSQL command: {"operation": "list_collections"}, {"operation": "sample_data", "collection": "collection_name", "limit": 5}, {"operation": "find", "query": {"field": "value"}}, {"operation": "aggregate", "pipeline": [{"$match": {"field": "value"}}]}, {"operation": "insert", "data": {"field": "value"}}, {"operation": "update", "query": {"field": "value"}, "update": {"$set": {"field": "new_value"}}}, {"operation": "delete", "query": {"field": "value"}}

    db_type, command = convert_nl_to_sql(command)

    if command:
        print("Command after conversion:")
        print(command)
    else:
        print("Could not generate command.")
        sys.exit(1)

    if db_type == "SQL":
        # Send the SQL query to the database
        mysql_result = database_result.mysql_runner(command)
    elif db_type == "NoSQL":
        # Send the NoSQL query to the database
        mysql_result = database_result.mongo_runner(command)
    else:
        print("Unsupported database type.")
        sys.exit(1)

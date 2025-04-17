import sys
import convert_nl_to_sql
import database_result

if __name__ == "__main__":
    # sample input: python3 main.py "NL comand"
    if len(sys.argv) != 2:
        print("Please provide a command in natural language.")
        sys.exit(1)
    
    NL_query = sys.argv[1]
    print(f"Command: {NL_query}")

    # Call the function to convert NL query to SQL
    db_type, database_name, command = convert_nl_to_sql.convert(NL_query)

    if command:
        print("Command after conversion:")
        print(command)
    else:
        print("Could not generate command.")
        sys.exit(1)

    if db_type == "SQL":
        # Send the SQL query to the database
        mysql_result = database_result.mysql_runner(database_name, command)
    elif db_type == "NoSQL":
        # Send the NoSQL query to the database
        mysql_result = database_result.mongo_runner(database_name, command)
    else:
        print("Unsupported database type.")
        sys.exit(1)

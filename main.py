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

    #call the function to convert NL command to SQL
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

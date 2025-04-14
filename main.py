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
    sql_query = convert_nl_to_sql(command)

    if sql_query:
        print("Generated SQL Query:")
        print(sql_query)
    else:
        print("Could not generate SQL query.")
        sys.exit(1)

    # Send the SQL query to the database
    mysql_result = database_result(sql_query)

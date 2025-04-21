import sys
import convert_nl_to_sql
import database_result

if __name__ == "__main__":
    # sample input: python3 main.py "NL comand"
    while True:

        NL_query = str(input('>>'))
        if NL_query == "exit":
            break
        print(f"Command: {NL_query}")

        # Call the function to convert NL query to SQL
        db_type, command = convert_nl_to_sql.convert(NL_query)

        if command:
            print("Command after conversion:")
            print(command)
        else:
            print("Could not generate command.")
            sys.exit(1)

        if db_type == "SQL":
            # Send the SQL query to the database
            mysql_result = database_result.mysql_runner(command)
            print(mysql_result)
        elif db_type == "NoSQL":
            # Send the NoSQL query to the database
            Nosql_result = database_result.mongo_runner(command)
            print(Nosql_result)
        else:
            print("Unsupported database type.")
            sys.exit(1)
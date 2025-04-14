from sqlalchemy import create_engine,text
import pymysql
import pandas as pd
import sys


def mysql_runner(sql_query: str) -> str:
    # Connect to the database
    # Enter your database password here
    my_sql_password = input("Enter your MySQL password: ")
    connection = f"mysql+pymysql://root:{my_sql_password}@localhost/chatDB"
    engine = create_engine(connection)

    try:
        with engine.connect() as conn:
            # Check if query starts with SELECT (case-insensitive)
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
    
    print(output)
    return output
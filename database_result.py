from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys


def mysql_runner(sql_query: str) -> str:
    # Connect to the database
    # Enter your database password here
    my_sql_password = input("Enter your MySQL password: ")
    connection = f"mysql+pymysql://root:{my_sql_password}@localhost/banking"
    engine = create_engine(connection)
    output = pd.read_sql(sql_query, engine)
    print(output)


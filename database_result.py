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
    first_name = sys.argv[1]
    last_name = sys.argv[2]
    output = pd.read_sql(f"select AccountID, AccountType, Balance from account a left join customer c on a.CustomerID = c.CustomerID "
                        f"where c.FirstName = '{first_name}' and c.LastName = '{last_name}'", engine)
    print(output)
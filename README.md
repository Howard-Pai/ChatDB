# ChatDB

This project provides a natural language interface to allow users to interact with MySQL and MongoDB (and other datasets) through plain English queries. The system leverages OpenAI’s GPT models (such as GPT‑4‑o‑mini) to convert natural language into SQL or NoSQL commands, which are then executed using libraries like SQLAlchemy, PyMySQL, and PyMongo.

## Prerequisites

- Operating System: macOS
- Python 3.8 or higher
- Installed [virtualenv](https://virtualenv.pypa.io/en/latest/) (or use Python’s built-in venv)
- The following API/environment variables must be set:
  - `OPENAI_API_KEY`: Your OpenAI API key. Save the key in a `.env` file (see `.env.example` for reference).
- For using MySQL or MongoDB, ensure you have these details:
  - MySQL connection information (IP/DNS, password, database name)
  - MongoDB connection information (IP/DNS, database name)

> Note: Do not hardcode your personal API key into the code. Use environment variables or the `.env` file. Ensure the `.env` file is included in `.gitignore` to avoid exposing sensitive information.

## Environment Setup

1. **Clone the Repository**

   ```
   git clone https://github.com/Howard-Pai/ChatDB.git
   cd ChatDB
   ```

2. **Create a Virtual Environment**

   You can create a virtual environment using one of the following methods:

   - Using virtualenv:
     ```
     virtualenv venv
     source venv/bin/activate
     ```

   - Or using Python’s built-in venv module:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the Required Libraries**

   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**

   In the root directory, create a `.env` file and add the following:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   Note: Do not expose your API key. Make sure the `.env` file is excluded from the repository.

## Running the Project

1. After activating the virtual environment, run the main program:
   ```
   python main.py
   ```

2. When the system starts, follow the prompt to enter your natural language query. The program will convert it into an SQL or NoSQL command and connect to the appropriate database for execution.

3. Type `exit` to quit the program.

## Database Configuration

- **MySQL Configuration**

  Verify the configuration in the `database_result.py` file:
  - `IPV4_DNS`
  - `MYSQL_PASSWORD`
  - `DATABASE_NAME`

- **MongoDB Configuration**

  Verify the connection and database name settings for MongoDB.

## Security Recommendations

- Do not hardcode your API keys into the source code. Always utilize environment variables or the `.env` file to manage sensitive data.
- Ensure `.env` is included in the `.gitignore` file to prevent accidental exposure of your API keys.
- Remove or hide all sensitive information before making the repository public.

## References

- [OpenAI API Documentation](https://beta.openai.com/docs/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [PyMySQL Documentation](https://github.com/PyMySQL/PyMySQL)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)


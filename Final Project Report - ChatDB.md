

## Google Drive/GitHub Link
https://github.com/Howard-Pai/ChatDB.git
---

## Introduction
The goal of this project is to develop **ChatDB**, a natural language interface (NLI) that allows users to interact with database management systems (DBMS) through conversational queries. ChatDB enables users to explore database schemas, retrieve data, and modify it—all by inputting queries in natural language. The system integrates with both **Relational Database Management Systems (RDBMS)** and **NoSQL databases**, specifically MySQL and MongoDB, respectively, to provide comprehensive database management capabilities.

This project utilizes advanced Natural Language Processing (NLP) techniques to convert human-readable queries into SQL or MongoDB commands that can be executed by the respective database systems. Users can request schema exploration, issue SELECT queries, perform JOIN operations, and even modify data (insert, update, delete) directly using plain language.

In addition, **ChatDB** supports multiple datasets to demonstrate its flexibility across different types of databases. For example, the project integrates with datasets from the **Pixar** and **Toys** domains, allowing users to query data related to films, products, stores, and sales.

Key features include:

- Database schema exploration (e.g., listing tables, retrieving sample data)
- Querying capabilities (SELECT, JOIN, WHERE clauses, etc.)
- Data modification (INSERT, UPDATE, DELETE)
- Integration with both RDBMS and NoSQL (MongoDB)

The project leverages modern **Large Language Models (LLMs)**, like OpenAI's GPT-4o-mini, to process and interpret user queries, translating them into database-specific commands.

---

## Planned Implementation (From Project Proposal)
Initially, our plan was to develop a **natural language interface (NLI)** for querying a **stock exchange database**, supporting both **SQL** and **NoSQL** systems. We intended to use **MySQL**, **PostgreSQL**, and **MongoDB** to build the system, and utilize **OpenAI GPT-4** or other large language models to convert natural language queries into SQL commands, with functionality to support querying, data modification, and more. The original goal was to focus on stock data analysis and queries, supporting complex operations like **JOIN** and **data modification**.

However, during the course of the project, we realized that the **stock exchange database** project had already been explored by many other teams, which led us to adjust our focus. As a result, we decided to shift our attention toward developing a more generalized **ChatDB** system, a natural language interface capable of querying and synthesizing features from different datasets.

The new direction for the project is to create a **universal natural language interface (ChatDB)** that will support querying not just stock databases but also other types of data, such as **Pixar films**, **toy sales**, and **restaurant menu data**. Our goal is to synthesize features from these datasets, which may later be relevant to **stock prices** or other financial data, potentially uncovering certain **correlations or causal relationships**. This shift will allow ChatDB to not only handle traditional queries but also explore the underlying patterns and relationships in the data.

### Key Changes:

1. **Data Scope Expansion**: Instead of focusing solely on the stock exchange database, the project now incorporates datasets like **Pixar**, **Toy sales**, and **Restaurant menu** data.
2. **Database Selection**: We are still using **MySQL** and **PostgreSQL** for relational databases but have also integrated **MongoDB** for NoSQL data.
3. **Model Update**: While we continue to use **OpenAI GPT-4** and other large language models to process natural language queries, the focus has shifted from just generating SQL queries to synthesizing different features from the data, which may reveal correlations or causal relationships with stock prices or other financial indicators.
4. **Interface Development**: The new ChatDB system will allow users to interact with it via natural language, supporting not only data queries but also the synthesis of new features, which could potentially be used to explore **stock price prediction** or other business-related applications in the future.

The ultimate goal of this project is to create a flexible and user-friendly system that allows users to interact with different databases using natural language, while also synthesizing valuable features that might have an impact on financial data such as stock prices.

---

## Architecture Design
### Flow Diagram
(Insert flow diagram here)

### Description
Provide a description of the system's architecture. Include how the different components interact and the role of each module.

---

## Implementation

### 1. Functionalities

The **ChatDB** project enables users to interact with multiple database systems using **natural language**. The system is designed to convert user inputs in plain English (or other languages) into SQL or MongoDB commands for querying and modifying databases. The key functionalities of the system include:

#### 1.1. **Natural Language to SQL Conversion**

- The system uses advanced **Natural Language Processing (NLP)** techniques to understand user queries and convert them into executable SQL commands. It supports standard SQL constructs like `SELECT`, `FROM`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, and `LIMIT`.
    
- For example, if a user asks, "Show me all films from Pixar," the system can translate this into a SQL query like `SELECT * FROM pixar_films`.
    

#### 1.2. **Data Exploration**

- ChatDB allows users to explore the schema of the database in natural language. Users can ask questions such as:
    
    - "What tables are available in the database?"
    - "What columns does the `movies` table have?"
    - "Show me sample data from the `products` table."
        
- These queries are translated into appropriate database commands to retrieve the schema or sample data and display it to the user in a readable format.
    

#### 1.3. **Data Modification**

- Users can modify data directly using natural language commands such as:
    
    - **Insert**: "Add a new product called 'Toy Car' with price $15."
    - **Update**: "Update the price of 'Toy Car' to $10."
    - **Delete**: "Delete all records where stock is zero."
        
- The system processes these commands and executes the appropriate SQL or MongoDB operations (`INSERT`, `UPDATE`, `DELETE`).
    

#### 1.4. **Multi-database Support**

- The system is capable of interacting with both **relational databases** (MySQL, PostgreSQL) and **NoSQL databases** (MongoDB). It automatically determines which database to query based on the structure and syntax of the input query. For example, a query for a `JOIN` operation will be converted into SQL for relational databases, while data retrieval operations in MongoDB will use the appropriate NoSQL query syntax.
    

#### 1.5. **Feature Synthesis and Data Insights**

- Beyond just querying and modifying data, **ChatDB** can also synthesize new features or generate insights from the data. For example, it can provide insights on correlations, trends, or patterns within the data.
    


### 2. Tech Stack

The **ChatDB** project leverages a modern stack of technologies and tools to support its functionalities. The tech stack includes the following components:

#### 2.1. **Backend**

- **Python**: The backend is built using Python, a versatile language ideal for data processing, and API development.
    

#### 2.2. **Database**

- **MySQL**: A relational database management system (RDBMS) used for storing structured data. ChatDB interacts with MySQL to process SQL queries and modify data.
    
- **MongoDB**: A NoSQL database used to handle unstructured or semi-structured data, providing flexibility for storing data in JSON-like documents.
    

#### 2.3. **NLP Model**

- **OpenAI GPT-4**: OpenAI’s GPT models are used to process the natural language queries and convert them into structured SQL or MongoDB queries. These models are powerful for understanding the context of user input and generating appropriate database queries
    

#### 2.5. **Other Tools**

- **SQLAlchemy**: An ORM (Object-Relational Mapper) for Python that abstracts the complexity of direct SQL queries. It provides a more Pythonic interface to interact with relational databases.
    
- **pymysql/psycopg2**: Libraries used to connect to MySQL and PostgreSQL databases, respectively, and execute SQL queries.
    
- **pymongo**: A Python driver for MongoDB used to handle operations and queries in the NoSQL database.

### 3. Implementation Screenshots
(Insert a few relevant screenshots of the working system, such as UI, code snippets, etc.)

---

## Learning Outcomes
Discuss what you learned during the project, such as new technologies, approaches, or any domain-specific knowledge related to databases and NLP.

---

## Challenges Faced
List the main challenges encountered during the project and how you overcame them.

---

## Individual Contribution
If this is a multi-person project, describe the individual contributions made by each team member. Be specific.

---

## Conclusion
Provide a summary of the project, its outcomes, and any concluding thoughts. Discuss whether the project met the initial objectives.

---

## Future Scope
Explain potential improvements or new features that could be added to your project in the future.

---

## README.md
Please attach a detailed `README.md` file that includes:
1. A step-by-step guide on how to implement your code.
2. Prerequisites such as installed software, API keys, etc.
3. Instructions on where to add personal API keys (if applicable).

---

## Requirements.txt
Include a `requirements.txt` file to create a virtual environment with all necessary libraries. Ensure that it contains all dependencies for running the project.

---

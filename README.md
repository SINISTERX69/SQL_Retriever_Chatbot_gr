# SQL Data Retriever

SQL Data Retriever is a chat-based interface designed to interact with a local `SQLite` database using natural language queries. It provides a way for users to fetch data from a company database by simply typing queries in conversational language. The system translates these queries into SQL `SELECT` statements and retrieves the relevant data.

## Features

- **Natural Language Interface**: Allows users to input queries in natural language.
- **SQL Query Execution**: Translates natural language queries into SQL and executes them against a `SQLite` database.
- **Error Handling**: Includes extensive error handling for query execution, formatting, and database connectivity.
- **Tool Integration**: Utilizes a tool-based architecture to execute SQL queries.
- **Model Selection**: Supports selection from available language models for query processing.

## Project Structure

- `Company_Chatbot`: 
  - The main class that initializes the chatbot, reads the system prompt, sets up the SQL tool, and handles interactions.

- `SQLFetchTool`: 
  - A function designed to execute and handle SQL `SELECT` queries, including error management for invalid queries or connection issues.

- `tool_call_handling`: 
  - Handles tool calls, processes results, and formats responses for the chat interface.

- `chat_func`: 
  - Manages chat interactions, processes user inputs, and integrates with LLMs to generate responses.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) installed on your machine.
- [gradio](https://gradio.app/): The UI framework for the chat interface.
- [SQLAlchemy](https://www.sqlalchemy.org/): ORM for database connectivity and queries.
- [ollama](https://ollama.com/download) Open Source API for running LLMs locally.
- Use the `create_db.py` to create a new custom db or use the one provided in repo.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your_username/sql-data-retriever.git
   cd sql-data-retriever
   ```

2. Install the required Python packages:

   ```bash
   pip install gradio sqlalchemy
   ```

3. Ensure your `Company.db` database is properly set up and configured.

### Running the Application

Launch the chat interface locally by executing the script:

```bash
python Main.py
```

The interface will open in your default web browser and the website will be hosted locally for 72 hours.
The public link will be available in the terminal. 

### Usage

- Select the preferred language model from the dropdown.
- Enter your natural language query in the provided textbox. 
- Receive SQL query results directly through the chat interface.

## Error Handling

The system is designed to handle various errors during query execution, including:

- **Invalid Query Format**: Ensures only valid `SELECT` queries are run.
- **Database Connection Errors**: Reports issues with connecting to the `SQLite` database.
- **Empty Query or Results**: Handles cases where queries are empty or return no results.

## Customization

- **System Prompt**: Modify the `system_prompt.txt` file to tailor the system’s initial behavior.
- **Database**: Replace `Company.db` with your own SQLite database.

## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

## Contact

Your Name - [Aniket Das](mailto:aniket.das1203@gmail.com)

Project Link: [https://github.com/SINISTERX69/SQL_Retriever_Chatbot_gr](https://github.com/SINISTERX69/SQL_Retriever_Chatbot_gr)

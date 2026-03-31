import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_classic import hub
from langgraph.prebuilt import create_react_agent

load_dotenv()


# Connecting MySQL database
host = os.getenv("DB_HOST", "localhost")
port = "3306"
username = "root"
password = os.getenv("SQL_PASSWORD")
database_schema = "text_to_sql"

mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"
db = SQLDatabase.from_uri(mysql_uri)

# Call the LLM
GEMINI_API = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", api_key = GEMINI_API)

# Prepare Tools
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()
print(tools)

# Define a custom System Message
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

assert len(prompt_template.messages) == 1
print(prompt_template.input_variables)

system_message = prompt_template.format(dialect="mysql", top_k=5)

# Create the Agent
agent_executor = create_react_agent(llm, tools, prompt=system_message)

# Run a Query
def ask_agent(question):
    print(f"\n--- Question: {question} ---\n")
    inputs = {"messages": [("user", question)]}
    for event in agent_executor.stream(inputs, stream_mode="values"):
        # This prints the step-by-step reasoning and tool calls
        event["messages"][-1].pretty_print()

if __name__ == "__main__":
	ask_agent("How many products are in the database?")

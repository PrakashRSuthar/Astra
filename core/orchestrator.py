from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from services import llm_service
# Agent Imports
from agents.research_agent import web_search
from agents.news_agent import news_search
from agents.writer_agent import writer
from agents.planner_agent import add_task, view_tasks
from agents.workspace_agent import add_workspace, open_workspace, list_workspaces, open_folder # <--- NAYA IMPORT

# Add the new open_folder tool to the list
tools = [
    web_search, 
    news_search, 
    writer,
    add_task,
    view_tasks,
    add_workspace,
    open_workspace,
    list_workspaces,
    open_folder
]

# The rest of the file remains exactly the same
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant named Astra. You have access to a set of tools to answer user questions."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

llm = llm_service.get_llm()
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True
)

def run_agent(user_query: str, chat_history: list):
    """Runs the main agent executor chain with chat history."""
    return agent_executor.invoke({
        "input": user_query,
        "chat_history": chat_history
    })
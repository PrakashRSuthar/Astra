from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from services import llm_service
# Agent Imports
from agents.research_agent import web_search
from agents.news_agent import news_search
from agents.writer_agent import writer
from agents.planner_agent import add_task, view_tasks
from agents.workspace_agent import add_workspace, open_workspace, list_workspaces, open_folder
from agents.memory_agent import save_memory, recall_memory, view_all_memories # <--- NAYA IMPORT

# Add the new memory tools to the list
tools = [
    web_search, 
    news_search, 
    writer,
    add_task,
    view_tasks,
    add_workspace,
    open_workspace,
    list_workspaces,
    open_folder,
    save_memory,
    recall_memory,
    view_all_memories
]

# --- THE MOST IMPORTANT CHANGE: THE NEW PROMPT ---
# This new prompt teaches the agent to be proactive about using its memory.
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are Astra, a helpful and personalized AI assistant. You have access to a set of tools to answer user questions.

CRITICAL INSTRUCTIONS:
1.  **Proactive Memory Saving:** If the user tells you a personal fact, preference, or any piece of information that might be useful later (e.g., "my favorite color is blue", "my project is due on Friday", "my friend's name is Alex"), you MUST use the `save_memory` tool to remember it.
2.  **Memory-First Approach:** Before answering any question, consider if you have any relevant information in your memory by using the `recall_memory` tool. Use this recalled information to provide a more personal and contextual answer.
3.  **Combine Tools:** You can use your memory to make other tools more powerful. For example, recall a user's favorite topic from memory, and then use that topic in a `web_search`.
"""),
    ("placeholder", "{chat_history}"),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# The rest of the file remains exactly the same
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
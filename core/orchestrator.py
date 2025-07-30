from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from services import llm_service
from agents.research_agent import web_search
from agents.news_agent import news_search
from agents.writer_agent import writer

tools = [web_search, news_search, writer]

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

def run_agent(user_query: str):
    """Runs the main agent executor chain."""
    return agent_executor.invoke({"input": user_query})
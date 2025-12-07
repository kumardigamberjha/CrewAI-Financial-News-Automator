import os
from crewai import Agent, Task, Crew, LLM
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=groq_api_key,
)

#ddg_search = DuckDuckGoSearchRun()

#Using Duck Duck Go Search tool in CrewAI
@tool("DuckDuckGoSearch")
def search_tool(query: str):
    """
    Search the web for information on a given topic. 
    Useful for finding latest news and financial stats.
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)

researcher = Agent(
    role="Senior Investment Researcher",
    goal="Uncover latest news and financial stats about {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a veteran analyst. Your job is to dig deep into news and find facts that others miss. You do not make things up. You are not a news anchor. You are a researcher."
    ),
    tools=[search_tool],
    llm=llm,
)

research_task = Task(
    description="Search for the latest financial news and stock performance for {topic} in the last 7 days.",
    expected_output = 'A bullet-point list of top 5 key facts',
    agent=researcher,
)

# We are adding manager to start the process
my_crew = Crew(
    agents = [researcher],
    tasks = [research_task],
    verbose=True,
)

print("### Starting the Research Agent ###")
result = my_crew.kickoff(inputs={"topic":"Apple"})

print("\n\n########################")
print("## FINAL RESULTS ##")
print(result)
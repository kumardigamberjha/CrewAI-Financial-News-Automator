import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from langchain_groq import ChatGroq


load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

# AGent must have parameters: (role, goal, backstory, llm, verbose) 
writer= Agent(
    role="You are an Senior Tech Blog Writer",
    goal="Write engaging and easy to understand tech articles",
    backstory="You are a senior tech blog writer with 15 years of experience in writing tech articles",
    allow_delegation=False,
    llm=llm,
    verbose=True,
)

# Testing data provided to writer to write blog post 
mock_research_data = """
1. AutoGPT: Autonomous AI agent that chains thoughts.
2. BabyAGI: Simple framework for task management using AI.
3. CrewAI: Role-based agent orchestration framework.
"""

task = Task(
    description=f"Write a short LinkedIn post (max 200 words) based on this research data: {mock_research_data}",
    expected_output="A professional LinkedIn post with emojis and hashtags.",
    agent=writer,
)

print("--- Starting Writer Agent Test ---")

writer_crew = Crew(
    agents=[writer],
    tasks=[task],
    verbose=True,
)

result = writer_crew.kickoff()

print("#################")
print("FINAL RESULT FROM AGENT 2:")
print(result)
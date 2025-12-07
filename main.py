import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool
import requests

# 1. SETUP
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not os.getenv("LINKEDIN_ACCESS_TOKEN") or not os.getenv("LINKEDIN_USER_ID"):
    print("⚠️ WARNING: LinkedIn keys are missing in .env. The Publisher agent will fail.")

# We can share this LLM instance across both agents
my_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=api_key,
)

# 2. DEFINE THE TOOL
# TOOL A: Search
@tool("DuckDuckGoSearch")
def search_tool(query: str):
    """
    Search the web for information on a given topic. 
    Useful for finding latest news and financial stats.
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)

# Tool B: LinkedIn Post
@tool("LinkedinPublisher")
def linkedin_post(text_content: str):
    """
    Publish a LinkedIn post with the given text content.
    """
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    user_id = os.getenv("LINKEDIN_AUTHOR_URN")
    
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    post_data = {
        "author": user_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text_content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 201:
        return "✅ Successfully posted to LinkedIn!"
    else:
        return f"❌ Failed to post. Error: {response.text}"

# 3. DEFINE AGENTS

# Agent 1: The Researcher
researcher = Agent(
    role="Senior Investment Researcher",
    goal="Uncover latest news and financial stats about {topic}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a veteran analyst. Your job is to dig deep into news and find facts that others miss. "
        "You do not make things up. You are not a news anchor. You are a researcher."
    ),
    tools=[search_tool],
    llm=my_llm,
)

# Agent 2: The Writer
writer = Agent(
    role="Senior Tech Blog Writer",
    goal="Write engaging and easy to understand tech articles about {topic}",
    backstory=(
        "You are a senior tech blog writer with 15 years of experience. "
        "You take complex financial data and turn it into exciting stories."
    ),
    allow_delegation=False,
    llm=my_llm,
    verbose=True,
)

# Agent 3: The Publisher
publisher = Agent(
    role="LinkedIn Publisher",
    goal="Publish a LinkedIn post with the given text content using the LinkedIn API",
    backstory=(
        "You are a LinkedIn publisher with 15 years of experience. "
        "You take complex financial data and turn it into exciting stories."
    ),
    tools=[linkedin_post],
    allow_delegation=False,
    llm=my_llm,
    verbose=True,
)

# 4. DEFINE TASKS

# Task 1: Research
# This runs first.
research_task = Task(
    description=(
        "Search for the latest financial news and stock performance for {topic} in the last 7 days. "
        "Focus on major announcements or market shifts."
    ),
    expected_output='A bullet-point list of top 5 key facts and metrics.',
    agent=researcher,
)

# Task 2: Writing
# This runs second. Crucially, we tell it to use the context from the previous task.
write_task = Task(
    description=(
        "Using the research findings from the previous task, write a professional LinkedIn post about {topic}. "
        "The post should be under 200 words, engaging, and include hashtags."
    ),
    expected_output="A ready-to-publish LinkedIn post.",
    agent=writer,
    context=[research_task] # Explicitly stating we need the output from task 1
)

#Task 3: Publishing
task_publish = Task(
    description=(
        "Take the text produced by the Writer and publish it to LinkedIn using the LinkedInPublisher tool. "
        "Do not alter the text. Just post it."
    ),
    expected_output="A confirmation message that the post was published.",
    agent=publisher,
    context=[write_task]
)

# 5. DEFINE THE CREW (THE MANAGER)
my_crew = Crew(
    agents=[researcher, writer, publisher],
    tasks=[research_task, write_task, task_publish], # The order matters here!
    verbose=True,
)

# 6. EXECUTE
print("### Starting the Corporate Crew ###")
user_input = "Apple" # You can change this to "Tesla", "Nvidia", etc.
result = my_crew.kickoff(inputs={"topic": user_input})

print("\n\n########################")
print("## FINAL LINKEDIN POST ##")
print(result)
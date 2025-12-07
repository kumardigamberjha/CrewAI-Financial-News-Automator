# 🚀 MarketPulse AI: Autonomous LinkedIn Publisher

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![CrewAI](https://img.shields.io/badge/Orchestration-CrewAI-orange)
![Groq](https://img.shields.io/badge/Inference-Groq-purple)
![LinkedIn API](https://img.shields.io/badge/API-LinkedIn-Bn)

## 📖 Overview

**MarketPulse AI** is a fully autonomous agentic workflow designed to streamline social media content creation for financial/tech influencers. 

Using **CrewAI** orchestration and **Groq's Llama 3** model, this system employs a team of AI agents to:
1.  **Research:** Scrape the web for the latest stock market news (e.g., Apple, Nvidia).
2.  **Write:** Draft engaging, viral-ready LinkedIn posts with hashtags.
3.  **Publish:** Automatically post the content to a personal LinkedIn profile via the official API.

## 🤖 The Crew

The system utilizes three specialized agents:

| Agent | Role | Function |
| :--- | :--- | :--- |
| **🕵️ Researcher** | Senior Investment Analyst | Uses `DuckDuckGo` to find real-time financial news and market moves. |
| **✍️ Writer** | Social Media Strategist | Transforms dry data into engaging, professional LinkedIn posts. |
| **🚀 Publisher** | API Manager | Handles OAuth2 authentication and pushes the final text to LinkedIn. |

## 🛠️ Tech Stack

* **Language:** Python
* **Framework:** [CrewAI](https://www.crewai.com/)
* **LLM Engine:** Groq (Llama-3-70b)
* **Search Tool:** DuckDuckGo
* **Authentication:** LinkedIn OAuth 2.0

## ⚡ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/MarketPulse-AI.git](https://github.com/YOUR_USERNAME/MarketPulse-AI.git)
    cd MarketPulse-AI
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory and add your keys:
    ```env
    GROQ_API_KEY=gsk_your_key_here
    LINKEDIN_CLIENT_ID=your_linkedin_client_id
    LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
    LINKEDIN_ACCESS_TOKEN=your_generated_access_token
    LINKEDIN_USER_ID=urn:li:person:your_id
    ```

## 🏃‍♂️ Usage

Run the main script to kick off the crew:

```bash
python main.py

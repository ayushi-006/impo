import os
import requests
from dotenv import load_dotenv
from langchain.tools import Tool

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def run_graphql_query(query, variables={}):
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers,
    )
    if response.status_code != 200:
        raise Exception(f"Query failed: {response.text}")
    return response.json()

def fetch_github_info(username:"ayushi-006") -> str:
    query = """
    query($login: String!) {
      user(login: $login) {
        name
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
        topRepositories(first: 5, orderBy: {field: STARGAZERS, direction: DESC}) {
          nodes {
            name
            description
            stargazerCount
            primaryLanguage { name }
            url
          }
        }
      }
    }
    """
    result = run_graphql_query(query, {"login": username})
    user = result["data"]["user"]
    name = user.get("name", username)
    total_contributions = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    repos = user["topRepositories"]["nodes"]

    summary = f"{name} has made {total_contributions} contributions this year.\nTop Projects:\n"
    for r in repos:
        summary += f"→ {r['name']} ({r['primaryLanguage']['name'] if r['primaryLanguage'] else 'N/A'}) - ⭐ {r['stargazerCount']}\n"
        summary += f"   {r['description']}\n   {r['url']}\n"
    # return summary

    # Save  to file
        with open("github_summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
        
        print("✅ GitHub summary saved to github_summary.txt")

# LangChain Tool wrapper
github_tool = Tool(
    name="GitHubProfileAnalyzer",
    func=fetch_github_info,
    description="Fetch GitHub contribution stats and top repositories for a given username"
)

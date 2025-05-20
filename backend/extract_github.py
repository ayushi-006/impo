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

github_username = "ayushi-006"  # Replace with the desired GitHub username
def fetch_github_info(username: str) -> str:
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
        if r is None:
            continue
        repo_name = r.get('name', 'N/A')
        language = r.get('primaryLanguage', {}).get('name') if r.get('primaryLanguage') else 'N/A'
        stars = r.get('stargazerCount', 0)
        description = r.get('description', '')
        url = r.get('url', '')
        total_contributions= r.get('totalContributions', 0)
        summary += f"→ {repo_name} ({language}) - ⭐ {stars}\n"
        summary += f"   {description}\n   {url}\n"
        # summary += f"   Skills: {', '.join(skills)}\n\n"
        summary += f"Total Contributions: {total_contributions}\n"  
    # return summary
    with open("github_summary.txt", "w", encoding="utf-8") as f:
     f.write(summary)

    print("✅ GitHub summary saved to github_summary.txt")

    
# github_summary = fetch_github_info("krishnaik06")
# Save  to file




# LangChain Tool wrapper
github_tool = Tool(
    name="GitHubProfileAnalyzer",
    func=fetch_github_info,
    description="Fetch GitHub contribution stats and top repositories for a given username"
)

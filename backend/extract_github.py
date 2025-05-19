#Extract GitHub info using GitHub API (starred repos, languages used, contributions).

import requests
import os
from dotenv import load_dotenv

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

def get_contribution_stats(username):
    query = """
    query($login: String!) {
      user(login: $login) {
        name
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
        repositories(first: 10, orderBy: {field: STARGAZERS, direction: DESC}, privacy: PUBLIC) {
          nodes {
            name
            description
            stargazerCount
            primaryLanguage {
              name
            }
            url
            updatedAt
          }
        }
        topRepositories(first: 5, orderBy: {field: STARGAZERS, direction: DESC}) {
          nodes {
            name
            description
            stargazerCount
            primaryLanguage {
              name
            }
          }
        }
      }
    }
    """
    variables = {"login": username}
    result = run_graphql_query(query, variables)
    return result["data"]["user"]

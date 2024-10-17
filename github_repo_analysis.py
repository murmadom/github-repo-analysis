import os
import requests
import json
import time
from dotenv import load_dotenv
from collections import Counter

# Load environment variables
load_dotenv()

# GitHub Personal Access Token from .env file
GITHUB_PAT = os.getenv("GITHUB_PAT")
HEADERS = {'Authorization': f'token {GITHUB_PAT}'}

# GitHub API URL
BASE_URL = "https://api.github.com/orgs/{org}/repos"

def get_repos(org):
    """Retrieve all repositories for a given organization using pagination."""
    repos = []
    page = 1
    per_page = 100
    while True:
        url = BASE_URL.format(org=org) + f"?page={page}&per_page={per_page}"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            repos.extend(data)
            if len(data) < per_page:
                break  # No more pages
            page += 1
        else:
            handle_api_error(response)
            break
    return repos

def handle_api_error(response):
    """Handle GitHub API error responses including rate limits."""
    if response.status_code == 403:
        if "rate limit" in response.text.lower():
            print("Rate limit exceeded. Retrying after delay...")
            time.sleep(60)  # Sleep for 1 minute
        else:
            print("Forbidden request. Check API token.")
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        response.raise_for_status()

def analyze_repos(repos):
    """Process repository data and return required analyses."""
    total_stars = 0
    languages = []
    repo_details = []
    
    for repo in repos:
        name = repo.get('name', 'N/A')
        description = repo.get('description', 'N/A')
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        language = repo.get('language', 'N/A')
        
        total_stars += stars
        if language:
            languages.append(language)
        
        repo_details.append({
            'name': name,
            'stars': stars,
            'description': description,
            'forks': forks,
            'language': language
        })
    
    # Most popular language by the number of repositories
    most_popular_language = Counter(languages).most_common(1)[0][0]
    
    # Top 5 repositories by star count
    top_5_repositories = sorted(repo_details, key=lambda x: x['stars'], reverse=True)[:5]
    top_5_repositories_name_stars = [{"name": item["name"], "stars": item["stars"]} for item in top_5_repositories]
    
    return {
        'total_repositories': len(repos),
        'total_stars': total_stars,
        'most_popular_language': most_popular_language,
        'top_5_repositories': top_5_repositories_name_stars
    }

def display_results(result):
    """Print the final results in a structured JSON format."""
    print(json.dumps(result, indent=4))

def main():
    """Main function to run the process for a user-provided GitHub organization."""
    # Accept user input for organization name
    organization = input("Enter the GitHub organization name: ").strip()
    
    if not organization:
        print("Organization name cannot be empty.")
        return

    print(f"Retrieving repositories for organization: {organization}")
    
    # Retrieve repository data
    repos = get_repos(organization)
    
    # Analyze and process the data
    result = analyze_repos(repos)
    
    # Output the result in the required format
    display_results(result)

if __name__ == "__main__":
    main()
    # Example input organization
    # organization = "google"
    # main(organization)
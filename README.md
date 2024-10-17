GitHub Repository Data Analyzer
This Python application interacts with the GitHub API to retrieve, process, and analyze repository data for a given organization. It handles authentication, pagination, and processes large datasets efficiently. The program returns the total number of repositories, total stars, the most popular programming language, and the top 5 most-starred repositories.

Prerequisites
Before running the script, ensure you have the following prerequisites installed:

Python 3.x: The project is built using Python.
GitHub Personal Access Token (PAT): A GitHub PAT is required to authenticate and interact with the GitHub API.

How to Run the Script
Ensure all dependencies are installed and the .env file (with GitHub PAT) is properly set up.
Run the Python script using: python github_repo_analysis.py
You will be prompted to input the GitHub organization name (e.g. google or microsoft).
The script will retrieve and analyze the repository data, then display the results in a structured format.

Example Input:
organization = "google"

Example Output:
Retrieving repositories for organization: google
{
    "total_repositories": 2677,
    "total_stars": 1852789,
    "most_popular_language": "Python",
    "top_5_repositories": [
        {"name": "material-design-icons","stars": 50528},
        {"name": "guava","stars": 50121},
        {"name": "zx","stars": 42959},
        {"name": "styleguide","stars": 37354},
        {"name": "leveldb","stars": 36379}
    ]
}

Error Handling
The script includes robust error handling mechanisms, including:

Authentication Errors:
If the GitHub PAT is invalid or missing, the script will print an error message and exit.

Rate Limits:
GitHub limits the number of API requests per hour. If the rate limit is exceeded, the script will notify you and wait for 1 minute before retrying.

Network Errors:
If the script encounters network-related issues (e.g., timeouts), it uses exponential backoff to retry requests.

General API Errors:
If the API returns any error responses, they are handled gracefully and printed to the console.

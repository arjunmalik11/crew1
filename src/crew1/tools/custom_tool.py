from langchain.tools import tool
from crewai import tools
import requests
import os
import json

class SearchTools:
    @tool('search python')
    def search_python(query: str) -> str:
        """
        Use this tool to search in Python documentation.
        This tool returns 5 results from python.org pages.
        """
        return SearchTools.perform_search(f"site:https://www.python.org/ {query}", max_results=5)

    @staticmethod
    def perform_search(query, max_results=5):
        # Base URL and API Key for the SERPer search engine
        search_url = "https://google.serper.dev/search"
        api_key = os.getenv("SERPER_API_KEY")  # Ensure SERPER_API_KEY is set in the environment

        # Constructing the payload for the POST request
        search_payload = {
            "q": query,
            "num": max_results,
        }

        # Setting up the headers with the API Key
        search_headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }

        # Making the POST request and parsing the JSON response
        response = requests.post(search_url, headers=search_headers, json=search_payload)
        search_results = response.json().get('organic', [])

        # Formatting the search results into a string
        result_str = [f"{result['title']}\n{result['snippet']}\n{result['link']}\n" for result in search_results]
        formatted_results = "Search results for '{}':\n\n{}".format(query, "\n\n".join(result_str))

        return formatted_results

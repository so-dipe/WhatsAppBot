import requests
from bs4 import BeautifulSoup
import re
from config.config import Config


def search(query):
    """
    This function sends a post request to the google search webhook
    and returns the response.

    Args:
        query (str): The query to search for.

    Returns:
        dict: The response from the google search webhook.
    """
    url = (
        f"{Config.GOOGLE_SEARCH_URL}?key={Config.GOOGLE_SEARCH_API_KEY}"
        f"&cx={Config.GOOGLE_SEARCH_ENGINE_ID}&q={query}"
    )
    try:
        response = requests.get(url)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to google search: {str(e)}")
        return None


def parse_search_results(response):
    data = response.get("items")
    results = []
    for item in data:
        result = {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet"),
        }
        results.append(result)
    return results


def get_content_from_url(url):
    try:
        response = requests.get(url)
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error opening link: {str(e)}")
        return None


def clean_content(content):
    soup = BeautifulSoup(content, "html.parser")
    content = soup.get_text()
    content = content.strip().replace("\n", " ")
    content = re.sub(r"\s+", " ", content)
    return content


def retrieve_content(query):
    response = search(query)
    response = parse_search_results(response)
    contents = []
    for url in response.values():
        content = get_content_from_url(url)
        content = clean_content(content)
        contents.append(content)
    return contents


def get_search_results(query):
    response = search(query)
    response = parse_search_results(response)
    return str(response)


def view_link(url):
    content = get_content_from_url(url)
    content = clean_content(content)
    return content

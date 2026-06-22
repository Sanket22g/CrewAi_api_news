from crewai.tools import BaseTool
from pydantic import Field, BaseModel
from typing import Type
from googleapiclient.discovery import build
import os
import requests
from bs4 import BeautifulSoup

class YouTubeSearchInput(BaseModel):
    query: str = Field(..., description="The search query string for YouTube videos.")

class YouTubeSearchTool(BaseTool):
    name: str = "YouTube Video Search"
    description: str = (
        "Searches YouTube for videos on a given topic. "
        "Returns a list of video titles, URLs, and channel names. "
        "Input should be a search query string."
    )
    args_schema: Type[BaseModel] = YouTubeSearchInput
    max_results: int = 5 
    def _run(self, query: str) -> str:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return "Error: YOUTUBE_API_KEY not found in environment variables."

        youtube = build("youtube", "v3", developerKey=api_key)

        response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=self.max_results,  
            order="relevance"
        ).execute()

        results = []
        for item in response.get("items", []):
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            channel = item["snippet"]["channelTitle"]
            results.append(f"Title: {title}\nURL: {url}\nChannel: {channel}")

        return "\n\n".join(results) if results else "No videos found."

class GithubTrendingInput(BaseModel):
    since: str = Field("daily", description="Time range for trending: daily, weekly, or monthly. Defaults to daily.")

class GithubTrendingTool(BaseTool):
    name: str = "Github Trending Repositories"
    description: str = (
        "Scrapes the GitHub trending page to fetch top starred repositories of the day. "
        "Returns the top repository's name, owner, URL, description, stars, and language."
    )
    args_schema: Type[BaseModel] = GithubTrendingInput

    def _run(self, since: str = "daily") -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        url = f"https://github.com/trending?since={since}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return f"Error: Status code {response.status_code}"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            for article in soup.select('article.Box-row'):
                title_el = article.select_one('h2 a')
                if not title_el:
                    continue
                href = title_el['href']
                name = href.strip('/')
                owner, repo_name = name.split('/', 1) if '/' in name else ("", name)
                repo_url = f"https://github.com/{name}"
                
                desc_el = article.select_one('p')
                description = desc_el.text.strip() if desc_el else ""
                
                lang_el = article.select_one('[itemprop="programmingLanguage"]')
                language = lang_el.text.strip() if lang_el else "Unknown"
                
                stars_el = article.select_one('a[href$="/stargazers"]')
                stars_str = stars_el.text.strip().replace(',', '') if stars_el else "0"
                
                return (
                    f"Name: {repo_name}\n"
                    f"Owner: {owner}\n"
                    f"URL: {repo_url}\n"
                    f"Description: {description}\n"
                    f"Stars: {stars_str}\n"
                    f"Language: {language}"
                )
            return "No trending repositories found."
        except Exception as e:
            return f"Exception occurred while fetching: {e}"


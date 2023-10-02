import requests
import settings


class requestHandler:
    def __init__(self, query) -> None:
        self.query = query

    def __str__(self) -> str:
        return f"query: {self.query}"

    def API_getWolfram(self):
        wolfram_ID = settings.WOLFRAM_API_ID
        url = f"https://api.wolframalpha.com/v1/conversation.jsp?appid={wolfram_ID}&i={self.query}%3f"
        response = requests.get(url)
        # TODO: Handle different url responses 
        return response
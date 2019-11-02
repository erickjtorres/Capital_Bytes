from typing import List

class ArticleSummary:
    def __init__(self, content: str, title: str):
        self.content = content
        self.title = title

class ArticlesSummaries:
    def __init__(self, articles: List[dict]):
        self.articles = articles
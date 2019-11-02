from newsdatascraper import Scraper
new_scraper = Scraper('mock-api')

def get_news_articles(company_name, number_of_articles = 3):
    articles = new_scraper.fetch_all_articles(query=company_name, pageSize = number_of_articles)
    return articles

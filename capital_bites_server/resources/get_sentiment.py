from flask_restful import Resource, reqparse
from resources.helper.get_news_articles import get_news_articles
from resources.helper.get_google_sentiment import analyze_text_sentiment

#https://[heroku_url]/sentiment?companyName=apple
parser = reqparse.RequestParser()
parser.add_argument('companyName', type=str)

class GetCurrentSentimentOfStock(Resource):
  def get(self):
    args = parser.parse_args()
    company_name = args['companyName']
    articles = get_news_articles(company_name)
    total_sentiment = 0
    for article in articles.articles:
        total_sentiment += analyze_text_sentiment(article.content)
    
    return {'current_sentiment': total_sentiment/5}

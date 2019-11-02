from flask import Flask
from flask_restful import Api, reqparse

from resources.main import Main
from resources.get_sentiment import GetCurrentSentimentOfStock
from resources.get_forecast import GetCurrentForecastOfStock
from resources.get_summary import GetSummaryOfArticles
from resources.favorites import Favorites

app = Flask(__name__)
api = Api(app)

api.add_resource(Main, "/")
api.add_resource(GetCurrentSentimentOfStock, "/sentiment")
api.add_resource(GetCurrentForecastOfStock, "/forecast")
api.add_resource(GetSummaryOfArticles, "/summary")
api.add_resource(Favorites, "/favorites")


if __name__ == "__main__":
  app.run()
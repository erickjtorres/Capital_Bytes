from flask_restful import Resource, reqparse
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import GRU
from keras import optimizers
import tensorflow as tf
import requests
import string
import difflib
from resources.helper.get_prediction import make_model, denormalize_data, load_company_data, find_company_name, fetch_stock_data, parse_data, prepare_data, compute_mean_std, name_to_ticker_symbol, normalize_data 

#https://[heroku_url]/forecast?companyName=apple

parser = reqparse.RequestParser()
parser.add_argument('companyName', type=str)


class GetCurrentForecastOfStock(Resource):
  def get(self):
    n_steps = 25 
    epochs = 20

    args = parser.parse_args()
    company_name = args['companyName']
    tf.logging.set_verbosity(tf.logging.ERROR)
    #company_name = input("Enter Company Name>")
    frame = load_company_data()
    clean_companies = [x for x in frame["Name"].tolist() if x]
    companies = [x.split(" ")[0].lower() for x in clean_companies]
    dirty_companies = ["".join([x for x in word if x not in string.punctuation]) for word in companies]

    dirty_2_clean = {}
    for dirty, clean in zip(dirty_companies, clean_companies):
        dirty_2_clean[dirty] = clean
    matches = find_company_name(company_name.lower(), dirty_companies)
    #print("Getting matches to ", matches[0])
    # convert the matched company to a ticker symbol and search.
    bestmatch = dirty_2_clean[matches[0]]
    ticker_symbol = name_to_ticker_symbol(bestmatch, frame)
    data = fetch_stock_data(ticker_symbol)
    data = parse_data(data)
    X, Y = prepare_data(data, n_steps)
    #print(X,Y)
    split = 0.95
    split = int(len(X)*split)
    x_train = X[:split]
    y_train = Y[:split]
    train_mu, train_sigma = compute_mean_std(x_train) # do only on train data

    x_test = X[split:]
    y_test = Y[split:]
    test_mu, test_sigma = compute_mean_std(x_test) # do only on test data


    #print("Training on ", len(x_train), " weeks of data!")
    model = make_model(n_steps, x_train)

    x_train = normalize_data(x_train, train_mu, train_sigma)
    y_train = normalize_data(y_train, train_mu, train_sigma)

    x_test = normalize_data(x_test, test_mu, test_sigma)
    y_test = normalize_data(y_test, test_mu, test_sigma)

    model.fit(x_train, y_train, epochs = epochs)
    #mse, mae = model.evaluate(x_test, y_test)
    #print("MSE | MAE", mse, mae)

    final_predictor = np.expand_dims(x_test[-1], axis=0)
    nextprice = model.predict(final_predictor)
    nextprice = denormalize_data(nextprice[0][0], test_mu, test_sigma)
    master = {} 
    master["current_price"] = str(y_test[-1])
    master["prediction"] = str(nextprice)
    master["company"] = str(bestmatch.split(" ")[0])
    master["ticker"] = str(ticker_symbol)
    return master 
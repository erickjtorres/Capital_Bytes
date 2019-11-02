import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import GRU
from keras import optimizers
import tensorflow as tf
import requests
import difflib
import pymongo

#connect to mongodb database
conn = pymongo.MongoClient("mock-client")

def fetch_stock_data(symbol="AAPL"):
    """
        Gets weekly data for that symbol
    """
    key = "mock-key"
    weekly_series = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + key
    data = requests.get(weekly_series)
    return data.json()


def parse_data(data):
    """
        Shift through keys and get the openning week values.
    """
    alldata = []
    try:
        data['Time Series (Daily)']
    except KeyError:
        return False
    for week in data['Time Series (Daily)']:
        curdat = (float(data['Time Series (Daily)'][week]["2. high"]) + float(data['Time Series (Daily)'][week]["3. low"]))/2
        alldata.append(curdat)
    alldata = alldata[::-1]
    # go through and smooth the curve out (WMA)
    for i in range(1, len(alldata)):
        if i == len(alldata)-1:
            alldata[i] = (alldata[i-1] + (alldata[i])) /2
            continue
        alldata[i] = (alldata[i-1] + (alldata[i]) + alldata[i+1])/3
    return alldata


def compute_mean_std(data):
    """ Compute mean, std. dev, for normalization"""
    return np.mean(data), np.std(data)


def prepare_data(data, seq_length):
    """ Make data into sequence data for RNN"""
    if len(data)-1-seq_length < 0:
        return False
    retdata = []
    retdata_y = []
    for x in range(len(data)-seq_length):
        if x+seq_length < len(data):
            curans = data[x+seq_length]
        else:
            curans = data[-1]
        retdata_y.append(curans)
        cur = data[x:x+seq_length]
        retdata.append(cur)
    retdata = np.asarray(retdata)
    retdata_y = np.asarray(retdata_y)
    retdata = np.expand_dims(retdata, axis=-1)
    return retdata, retdata_y


def make_model(n_steps, x_train):
    """Make RNN"""
    reg_model = Sequential()
    reg_model.add(GRU(n_steps, input_shape=(x_train.shape[1], x_train.shape[-1]), activation = "tanh"))
    reg_model.add(Dense(10, activation = "tanh"))
    reg_model.add(Dense(1))
    reg_model.compile(loss='mean_squared_error', optimizer='adadelta', metrics = ["mae"])
    return reg_model

def normalize_data(data, mu, sigma):
    return np.asarray([(x-mu)/sigma for x in data])

def denormalize_data(scalar, mu, sigma):
    return ((scalar*sigma)+mu)



def load_company_data():
    """  """
    cursor = conn["BytesDatabase"]["Companies"].find({})
    companies =  pd.DataFrame(list(cursor))    
    return companies

def find_company_name(search, companies):
    return difflib.get_close_matches(search.lower(), companies, n = 10, cutoff = 0.3)

def clean_companies(companies):
    """ returns dict with k = clean value and value = real company name (in df)"""
    return {x.split(" ")[0].lower():x for x in companies}

def load_name_to_ticker(companies):
    """returns dict[company_name] -> ticker symbol"""
    #companies = load_company_data()
    master = {}
    for idx, row in companies.iterrows():
        master[row["Name"]] = row['Symbol']
    return master

def name_to_ticker_symbol(company_name, df):
    master = load_name_to_ticker(df)
    return master[company_name]


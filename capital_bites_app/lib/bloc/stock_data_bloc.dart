import 'package:bloc/bloc.dart';
import 'package:capital_bites/bloc/bloc.dart';
import 'package:capital_bites/repository/stock_data_repository.dart';
import 'package:flutter/material.dart';

class StockDataBloc extends Bloc<StockDataEvent, StockDataState> {
  StockDataRepository stockDataRepository;

  StockDataBloc({@required this.stockDataRepository});
  @override
  get initialState => StockDataInitial();

  @override
  Stream<StockDataState> mapEventToState(event) async* {
    if (event is StockDataSearch) {
      yield* mapStockDataSearchToStockDataState(event);
    }
  }

  Stream<StockDataState> mapStockDataSearchToStockDataState(StockDataSearch event) async* {
    yield StockDataLoading();
    try {
      final Sentiment sentiment = await stockDataRepository.getStockSentiment(event.companyName);
      final List<ArticleSummary> articleSummaries = await stockDataRepository.getStockSummaries(event.companyName);
      final Forecast stockDataForecast = await stockDataRepository.getStockPredictions(event.companyName);
      final String imageUrl = await stockDataRepository.getGif(event.companyName);
      

      yield StockDataLoaded(
        stockData: StockData(
          currentPrice: double.parse(stockDataForecast.currentPrice),
          companyName: stockDataForecast.companyName,
          tickerSymbol: stockDataForecast.tickerSymbol,
          forecast: double.parse(stockDataForecast.prediction),
          articleSummaries: articleSummaries,
          sentiment: sentiment.sentiment,
          image: Image(
            image: NetworkImage(imageUrl),
          ),
        ),
      );
    } catch (_) {
      yield StockDataError();
    }
  }
}

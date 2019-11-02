import 'package:capital_bites/repository/stock_data_repository.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

abstract class StockDataState extends Equatable {}

//Model remove once repo gets created
class StockData {
  final String companyName;
  final String tickerSymbol;
  final double forecast;
  final double sentiment;
  final double currentPrice;
  final List<ArticleSummary> articleSummaries;
  final Image image;

  StockData({this.companyName, this.currentPrice, this.articleSummaries, this.image, this.sentiment, this.forecast, this.tickerSymbol});

}

class StockDataInitial extends StockDataState {
  @override
  List<Object> get props => [];

}

class StockDataLoaded extends StockDataState {
  final StockData stockData;

  StockDataLoaded({
    this.stockData,
  });

  @override
  List<Object> get props => [stockData];
}

class StockDataLoading extends StockDataState {
  @override
  List<Object> get props => [];
}

class StockDataError extends StockDataState {
  @override
  List<Object> get props => [null];
}

import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';

abstract class StockDataState extends Equatable {}

//Model remove once repo gets created
class StockData {
  final String companyName;
  final String summary;
  final Image image;

  StockData({this.companyName, this.summary, this.image});

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

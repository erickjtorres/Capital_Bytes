import 'package:bloc/bloc.dart';
import 'package:capital_bites/bloc/bloc.dart';
import 'package:flutter/material.dart';

class StockDataBloc extends Bloc<StockDataEvent, StockDataState> {
  @override
  get initialState => StockDataInitial();

  @override
  Stream<StockDataState> mapEventToState(event) async* {
    if (event is StockDataSearch) {
      yield* mapStockDataSearchToStockDataState();
    }
  }

  Stream<StockDataState> mapStockDataSearchToStockDataState() async* {
    yield StockDataLoading();
    await Future.delayed(
      new Duration(seconds: 1),
    );
    try {
      yield StockDataLoaded(
        stockData: StockData(
          companyName: 'Stock Name',
          summary: 'Some Financial Data and Summaries Here',
          image: Image(
            image: AssetImage('assets/stock_test.gif'),
          ),
        ),
      );
    } catch (_) {
      yield StockDataError();
    }
  }
}

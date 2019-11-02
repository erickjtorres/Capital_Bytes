import 'package:equatable/equatable.dart';

abstract class StockDataEvent extends Equatable {}

class StockDataSearch extends StockDataEvent {
  final String companyName;

  StockDataSearch({
    this.companyName,
  });

  @override
  List<Object> get props => [companyName];
}

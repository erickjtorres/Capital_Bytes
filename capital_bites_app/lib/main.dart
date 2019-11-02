import 'package:capital_bites/search_bar/floating_search_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

import 'bloc/bloc.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final capitalOneColor = Color.fromRGBO(35, 131, 157, 1);
    final StockDataBloc stocBloc = StockDataBloc();
    return MaterialApp(
      title: 'Capital Bites',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          backgroundColor: capitalOneColor,
          title: Text(
            'Capital Bites',
          ),
        ),
        body: Padding(
          padding: EdgeInsets.all(8.0),
          child: FloatingSearchBar(
            endDrawer: Container(),
            onSubmitted: (companyName) {
              stocBloc.add(
                StockDataSearch(
                  companyName: companyName,
                ),
              );
            },
            trailing: Icon(
              Icons.search,
            ),
            children: [
              Padding(
                padding: EdgeInsets.all(8.0),
                child: BlocBuilder<StockDataBloc, StockDataState>(
                  bloc: stocBloc,
                  builder: (context, state) {
                    if (state is StockDataLoading) {
                      return Center(
                        child: Column(
                          children: [
                            Text('Making complex information into small bites!'),
                            SpinKitWave(
                              color: capitalOneColor,
                              size: 50.0,
                            ),
                          ],
                        ),
                      );
                    } else if (state is StockDataLoaded) {
                      return Center(
                        child: Padding(
                          padding: EdgeInsets.all(8.0),
                          child: Column(
                            children: [
                              Text(
                                state.stockData.companyName,
                                style: TextStyle(fontSize: 20),
                              ),
                              state.stockData.image,
                              Row(
                                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                children: [
                                  Column(
                                    children: <Widget>[
                                      Icon(
                                        Icons.tag_faces,
                                        size: 40,
                                        color: Color.fromRGBO(32, 205, 54, 1),
                                      ),
                                      Text('Overall Feeling'),
                                    ],
                                  ),
                                  Column(
                                    children: <Widget>[
                                      Icon(
                                        Icons.trending_up,
                                        size: 40,
                                        color: Color.fromRGBO(32, 205, 54, 1),
                                      ),
                                      Text('Current Forecast'),
                                    ],
                                  ),
                                  
                                ],
                              ),
                              Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: Text(
                                  state.stockData.summary,
                                  textAlign: TextAlign.center,
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    } else {
                      return Center(
                        child: Container(
                          child: Text(
                            'Welcome to Capital Snacks! Search up some stocks!',
                          ),
                        ),
                      );
                    }
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

import 'package:bloc/bloc.dart';
import 'package:capital_bites/bloc/navigation_bloc.dart';
import 'package:capital_bites/chat_room.dart';
import 'package:capital_bites/stock_search.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:hydrated_bloc/hydrated_bloc.dart';

void main() async {
  BlocSupervisor.delegate = await HydratedBlocDelegate.build();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final capitalOneColor = Color.fromRGBO(0, 0, 0, 1);
    final NavigationBloc bloc = NavigationBloc();

    _onItemTapped(int index) {
      bloc.add(index);
    }

    return MaterialApp(
      title: 'Capital Bytes',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          backgroundColor: capitalOneColor,
          title: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Capital Bytes',
              ),
              Padding(
                padding: EdgeInsets.only(left: 2),
                child: Image(
                  image: AssetImage('assets/logo.png'),
                  width: 30,
                ),
              )
            ],
          ),
        ),
        body: BlocBuilder<NavigationBloc, int>(
            bloc: bloc,
            builder: (context, state) {
              if (state == 0) {
                return StockSearch();
              } else {
                return ChatRoom();
              }
            }),
        bottomNavigationBar: BottomNavigationBar(
          onTap: _onItemTapped,
          backgroundColor: Colors.black,
          items: const <BottomNavigationBarItem>[
            BottomNavigationBarItem(
              icon: Icon(Icons.search, color: Colors.white),
              title: Text(
                'Home',
                style: TextStyle(color: Colors.white),
              ),
            ),
            BottomNavigationBarItem(
              icon: Icon(
                Icons.chat,
                color: Colors.white,
              ),
              title: Text(
                'Chat',
                style: TextStyle(color: Colors.white),
              ),
            ),
          ],
          selectedItemColor: Colors.amber[800],
        ),
      ),
    );
  }
}

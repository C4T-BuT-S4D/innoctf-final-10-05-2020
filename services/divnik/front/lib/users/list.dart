import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:front/auxiliary.dart';
import 'package:front/menu.dart';
import 'package:front/session.dart';
import 'package:http/http.dart';

class UserListScreen extends StatefulWidget {
  @override
  _UserListScreenState createState() => _UserListScreenState();
}

class _UserListScreenState extends State<UserListScreen> {
  int page = 1;

  Future<Response> getCourseList() async {
    final response = await Session.get('/users/?page=$page');
    return response;
  }

  void nextPage() {
    setState(() {
      page = page + 1;
    });
  }

  void prevPage() {
    setState(() {
      page = page == 1 ? 1 : page - 1;
    });
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Response>(
      future: getCourseList(),
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return CircularProgressIndicator();
        }

        final response = snapshot.data;

        if (response.statusCode == 404) {
          WidgetsBinding.instance.addPostFrameCallback(
                  (_) => Navigator.of(context).pushNamed('/users'));
          return CircularProgressIndicator();
        }

        if (response.statusCode != 200) {
          WidgetsBinding.instance.addPostFrameCallback(
                  (_) => Navigator.of(context).pushNamed('/'));
          return CircularProgressIndicator();
        }

        final page = jsonDecode(response.body);
        final data = page['results'];

        final headRow = TableRow(children: [
          TableHeadCell(name: "Username"),
          TableHeadCell(name: "Name"),
          TableHeadCell(name: "Profile"),
        ]);

        final dataRows = <TableRow>[];
        for (final each in data) {
          var tableRow = TableRow(children: [
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(each['username']),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(each['first_name'] + " " + each['last_name']),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: new FlatButton(
                color: Colors.blue,
                onPressed: () {
                  Navigator.of(context).pushNamed(
                    '/user',
                    arguments: {'id': each['id']},
                  );
                },
                child: Text("Open"),
              ),
            ),
          ]);
          final row = tableRow;
          dataRows.add(row);
        }

        return Scaffold(
          appBar: DynamicAppBar(),
          body: Container(
            padding: EdgeInsets.all(20.0),
            child: SingleChildScrollView(
              child: Column(children: [
                Table(
                  border: TableBorder.all(width: 1, color: Colors.black),
                  children: [headRow] + dataRows,
                ),
                Row(
                  children: <Widget>[
                    Padding(
                      padding: EdgeInsets.all(8.0),
                      child: FlatButton(
                        color: Colors.blue,
                        onPressed: prevPage,
                        child: Text("Previous page"),
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.all(8.0),
                      child: FlatButton(
                        color: Colors.blue,
                        onPressed: nextPage,
                        child: Text("Next page"),
                      ),
                    ),
                  ],
                )
              ]),
            ),
          ),
        );
      },
    );
  }
}

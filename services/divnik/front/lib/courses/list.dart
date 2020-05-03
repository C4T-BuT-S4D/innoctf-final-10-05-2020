import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:front/auxiliary.dart';
import 'package:front/menu.dart';
import 'package:front/session.dart';
import 'package:http/http.dart';

class CourseListScreen extends StatefulWidget {
  const CourseListScreen({Key key}) : super(key: key);

  @override
  _CourseListScreenState createState() => _CourseListScreenState();
}

class _CourseListScreenState extends State<CourseListScreen> {
  int page = 1;

  Future<Response> getCourseList() async {
    final response = await Session.get('/courses/?page=$page');
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

  void openCourse(id) {
    Navigator.of(context).pushNamed(
      '/course',
      arguments: {'id': id},
    );
  }

  void claimReward(id) async {
    final response = await Session.get('/courses/$id/reward/');
    String title = "";
    if (response.statusCode == 200) {
      title = "Your course reward";
    } else {
      title = "Error!";
    }

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text(title),
          content: SingleChildScrollView(
            child: Text(response.body),
          ),
          actions: <Widget>[
            FlatButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text("OK"),
            ),
          ],
        );
      },
    );
  }

  Future<void> enrollCourse(BuildContext context,
      Map<String, dynamic> course) async {
    final data = {
      'course': course['id'],
    };
    final resp = await Session.post('/relations/', data);
    if (resp.statusCode != 201) {
      showDialog(
        context: context,
        builder: (context) {
          return AlertDialog(
            title: Text("Error!"),
            content: SingleChildScrollView(
              child: Text(resp.body),
            ),
            actions: <Widget>[
              FlatButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                child: Text("OK"),
              ),
            ],
          );
        },
      );
    } else {
      setState(() {});
    }
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
        if (response == null) {
          WidgetsBinding.instance.addPostFrameCallback(
                  (_) => Navigator.of(context).pushNamed('/'));
          return CircularProgressIndicator();
        }
        if (response.statusCode == 401) {
          WidgetsBinding.instance.addPostFrameCallback(
                  (_) => Navigator.of(context).pushNamed('/login'));
          return CircularProgressIndicator();
        }

        if (response.statusCode == 404) {
          WidgetsBinding.instance.addPostFrameCallback(
                  (_) => Navigator.of(context).pushNamed('/courses'));
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
          TableHeadCell(name: "ID"),
          TableHeadCell(name: "Name"),
          TableHeadCell(name: "Finished"),
          TableHeadCell(name: "Action"),
        ]);
        final dataRows = <TableRow>[];
        for (final each in data) {
          FlatButton actionButton;
          if (each['is_enrolled']) {
            if (each['is_finished']) {
              actionButton = FlatButton(
                color: Colors.blue,
                onPressed: () async {
                  await claimReward(each['id']);
                },
                child: Text(
                  "Claim reward!",
                ),
              );
            } else {
              actionButton = FlatButton(
                color: Colors.blue,
                onPressed: () {
                  openCourse(each['id']);
                },
                child: Text(
                  "Open",
                ),
              );
            }
          } else {
            actionButton = FlatButton(
              color: Colors.blue,
              onPressed: () async {
                await enrollCourse(context, each);
              },
              child: Text(
                "Enroll",
              ),
            );
          }
          var tableRow = TableRow(children: [
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(each['id'].toString()),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Column(children: [
                Text(each['name']),
                Tooltip(
                  message: each['description'],
                  child: FlatButton(
                    onPressed: null,
                    child: Text("Info"),
                  ),
                )
              ]),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(each['is_finished'] ? 'Yes' : 'No'),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: actionButton,
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
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: <Widget>[
                    FlatButton(
                      onPressed: () {
                        Navigator.of(context).pushNamed('/course_create');
                      },
                      color: Colors.blue,
                      child: Text('Create course'),
                    ),
                  ],
                ),
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

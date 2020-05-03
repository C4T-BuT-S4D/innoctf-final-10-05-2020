import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:front/auxiliary.dart';
import 'package:front/menu.dart';
import 'package:front/models.dart';
import 'package:front/session.dart';
import 'package:http/http.dart';
import 'package:provider/provider.dart';

class CourseDataResponse {
  final Response courseResponse;
  final Response gradesResponse;
  final Response relationsResponse;

  CourseDataResponse(
      this.courseResponse, this.gradesResponse, this.relationsResponse);

  int getErrorStatusCode() {
    if (courseResponse.statusCode != 200) {
      return courseResponse.statusCode;
    }
    if (gradesResponse.statusCode != 200) {
      return gradesResponse.statusCode;
    }
    if (relationsResponse.statusCode != 200) {
      return relationsResponse.statusCode;
    }

    return 200;
  }
}

class CourseGradeAlertDialog extends StatefulWidget {
  final List participants;
  final int courseId;

  const CourseGradeAlertDialog({Key key, this.participants, this.courseId})
      : super(key: key);

  @override
  _CourseGradeAlertDialogState createState() =>
      _CourseGradeAlertDialogState(participants, courseId);
}

class _CourseGradeAlertDialogState extends State<CourseGradeAlertDialog> {
  final List participants;
  final int courseId;

  int _participantChoice = 0;
  final _participantGrade = TextEditingController();
  final _comment = TextEditingController();
  String _errorText = "";

  _CourseGradeAlertDialogState(this.participants, this.courseId);

  @override
  Widget build(BuildContext context) {
    List<DropdownMenuItem<int>> choices = [];
    for (final part in participants) {
      choices.add(DropdownMenuItem<int>(
        child: Text(part['user_username']),
        value: part['id'],
      ));
    }
    final form = Form(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Padding(
            padding: EdgeInsets.all(8.0),
            child: DropdownButtonFormField(
              items: choices,
              onChanged: (choice) {
                setState(() {
                  _participantChoice = choice;
                });
              },
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextFormField(
              controller: _participantGrade,
              inputFormatters: [DecimalTextInputFormatter(decimalRange: 1)],
              keyboardType: TextInputType.numberWithOptions(decimal: true),
              decoration: InputDecoration(
                hintText: "Grade",
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextFormField(
              controller: _comment,
              decoration: InputDecoration(
                hintText: "Comment",
              ),
            ),
          ),
          _errorText != ""
              ? Padding(
                  padding: EdgeInsets.all(12.0),
                  child: Text(
                    _errorText,
                    style: TextStyle(color: Colors.red),
                  ))
              : Text(""),
        ],
      ),
    );

    return AlertDialog(
      title: Text("Grade a participant"),
      content: SingleChildScrollView(
        child: form,
      ),
      actions: <Widget>[
        FlatButton(
          onPressed: () {
            Navigator.of(context).pop();
          },
          child: Text("Cancel"),
        ),
        FlatButton(
          onPressed: () async {
            final data = {
              'rel': _participantChoice,
              'value': _participantGrade.text,
              'comment': _comment.text,
            };
            final response = await Session.post('/grades/', data);
            if (response.statusCode != 201) {
              setState(() {
                _errorText = response.body;
              });
            } else {
              Navigator.of(context).pop();
              Navigator.of(context).pushNamed(
                '/course',
                arguments: {'id': courseId},
              );
            }
          },
          child: Text("Submit"),
        ),
      ],
    );
  }
}

class CourseViewScreen extends StatefulWidget {
  @override
  _CourseViewScreenState createState() => _CourseViewScreenState();
}

class _CourseViewScreenState extends State<CourseViewScreen> {
  Future<CourseDataResponse> getCourse(BuildContext context) async {
    final Map<String, dynamic> args = ModalRoute.of(context).settings.arguments;
    if (args == null) {
      WidgetsBinding.instance.addPostFrameCallback(
          (_) => Navigator.of(context).pushNamed('/courses'));
      return null;
    }
    final courseId = args['id'];

    final courseResponse = await Session.get('/courses/$courseId/');
    final gradesResponse = await Session.get('/grades/?rel__course=$courseId');
    final relationsResponse = await Session.get('/relations/?course=$courseId');
    return CourseDataResponse(
        courseResponse, gradesResponse, relationsResponse);
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<CourseDataResponse>(
      future: getCourse(context),
      builder: (context, snapshot) {
        if (snapshot.connectionState != ConnectionState.done) {
          return CircularProgressIndicator();
        }

        final response = snapshot.data;
        if (response == null) {
          WidgetsBinding.instance.addPostFrameCallback(
              (_) => Navigator.of(context).pushNamed('/courses'));
          return CircularProgressIndicator();
        }

        if (response.getErrorStatusCode() == 401) {
          WidgetsBinding.instance.addPostFrameCallback(
              (_) => Navigator.of(context).pushNamed('/login'));
          return CircularProgressIndicator();
        }

        if (response.getErrorStatusCode() != 200) {
          WidgetsBinding.instance.addPostFrameCallback(
              (_) => Navigator.of(context).pushNamed('/courses'));
          return CircularProgressIndicator();
        }

        final user = Provider.of<UserModel>(context, listen: true);
        if (!user.authenticated) {
          WidgetsBinding.instance.addPostFrameCallback(
              (_) => Navigator.of(context).pushNamed('/login'));
          return CircularProgressIndicator();
        }

        final courseData = jsonDecode(response.courseResponse.body);
        final gradeData = jsonDecode(response.gradesResponse.body);
        final relationsData = jsonDecode(response.relationsResponse.body);

        final participants =
            relationsData.expand((e) => [if (e['level'] == 'P') e]).toList();

        final teachers =
            relationsData.expand((e) => [if (e['level'] == 'T') e]).toList();

        Map<int, List> mappedGrades = {};
        for (final each in gradeData) {
          if (mappedGrades[each['user']] == null) {
            mappedGrades[each['user']] = [];
          }
          mappedGrades[each['user']].add(each);
        }

        final headRow = TableRow(
          children: [
            TableHeadCell(name: "Participant"),
            TableHeadCell(name: "Grades"),
          ],
        );

        final List<TableRow> dataRows = [];
        for (final part in participants) {
          List<Widget> gradeButtons = [];
          if (mappedGrades[part['user']] != null) {
            gradeButtons = mappedGrades[part['user']]
                .map(
                  (e) => FlatButton(
                    onPressed: () async {
                      await requestGradeComment(e['id']);
                    },
                    child: Text(e['value'].toString()),
                    color: Colors.blue,
                    padding: EdgeInsets.symmetric(
                      horizontal: 12.0,
                      vertical: 5.0,
                    ),
                  ),
                )
                .toList();
          }
          dataRows.add(
            TableRow(
              children: [
                TableHeadCell(name: part['user_username']),
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: gradeButtons,
                ),
              ],
            ),
          );
        }

        final List<Widget> teachersButtons = [];
        bool isTeacher = false;
        for (final teacher in teachers) {
          if (teacher['user'] == user.id) {
            isTeacher = true;
          }
          teachersButtons.add(
            FlatButton(
              onPressed: () {
                Navigator.of(context).pushNamed(
                  '/user',
                  arguments: {'id': teacher['user']},
                );
              },
              child: Text(teacher['user_username']),
            ),
          );
        }

        return Scaffold(
          appBar: DynamicAppBar(),
          body: Container(
            padding: EdgeInsets.all(20.0),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Text(
                      "Course \"${courseData['name']}\"",
                      style: TextStyle(
                        fontSize: 24.0,
                        fontWeight: FontWeight.bold,
                      ),
                    )
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Text(courseData['description']),
                    )
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.start,
                  children: <Widget>[
                        Text(
                          'Course teachers:',
                          style: TextStyle(
                            fontSize: 18.0,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ] +
                      teachersButtons,
                ),
                Table(
                  border: TableBorder.all(width: 1, color: Colors.black),
                  children: [headRow] + dataRows,
                ),
                isTeacher
                    ? Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: FlatButton(
                          onPressed: () {
                            showDialog(
                              context: context,
                              builder: (context) => CourseGradeAlertDialog(
                                participants: participants,
                                courseId: courseData['id'],
                              ),
                            );
                          },
                          child: Text('Grade a participant'),
                          color: Colors.blue,
                        ),
                      )
                    : Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: Text('You are a participant of this course'),
                      ),
              ],
            ),
          ),
        );
      },
    );
  }

  requestGradeComment(id) async {
    final response = await Session.get('/grades/$id/comment/');
    String title = "";
    if (response.statusCode == 200) {
      title = "Your grade comment";
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
}

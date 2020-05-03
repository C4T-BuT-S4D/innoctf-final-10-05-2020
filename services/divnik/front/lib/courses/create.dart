import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:front/menu.dart';
import 'package:front/models.dart';
import 'package:front/session.dart';

class CourseCreateScreen extends StatefulWidget {
  @override
  _CourseCreateScreenState createState() => _CourseCreateScreenState();
}

class _CourseCreateScreenState extends State<CourseCreateScreen> {
  final _nameTextController = TextEditingController();
  final _descriptionTextController = TextEditingController();
  final _rewardTextController = TextEditingController();
  var isLoading = false;
  var errorText = "";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: DynamicAppBar(),
        body: Form(
          child: isLoading
              ? Center(
            child: CircularProgressIndicator(),
          )
              : Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                'Create course',
                style: Theme
                    .of(context)
                    .textTheme
                    .headline4,
              ),
              Padding(
                padding: EdgeInsets.all(8.0),
                child: TextFormField(
                  controller: _nameTextController,
                  decoration: InputDecoration(hintText: 'Name'),
                ),
              ),
              Padding(
                padding: EdgeInsets.all(8.0),
                child: TextFormField(
                  controller: _descriptionTextController,
                  decoration: InputDecoration(hintText: 'Description'),
                ),
              ),
              Padding(
                padding: EdgeInsets.all(8.0),
                child: TextFormField(
                  controller: _rewardTextController,
                  decoration: InputDecoration(hintText: 'Reward'),
                ),
              ),
              errorText != ""
                  ? Padding(
                  padding: EdgeInsets.all(12.0),
                  child: Text(
                    errorText,
                    style: TextStyle(color: Colors.red),
                  ))
                  : Text(""),
              FlatButton(
                color: Colors.blue,
                textColor: Colors.white,
                onPressed: _submitForm,
                child: Text('Submit'),
              ),
            ],
          ),
        ));
  }

  void _submitForm() async {
    setState(() {
      isLoading = true;
    });

    final formData = CourseCreateModel(
      _nameTextController.text,
      _descriptionTextController.text,
      _rewardTextController.text,
    );

    try {
      final resp = await Session.post('/courses/', formData);
      if (resp.statusCode == 201) {
        final data = jsonDecode(resp.body);
        Navigator.of(context)
            .pushNamed('/course', arguments: {'id': data['id']});
      } else {
        errorText = resp.body;
      }
    } catch (e) {
      print(e);
    }

    setState(() {
      isLoading = false;
    });
  }
}

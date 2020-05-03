import 'dart:convert';

import 'package:flutter/material.dart';

class RegisterModel {
  final String firstName;
  final String lastName;
  final String username;
  final String password;

  RegisterModel(this.firstName, this.lastName, this.username, this.password);

  Map<String, dynamic> toJson() => {
        'first_name': this.firstName,
        'last_name': this.lastName,
        'username': this.username,
        'password': this.password,
      };
}

class LoginModel {
  final String username;
  final String password;

  LoginModel(this.username, this.password);

  Map<String, dynamic> toJson() => {
        'username': this.username,
        'password': this.password,
      };
}

class CourseCreateModel {
  final String name;
  final String description;
  final String reward;

  CourseCreateModel(this.name, this.description, this.reward);

  Map<String, dynamic> toJson() => {
        'name': this.name,
        'description': this.description,
        'reward': this.reward,
        'is_finished': false,
      };
}

class CourseRelation {
  final int userId;
  final String userUsername;
  final int courseId;
  final String courseName;
  final String level;

  CourseRelation(this.userId, this.userUsername, this.courseId, this.courseName,
      this.level);
}

class UserModel extends ChangeNotifier {
  bool authenticated = false;
  int id = 0;
  String username = "";
  String firstName = "";
  String lastName = "";
  List<CourseRelation> courseRels = [];

  void parseResponse(response) {
    final data = jsonDecode(response.body);
    id = data['id'];
    username = data['username'];
    firstName = data['first_name'];
    lastName = data['last_name'];

    for (var rel in data['uc_rels']) {
      final parsedRel = CourseRelation(
        rel['user'],
        rel['user_username'],
        rel['course'],
        rel['course_name'],
        rel['level'],
      );
      courseRels.add(parsedRel);
    }
    authenticated = true;
    notifyListeners();
  }

  String fullName() {
    return '$firstName $lastName';
  }
}

import 'package:flutter/material.dart';
import 'package:front/courses/create.dart';
import 'package:front/courses/list.dart';
import 'package:front/courses/view.dart';
import 'package:front/users/list.dart';
import 'package:front/users/login.dart';
import 'package:front/users/profile.dart';
import 'package:front/users/register.dart';
import 'menu.dart';
import 'models.dart';
import 'package:scoped_model/scoped_model.dart';

void main() => runApp(DivnikApp());

class DivnikApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return new ScopedModel<UserModel>(
        model: new UserModel(),
        child: MaterialApp(
          routes: {
            '/register': (context) => RegisterScreen(),
            '/login': (context) => LoginScreen(),
            '/users': (context) => UserListScreen(),
            '/user': (context) => UserProfileScreen(),
            '/course': (context) => CourseViewScreen(),
            '/courses': (context) => CourseListScreen(),
            '/course_create': (context) => CourseCreateScreen(),
          },
          home: WelcomeScreen(),
        ));
  }
}

class WelcomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: DynamicAppBar(),
      body: Container(
        margin: EdgeInsets.all(10),
        child: Center(
          child: Column(children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "Hi!",
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text("Welcome to Divnik, a simple online school diary."),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text("You can create courses and take part in others."),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: FlatButton(
                    color: Colors.blue,
                    onPressed: () =>
                        Navigator.of(context).pushNamed('/courses'),
                    child: Text("Show all courses"),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: FlatButton(
                    color: Colors.blue,
                    onPressed: () => Navigator.of(context).pushNamed('/users'),
                    child: Text("Show other users"),
                  ),
                ),
              ],
            ),
          ]),
        ),
      ),
    );
  }
}

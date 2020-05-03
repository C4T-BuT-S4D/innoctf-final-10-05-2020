import 'package:flutter/material.dart';
import 'package:front/courses/relationTable.dart';
import 'package:front/menu.dart';
import 'package:front/models.dart';
import 'package:front/session.dart';
import 'package:http/http.dart';

class UserProfileScreen extends StatefulWidget {
  @override
  _UserProfileScreenState createState() => _UserProfileScreenState();
}

class _UserProfileScreenState extends State<UserProfileScreen> {
  Future<Response> getUser(BuildContext context) async {
    final Map<String, dynamic> args = ModalRoute
        .of(context)
        .settings
        .arguments;
    if (args == null) {
      WidgetsBinding.instance
          .addPostFrameCallback((_) => Navigator.of(context).pushNamed('/'));
      return null;
    }
    final userId = args['id'];

    final response = await Session.get('/users/$userId/');
    return response;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Response>(
        future: getUser(context),
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return CircularProgressIndicator();
          }

          final response = snapshot.data;
          if (response == null) {
            return CircularProgressIndicator();
          }

          if (response.statusCode != 200) {
            WidgetsBinding.instance.addPostFrameCallback(
                    (_) => Navigator.of(context).pushNamed('/'));
            return CircularProgressIndicator();
          }

          final res = UserModel();
          res.parseResponse(response);

          return Scaffold(
            appBar: DynamicAppBar(),
            body: Center(
                child: Padding(
                  padding: EdgeInsets.all(10.0),
                  child: Center(
                    child: Column(
                      children: <Widget>[
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Container(
                              margin: EdgeInsets.all(25.0),
                              child: Text(
                                'User ${res.username}, ${res.fullName()}',
                                style: TextStyle(
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ],
                        ),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Container(
                              margin: EdgeInsets.all(25.0),
                              child: Text(
                                'User courses:',
                                style: TextStyle(
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ],
                        ),
                        CourseRelationTable(relations: res.courseRels),
                      ],
                    ),
                  ),
                )),
          );
        });
  }
}

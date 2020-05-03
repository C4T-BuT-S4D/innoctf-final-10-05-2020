import 'package:flutter/material.dart';
import 'package:front/session.dart';
import 'package:http/http.dart';

import 'models.dart';

class DynamicAppBar extends StatefulWidget implements PreferredSizeWidget {
  @override
  _DynamicAppBarState createState() => _DynamicAppBarState();

  @override
  final Size preferredSize;

  DynamicAppBar({Key key})
      : preferredSize = Size.fromHeight(kToolbarHeight),
        super(key: key);
}

class _DynamicAppBarState extends State<DynamicAppBar> {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Response>(
      future: Session.setCurrentUser(context),
      builder: (context, snapshot) {
        final logRegAppBar = AppBar(
          title: const Text("Divnik"),
          actions: <Widget>[
            FlatButton(
              color: Colors.blue,
              textColor: Colors.white,
              onPressed: () {
                Navigator.of(context).pushNamed("/login");
              },
              child: Text('Login'),
            ),
            FlatButton(
              color: Colors.blue,
              textColor: Colors.white,
              onPressed: () {
                Navigator.of(context).pushNamed("/register");
              },
              child: Text('Register'),
            ),
          ],
        );
        if (snapshot.connectionState != ConnectionState.done) {
          return logRegAppBar;
        }
        final response = snapshot.data;
        if (response.statusCode ~/ 100 == 4) {
          return logRegAppBar;
        }

        final user = UserModel.of(context);

        final userAppBar = AppBar(
          title: const Text("Divnik"),
          actions: <Widget>[
            FlatButton(
              color: Colors.blue,
              textColor: Colors.white,
              onPressed: () {
                Navigator.of(context)
                    .pushNamed('/user', arguments: {'id': user.id});
              },
              child: Text(user.username),
            ),
          ],
        );

        return userAppBar;
      },
    );
  }
}

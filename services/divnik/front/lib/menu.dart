import 'package:flutter/material.dart';
import 'package:front/session.dart';
import 'package:http/http.dart';
import 'package:provider/provider.dart';

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
    return Consumer<UserModel>(
      builder: (context, user, child) {
        if (!user.authenticated) {
          return AppBar(
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
          ;
        } else {
          return AppBar(
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
        }
      },
    );
  }
}

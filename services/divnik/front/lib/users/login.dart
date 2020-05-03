import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:front/menu.dart';
import 'package:front/models.dart';
import 'package:front/session.dart';

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: DynamicAppBar(),
      backgroundColor: Colors.grey[200],
      body: Center(
        child: SizedBox(
          width: 400,
          child: Card(
            child: LoginForm(),
          ),
        ),
      ),
    );
  }
}

class LoginForm extends StatefulWidget {
  @override
  _LoginFormState createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _usernameTextController = TextEditingController();
  final _passwordTextController = TextEditingController();

  var isLoading = false;
  var errorText = "";

  @override
  Widget build(BuildContext context) {
    return Form(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            'Login',
            style: Theme.of(context).textTheme.headline4,
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextFormField(
              controller: _usernameTextController,
              decoration: InputDecoration(hintText: 'Username'),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextFormField(
              controller: _passwordTextController,
              decoration: InputDecoration(hintText: 'Password'),
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
    );
  }

  void _submitForm() async {
    setState(() {
      isLoading = true;
    });

    final formData = LoginModel(
      _usernameTextController.text,
      _passwordTextController.text,
    );

    try {
      final resp = await Session.post('/login/', formData);
      if (resp.statusCode == 200) {
        final data = json.decode(resp.body);
        Session.token = data['token'];
        Session.setCurrentUser(context);
        Navigator.of(context).pushNamed('/');
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

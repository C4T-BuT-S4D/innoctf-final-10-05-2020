import 'package:front/menu.dart';
import 'package:front/session.dart';
import 'package:front/models.dart';

import 'package:flutter/material.dart';

class RegisterScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: DynamicAppBar(),
      backgroundColor: Colors.grey[200],
      body: Center(
        child: SizedBox(
          width: 400,
          child: Card(
            child: RegisterForm(),
          ),
        ),
      ),
    );
  }
}

class RegisterForm extends StatefulWidget {
  @override
  _RegisterFormState createState() => _RegisterFormState();
}

class _RegisterFormState extends State<RegisterForm> {
  final _firstNameTextController = TextEditingController();
  final _lastNameTextController = TextEditingController();
  final _usernameTextController = TextEditingController();
  final _passwordTextController = TextEditingController();
  var isLoading = false;
  var errorText = "";

  @override
  Widget build(BuildContext context) {
    return Form(
      child: isLoading
          ? Center(
        child: CircularProgressIndicator(),
      )
          : Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            'Register',
            style: Theme
                .of(context)
                .textTheme
                .headline4,
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextFormField(
              controller: _firstNameTextController,
              decoration: InputDecoration(hintText: 'First name'),
            ),
          ),
          Padding(
            padding: EdgeInsets.all(8.0),
            child: TextFormField(
              controller: _lastNameTextController,
              decoration: InputDecoration(hintText: 'Last name'),
            ),
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
            child: Text('Sign up'),
          ),
        ],
      ),
    );
  }

  void _submitForm() async {
    setState(() {
      isLoading = true;
    });

    final formData = RegisterModel(
      _firstNameTextController.text,
      _lastNameTextController.text,
      _usernameTextController.text,
      _passwordTextController.text,
    );

    try {
      final resp = await Session.post('/users/', formData);
      if (resp.statusCode == 201) {
        Navigator.of(context).pushNamed('/login');
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

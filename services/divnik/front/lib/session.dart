import 'dart:convert';
import 'dart:html';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'models.dart';

class Session {
  static Map<String, String> headers = {
    'Content-Type': 'application/json',
  };

  static String token = "";

  static String getApiUrl() {
    final origin = window.location.origin;
    if (origin.contains('localhost')) {
      return 'http://127.0.0.1:8910/api';
    }
    return origin + '/api';
  }

  static Future<http.Response> get(String url) async {
    url = getApiUrl() + url;
    final reqHeaders = headers;
    if (token != "") {
      reqHeaders['Authorization'] = 'Token ' + token;
    }
    http.Response response = await http.get(url, headers: reqHeaders);
    return response;
  }

  static Future<http.Response> post(String url, dynamic data) async {
    url = getApiUrl() + url;
    final reqHeaders = headers;
    if (token != "") {
      reqHeaders['Authorization'] = 'Token ' + token;
    }
    http.Response response =
    await http.post(url, body: json.encode(data), headers: reqHeaders);
    return response;
  }

  static Future<http.Response> setCurrentUser(BuildContext context) async {
    final response = await get('/me/');
    if (response.statusCode == 200) {
      UserModel.of(context).parseResponse(response);
    }
    return response;
  }
}

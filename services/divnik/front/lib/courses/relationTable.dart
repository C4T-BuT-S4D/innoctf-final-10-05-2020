import 'package:flutter/material.dart';
import 'package:front/auxiliary.dart';
import 'package:front/models.dart';

class CourseRelationTable extends StatefulWidget {
  final List<CourseRelation> relations;

  const CourseRelationTable({Key key, @required this.relations})
      : super(key: key);

  @override
  _CourseRelationTableState createState() =>
      _CourseRelationTableState(relations);
}

class _CourseRelationTableState extends State<CourseRelationTable> {
  final List<CourseRelation> relations;

  _CourseRelationTableState(this.relations);

  @override
  Widget build(BuildContext context) {
    final headRow = TableRow(
      children: [
        TableHeadCell(name: "Course ID"),
        TableHeadCell(name: "Course name"),
        TableHeadCell(name: "Participation level"),
      ],
    );

    final dataRows = <TableRow>[];
    for (final each in relations) {
      var tableRow = TableRow(children: [
        Padding(
          padding: EdgeInsets.all(8.0),
          child: Text(each.courseId.toString()),
        ),
        Padding(
          padding: EdgeInsets.all(8.0),
          child: Text(each.courseName),
        ),
        Padding(
          padding: EdgeInsets.all(8.0),
          child: Text(each.level),
        ),
      ]);
      final row = tableRow;
      dataRows.add(row);
    }

    return Table(
      border: TableBorder.all(width: 1, color: Colors.black),
      children: [headRow] + dataRows,
    );
  }
}

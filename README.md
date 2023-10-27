# Student-Information-Management-System
The final version of SCUT MIS for Database Course Design

## How to use

Just simply run the *Login.exe* then you can access the MIS.

## Design Details

- The UI part was accomplished with *tkinter* library in Python. 

- The Database was supported by *SQLite 3*, which is also a library in Python.

- The User information part was accomplished using *pickle* library in Python.

The detail information and requirements of MIS follow as below:

It is used to manage the information about courses and scores. It can record, modify, query, and get statistical data about the students’ and courses’ information.

**Students’ information** includes: student’s ID, Name, Sex, Entrance Age, Entrance Year and Class. The Sex must be male or female. The Entrance Age is between 10 and 50. The length of student’s ID is 10.
 
**Courses’ information** includes: course’s ID, Name, Teacher’s ID, Credit, Grade (which grade can take this course), Canceled Year (can be null). The length of course’s ID is 7. Only if a student’s grade is larger than the course’s Grade and he/she chose the course earlier than the course’s Canceled Year, the course can be choose.

**Teachers’ information** includes: teacher’s ID (the length is 5), Name, Courses (that he/she can teach).

**Course choosing information** includes: student’s ID, course’s ID, Teacher’s ID, Chosen year, Score. Student’s ID is a foreign key pointing to Students’ information. Course’s ID is a foreign key pointing to Courses’ information. Teacher’s ID is a foreign key pointing to Teachers’ information. If a student drops out, his/her course choosing information need to be deleted.

1. Information about student, course and course choosing can be modified.
2. Information about student, course and course choosing can be inserted and deleted.
3. Information about student and courses he/she chose can be queried based on a student’s ID or Name. If ID and Name are not given, show all students’ and their courses information. 
4. The score of a course that a student chose can be queried based on a student’s Name (or ID) and a course’s Name (or ID). If no student’s and course’s ID or Name are given, show all scores of all students’ courses. 
5. Information about course or course choosing can be queried based on course’s Name or ID. If no course’s Name or ID is given, show information about all courses or all course choosing. 
6. Information about teacher or courses a teacher teaches can be queried based on a teacher’s Name or ID. If no teacher’s Name or ID is given, show information about all teachers or all courses they teach. 
7. Average scores of a student, all students, students in the same class and a course can be queried. 

### Authorities 

1. A student can modify no information.
2. An administrator can modify information of students, courses and course choosing. But he/she can’t modify students’ score.
3. A teacher can modify students’ score.
Use any databases, such as DBMS SQL Server, Oracle, or DB2, 
Use any programming languages, such as java, c++, asp.net, php. Use c/s or b/s Model.


from studentvue import StudentVue
from getpass import getpass
import sqlite3
from flask import Flask
class User:
    def __init__ (self, username, userId, classes, teachers, grades):
        self.username = username
        self.userId = userId
        self.classes = classes
        self.teachers = teachers
        self.grades = grades

    def teacherComment (self, index, score, comment="$"):
        currTeacher = self.teachers[index]

        userIdArr = toArr(cursor.execute("SELECT commentID FROM teacherInfo WHERE name = ?", (currTeacher, )).fetchone()[0])
        if not self.userId in userIdArr:
            if userIdArr[0] == '': userIdArr = []
            userIdArr.append(self.userId)
            cursor.execute("UPDATE teacherInfo SET commentID = ? WHERE name = ?", (str(userIdArr), currTeacher))

            arr = toArr(cursor.execute("SELECT scores FROM teacherInfo WHERE name = ?", (currTeacher,)).fetchone()[0])
            if arr[0] == '': arr = []

            arr = [eval(i) for i in arr]
            arr.append(score)

            averageScore = sum(arr) / len(arr)
            cursor.execute("UPDATE teacherInfo SET scores = ? WHERE name = ?", (str(arr), currTeacher,))
            cursor.execute("UPDATE teacherInfo SET averageScore = ? WHERE name = ?", (averageScore, currTeacher,))
            connection.commit()

            commentArr = toArr(cursor.execute("SELECT comments FROM teacherInfo WHERE name = ?", (self.teachers[index], )).fetchone()[0])
            if commentArr[0] == '': commentArr = []
            commentArr.append(comment)
            cursor.execute("UPDATE teacherInfo SET comments = ? WHERE name = ?", (str(commentArr), self.teachers[index], ))

            connection.commit()

    def classComment (self, index, score, comment=""):
        currClass = self.classes[index]
        userIdArr = toArr(cursor.execute("SELECT commentID FROM classInfo WHERE name = ?", (currClass, )).fetchone()[0])
        if not self.userId in userIdArr:
            if userIdArr[0] == '': userIdArr = []
            userIdArr.append(self.userId)
            cursor.execute("UPDATE classInfo SET commentID = ? WHERE name = ?", (str(userIdArr), currClass))
            scoreArr = toArr(cursor.execute("SELECT scores FROM classInfo WHERE name = ?", (currClass, )).fetchone()[0])
            if scoreArr[0] == '': scoreArr = []

            scoreArr = [eval(i) for i in scoreArr]
            scoreArr.append(score)

            averageScore = sum(scoreArr) / len(scoreArr)
            cursor.execute("UPDATE classInfo SET scores = ? WHERE name = ?", (str(scoreArr), currClass,))
            cursor.execute("UPDATE classInfo SET averageScore = ? WHERE name = ?", (averageScore, currClass,))
            connection.commit()
            commentArr = toArr(cursor.execute("SELECT comments FROM classInfo WHERE name = ?", (currClass, )).fetchone()[0])
            if commentArr[0] == '': commentArr = []
            commentArr.append(comment)
            cursor.execute("UPDATE classInfo SET comments = ? WHERE name = ?",
                           (str(commentArr), currClass,))

            connection.commit()


def toString(arr, username):
    # this function returns a string formatted to add to the sqlite db
    string = "("
    string += ("'" + username + "', ")
    string += ("'" + arr[1] + "', ")
    string += ("'" + arr[2] + "', ")
    string += ("'" + arr[3] + "', ")
    string += (str(arr[4]) + ")")
    return string

def get_db_connection():
    conn = sqlite3.connect('example.db', check_same_thread=False)
    return conn

def toArr (s):
    return s.strip("][").replace("'", "").split(", ")

def addSchedule(username, password):
    sv = StudentVue(username, password, "https://md-mcps-psv.edupoint.com")
    gradebook = sv.get_gradebook()

    addedData = True
    cursor.execute("SELECT studentName FROM allInfo WHERE studentName = ?", (username,))
    data = cursor.fetchone()
    if data is None:
        addedData = False

    info = []

    for index, i in enumerate(gradebook["Gradebook"]["Courses"]["Course"]):
        info.append(
            [(index + 1), i["@Title"], i["@Staff"], i["@StaffEMail"], i["Marks"]["Mark"]["@CalculatedScoreRaw"]])
        instancesOfTeacher = cursor.execute("SELECT name FROM teacherInfo WHERE name = ?",
                                            (info[index][2],)).fetchall()
        instanceOfClass = cursor.execute("SELECT name FROM classInfo WHERE name = ?", (info[index][1], )).fetchall()

        if len(instanceOfClass) == 0:
            cursor.execute("INSERT INTO classInfo VALUES (?, ?, ?, ?, ?, ?)",
                           (info[index][1], info[index][2], -1, str([]), str([]), str([]), ))
        else:
            currTeacher = info[index][2]
            if not currTeacher in toArr(cursor.execute("SELECT classTeachers FROM classInfo WHERE name = ?", (info[index][1], )).fetchone()[0]):
                arr = toArr(cursor.execute("SELECT classTeachers FROM classInfo WHERE name = ?", (info[index][1], )).fetchone()[0])
                arr.append(currTeacher)
                cursor.execute("UPDATE classInfo SET classTeachers = ? WHERE name = ?", (str(arr), info[index][1]))



        if len(instancesOfTeacher) == 0:
            cursor.execute("INSERT INTO teacherInfo VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (info[index][2], info[index][3], -1 , str([info[index][1]]), str([]), str([]), str([]), ))
        else:
            #what this code does is check whether the teacher already has the same class added and if not adds it into the teacher info database
            currClass = i["@Title"]
            if not currClass in toArr(cursor.execute("SELECT teacherClasses FROM teacherInfo WHERE name = ?", (i["@Staff"], )).fetchone()[0]):
                arr = toArr(cursor.execute("SELECT teacherClasses FROM teacherInfo WHERE name = ?", (i["@Staff"], )).fetchone()[0])
                arr.append(currClass)
                cursor.execute("UPDATE teacherInfo SET teacherClasses = ? WHERE name = ?", (str(arr), i["@Staff"]))


    if not addedData:
        for index, i in enumerate(info):
            cursor.execute("INSERT INTO allInfo VALUES \n\t" + toString(i, username))
        connection.commit()

    connection.commit()

def createUser (username, password):
    print(password)
    sv = StudentVue(username, password, "https://md-mcps-psv.edupoint.com")
    studentInfo = sv.get_student_info()
    studentName = studentInfo["StudentInfo"]["FormattedName"]["$"]
    tupleTeacherList = cursor.execute("SELECT teacherName FROM allInfo WHERE studentName = ?", (username, )).fetchall()
    teachers = []
    for i in range(len(tupleTeacherList)):
        teachers.append(tupleTeacherList[i][0])
    tupleClassList = cursor.execute("SELECT className FROM allInfo WHERE studentName = ?", (username, )).fetchall()
    classes = []
    for i in range(len(tupleClassList)):
        classes.append(tupleClassList[i][0])
    tupleGradesList = cursor.execute("SELECT gradeInClass FROM allInfo WHERE studentName = ?", (username, )).fetchall()
    grades = []
    for i in range(len(tupleGradesList)):
        grades.append(tupleGradesList[i][0])
    addSchedule(username, password)
    return User(studentName, username, classes, teachers, grades)

# ****************************************************MAIN**********************************************************

connection = sqlite3.connect("example.db", check_same_thread=False)
cursor = connection.cursor()


app = Flask(__name__)


@app.route("/")
def helloworld ():
    return "hello world"

#ONE USE ---> Creates SQLITE DB TABLES
#cursor.execute("CREATE TABLE teacherInfo(name, email, averageScore, teacherClasses, comments, scores, commentID)")
#cursor.execute("CREATE TABLE allInfo(studentName, className, teacherName, teacherEmail, gradeInClass)")
#cursor.execute("CREATE TABLE classInfo(name, classTeachers, averageScore, comments, scores, commentID)")

#username = input("Enter username: ")
#password = getpass()

#addSchedule()
#currUser = createUser(username, password)
#WE SHOULD ONLY USE THE TEACHER COMMENT SO THAT THE SCORES AND COMMENTS STICK TOGETHER
#currUser.teacherComment(7, 10)
#currUser.classComment(0, 0, "bad bad class do not take")

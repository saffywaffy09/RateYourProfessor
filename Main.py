from studentvue import StudentVue
from getpass import getpass
import sqlite3


def toString(arr):
    # this function returns a string formatted to add to the sqlite db
    string = "("
    string += ("'" + username + "', ")
    string += ("'" + arr[1] + "', ")
    string += ("'" + arr[2] + "', ")
    string += ("'" + arr[3] + "', ")
    string += (str(arr[4]) + ")")
    return string

def toArr (s):
    return s.strip("][").replace("'", "").split(", ")

def addSchedule():
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
        instancesOfTeacher = cursor.execute("SELECT teacherName FROM teacherInfo WHERE teacherName = ?",
                                            (info[index][2],)).fetchall()
        if len(instancesOfTeacher) == 0:
            cursor.execute("INSERT INTO teacherInfo VALUES (?, ?, ?, ?, ?, ?)",
                           (info[index][2], info[index][3], -1 , str([info[index][1]]), str([]), str([])))
        else:
            #have to check whether the teacher has the class that we currently have and want to add
            #idk how to do this YET
            # check if the class that we had the teacher for, if the teacher has that class
            currClass = i["@Title"]
            if not currClass in toArr(cursor.execute("SELECT teacherClasses FROM teacherInfo WHERE teacherName = ?", (i["@Staff"], )).fetchone()[0]):
                arr = toArr(cursor.execute("SELECT teacherClasses FROM teacherInfo WHERE teacherName = ?", (i["@Staff"], )).fetchone()[0])
                arr.append(currClass)
                cursor.execute("UPDATE teacherInfo SET teacherClasses = ? WHERE teacherName = ?", (str(arr), i["@Staff"]))
            pass

    if not addedData:
        for index, i in enumerate(info):
            cursor.execute("INSERT INTO allInfo VALUES \n\t" + toString(i))
        connection.commit()


# ****************************************************MAIN**********************************************************

connection = sqlite3.connect("example.db")
cursor = connection.cursor()

#ONE USE ---> Creates SQLITE DB TABLES
#cursor.execute("CREATE TABLE teacherInfo(teacherName, teacherEmail, teacherScore, teacherClasses, indivComments, indivScore)")
#cursor.execute("CREATE TABLE allInfo(studentName, className, teacherName, teacherEmail, gradeInClass)")
#cursor.execute("CREATE TABLE classInfo(className, classTeachers, classScore, classComments, indivScore)")

username = input("Enter username: ")
password = getpass()

addSchedule()

# cursor.execute("CREATE TABLE ")


res = cursor.execute("SELECT teacherName FROM allInfo WHERE studentName = ?", (username,))

from studentvue import StudentVue
from getpass import getpass
import sqlite3

def toString(arr):
    #this function returns a string formatted to add to the sqlite db
    string = "("
    string += ("'" + username + "', ")
    string += ("'" + arr[1] + "', ")
    string += ("'" + arr[2] + "', ")
    string += ("'" + arr[3] + "', ")
    string += (str(arr[4]) + ")")
    return string



username = input("Enter username: ")
password = getpass()

connection = sqlite3.connect("example.db")
cursor = connection.cursor()

#this table has already been created
#cursor.execute("CREATE TABLE allInfo(studentName, className, teacherName, teacherEmail, gradeInClass)")

sv = StudentVue(username, password, "https://md-mcps-psv.edupoint.com")
gradebook = sv.get_gradebook()

info = []
for index, i in enumerate(gradebook["Gradebook"]["Courses"]["Course"]):
    info.append([(index+1), i["@Title"], i["@Staff"], i["@StaffEMail"], i["Marks"]["Mark"]["@CalculatedScoreRaw"]])

for index, i in enumerate(info):
    cursor.execute("INSERT INTO allInfo VALUES \n\t" + toString(i))

connection.commit()

res = cursor.execute("SELECT className FROM allInfo")
print(res.fetchall())
from studentvue import StudentVue
from getpass import getpass


username = input("Enter username: ")
password = getpass()


# for right now this only works for mcps
sv = StudentVue(username, password, "https://md-mcps-psv.edupoint.com")
gradebook = sv.get_gradebook()



schedule = sv.get_schedule(1)
if "RT_ERROR" in schedule.keys():
    print("bad credentials")
studentClassSchedule = schedule['StudentClassSchedule']
classLists = studentClassSchedule['ClassLists']
classListing = classLists['ClassListing']

for i in classListing:
    print(i["@CourseTitle"])

print()



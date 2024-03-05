from studentvue import StudentVue
username = input("Enter username: ")
password = input("Enter password: ")
# for right now this only works for mcps
sv = StudentVue(username, password, "https://md-mcps-psv.edupoint.com")
firstQuarter = sv.get_gradebook(1)
secondQuarter = sv.get_gradebook(3)
thirdQuarter = sv.get_gradebook(5)
fourthQuarter = sv.get_gradebook(7)

print("FIRST SEMESTER")
for i in firstQuarter["Gradebook"]["Courses"]["Course"]:
    print(f"{i["@Title"]} taught by Professor {i["@Staff"]} ({i["@StaffEMail"]})")
print("----------------------------------------")
print("SECOND SEMESTER")
for i in secondQuarter["Gradebook"]["Courses"]["Course"]:
    print(f"{i["@Title"]} taught by Professor {i["@Staff"]} ({i["@StaffEMail"]})")


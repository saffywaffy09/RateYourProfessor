from studentvue import StudentVue
username = input("Enter username: ")
password = input("Enter password: ")
# for right now this only works for mcps
sv = StudentVue(username, password, "https://md-mcps-psv.edupoint.com")
gradebook = sv.get_gradebook()

for i in gradebook["Gradebook"]["Courses"]["Course"]:
    print(i["@Title"], "taught by", i["@Staff"])
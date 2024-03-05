from studentvue import StudentVue
sv = StudentVue("172834", "not my real password", "https://md-mcps-psv.edupoint.com")
gradebook = sv.get_gradebook()
print(gradebook["Gradebook"]["Courses"]["Course"])
for i in gradebook["Gradebook"]["Courses"]["Course"]:
    print(i["@Title"])


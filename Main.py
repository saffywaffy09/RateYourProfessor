from studentvue import StudentVue
gradebook = sv.get_gradebook()
print(gradebook["Gradebook"]["Courses"]["Course"])
for i in gradebook["Gradebook"]["Courses"]["Course"]:
    print(i["@Title"])


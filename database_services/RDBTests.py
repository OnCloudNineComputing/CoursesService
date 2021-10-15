from database_services.RDBService import RDBService


def test_1():

    res = RDBService.get_by_prefix(
        "cloud_computing_f21", "courses", "course_name", "Cloud Computing"
    )
    print("Test 1 result = ", res)


def test_2():

    res = RDBService.find_by_template(
        "cloud_computing_f21", "courses", {"course_name": "Cloud Computing"}, None
    )
    print("Test 2 result = ", res)


def test_3():

    res = RDBService.create(
        "cloud_computing_f21", "courses",
        {
            "course_name": "Artificial Intelligence",
            "course_year": 2021,
            "course_sem": "Fall",
            "dept": "COMS",
            "course_number": "W4701",
            "section": "002",
            "credits": 3,
            "call_number": 13267,
            "professors": "Ansaf Salleb-Aouissi",
            "TAs": "Rohith Ravindranath, Tom Cohen, Adam Lin, Justin Ghaeli, Ariel Goldman, Joseph Brew, Caitlyn Chen, Nicholas Lillis, Michael Winitch, Elyas Obbad, Gustave Ducrest, Joe Redmond, Chandan Suri, Sanya Mehta, Akhil Konda, Andrea Clark Sevilla, Keshaw Singh, Evan Zauderer, Pierre Rodgers",
            "course_days": "TR",
            "start_time": "11:40:00",
            "end_time": "12:55:00",
            "location": "CIN Alfred Lerner Hall",
            "enrollment": 153
        })

    print("Test 3 result = ", res)


test_2()



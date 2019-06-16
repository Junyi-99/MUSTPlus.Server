from django.http import HttpResponse

from services.basic.models import Department, Faculty

FACULTIES = {
    '資訊科技學院': 'Faculty of Information Technology',
    '商學院': 'School of Business',
    '法學院': 'Faculty of Law',
    '中醫藥學院': 'Faculty of Chinese Medicine',
    '酒店與旅遊管理學院': 'Faculty of Hospitality and Tourism Management',
    '人文藝術學院': 'Faculty of Humanities and Arts',
    '醫學院': 'Faculty of Medicine',
    '國際學院': 'University International College',
    '藥學院': 'School of Pharmacy',
    '研究生院': 'School of Graduate Studies',
    '通識教育部': 'Department of General Education',
    '持續教育學院': 'School of Continuing Studies',
    '健康科學學院': 'Faculty of Health Sciences',
}

DEPARTMENTS = {
    '學生事務處': 'student Affairs Office',
    '教務處': 'Academic Affairs Office',
    '註冊處': 'Registry',
    '校長室': "Rector's Office",
    '會計處': 'Accounts Office',
    '總務處': 'General Affairs Office',
    '人事處': 'Personnel Office',
    '求職訊息': 'Unknown Name',
    '學術研究處': 'Unknown Name',
    '資訊處': 'Information Technology Office',
    '圖書出版及供應中心': 'Unknown Name',
    '物業及設施管理處': 'Estates and Facilities Management Office',
    '可持續發展研究所': 'The Institute for Sustainable Development',
    '圖書館': 'Library',
    '教育發展中心': 'Educational Development Centre',
    '科研管理處': 'Research and Technology Administration Office',
    '招生處': 'Admission Office',
    '創業就業發展中心': 'Centre for Entrepreneurship and Career Planning',
    '教學質量督導處': 'Quality Assurance Office',
    '人力資源處': 'Human Resources Office',
}


# 初始化 faculty 表的 value
def init_faculties(request):
    print("Initializing faculties")
    for key, value in FACULTIES.items():
        faculty = Faculty(name_zh=key, name_en=value)
        faculty.save()
    print("Done!")
    return HttpResponse("")


def init_departments(request):
    print("Initializing Departments")
    for key, value in DEPARTMENTS.items():
        department = Department(name_zh=key, name_en=value)
        department.save()
    print("Done!")
    return HttpResponse("")

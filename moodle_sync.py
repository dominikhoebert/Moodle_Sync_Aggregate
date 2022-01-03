import moodle_api
import pandas as pd

"""
[SSL: CERTIFICATE_VERIFY_FAILED] Error: https://stackoverflow.com/questions/51925384/unable-to-get-local-issuer-certificate-when-using-requests-in-python
Install certifi; copy cacert.pem aus certifi folder
"""


class MoodleSync:
    def __init__(self, url: str, key: str):
        moodle_api.URL = url
        moodle_api.KEY = key

    def get_recent_courses(self):
        response = moodle_api.call('core_course_get_recent_courses')
        return {c['fullname']: {'id': c['id']} for c in response}

    def get_course_modules(self, course_id):
        response = moodle_api.call('core_course_get_contents', courseid=course_id)
        modules = {}
        for section in response:
            for module in section['modules']:
                if 'modname' in module:
                    if module['modname'] == 'assign':
                        modules[module['name']] = {'id': module['id']}
        return modules

    def get_students_of_module(self, module_id):
        response = moodle_api.call('mod_assign_list_participants', assignid=module_id, groupid=3, filter="")
        print(response)

    def get_gradereport_of_course(self, course_id):
        response = moodle_api.call('gradereport_user_get_grade_items', courseid=course_id)
        graditems = {}
        for graditem in response['usergrades'][0]['gradeitems']:
            graditems[graditem['itemname']] = graditem['id']

        df = pd.DataFrame(columns=['userfullname'] + list(graditems.keys()))

        for student in response['usergrades']:
            grades = {'userfullname': student['userfullname']}
            for gradeitem in student['gradeitems']:
                grades[gradeitem['itemname']] = gradeitem['gradeformatted']
            df = df.append(grades, ignore_index=True)

        df = df.rename(columns={None: 'Kurs', 'userfullname': 'Schüler'})
        return df


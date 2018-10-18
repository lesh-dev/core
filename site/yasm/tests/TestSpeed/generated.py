import unittest
import timeit
import sys
import json
import instance
import instance.login.controllers
from flask_login import login_user
from instance.api.generated import notification_list
from instance.api.generated import department_list
from instance.api.generated import person_list
from instance.api.generated import contact_list
from instance.api.generated import school_list
from instance.api.generated import course_list
from instance.api.generated import course_teachers_list
from instance.api.generated import exam_list
from instance.api.generated import person_school_list
from instance.api.generated import person_comment_list
from instance.api.generated import submission_list
from instance.api.generated import contestants_list
from instance.api.generated import problems_list
from instance.api.generated import solutions_list
yasm = instance.create()

class TestSpeed(unittest.TestCase):
    @classmethod
    def test_notification_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(notification_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_department_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(department_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_person_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(person_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_contact_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(contact_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_school_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(school_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_course_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(course_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_course_teachers_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(course_teachers_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_exam_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(exam_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_person_school_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(person_school_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_person_comment_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(person_comment_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_submission_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(submission_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_contestants_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(contestants_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_problems_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(problems_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()

    @classmethod
    def test_solutions_list(cls):
        with yasm.test_request_context():
            login_user(user=instance.login.controllers.load_user(467))
            time = timeit.timeit(solutions_list, number=10)
            test_case = sys._getframe().f_code.co_name
            results_file = open("results")
            results = json.load(results_file)
            results_file.close()
            if test_case in results.keys():
                assert results[test_case] * 1.1 > time
                if time < results[test_case]:
                    results[test_case] = time
            else:
                results[test_case] = time
            results_file = open("results", "w")
            results_file.write(json.dumps(results, indent=4, sort_keys=True))
            results_file.close()


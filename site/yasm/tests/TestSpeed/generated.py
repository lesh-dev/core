import unittest
import timeit
import sys
import json
import instance
import instance.login.controllers
from flask_login import login_user
import tests.testinglib as testinglib
from instance.api.generated import notification_list
from instance.api.generated import department_list
from instance.api.generated import person_list
from instance.api.generated import direct_login_list
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
    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_notification_list(self):
        time = timeit.timeit(notification_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_department_list(self):
        time = timeit.timeit(department_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_person_list(self):
        time = timeit.timeit(person_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_direct_login_list(self):
        time = timeit.timeit(direct_login_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_contact_list(self):
        time = timeit.timeit(contact_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_school_list(self):
        time = timeit.timeit(school_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_course_list(self):
        time = timeit.timeit(course_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_course_teachers_list(self):
        time = timeit.timeit(course_teachers_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_exam_list(self):
        time = timeit.timeit(exam_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_person_school_list(self):
        time = timeit.timeit(person_school_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_person_comment_list(self):
        time = timeit.timeit(person_comment_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_submission_list(self):
        time = timeit.timeit(submission_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_contestants_list(self):
        time = timeit.timeit(contestants_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_problems_list(self):
        time = timeit.timeit(problems_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

    @testinglib.load_result
    @testinglib.request_needed(yasm)
    @testinglib.login_needed(467)
    def test_solutions_list(self):
        time = timeit.timeit(solutions_list, number=10) / 10
        if testinglib.result.get():
            assert testinglib.result.get() * 1.1 > time
            if time < testinglib.result.get():
                testinglib.result.set(time)
        else:
            testinglib.result.set(time)

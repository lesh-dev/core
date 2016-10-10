# coding: utf-8

"""
    Here we (re)implement basic XSM entities in Python
    with generic testing abilities, as vstarodub@ done
    with Effi-based entities in ASoft.

    Achtung: PEP8 grammar_nazi is here. Do not use
    lowerCamelCase, CamelCase, etc.
"""

import random_crap as rc


class Person(object):
    """
        Иван Человеков был простой человек
        И просто смотрел на свет
        И "Да" его было настоящее "Да",
        А "Нет" -- настоящее "Нет"!

                    И. Кормильцев, В. Бутусов
    """
    # Parent test object
    xtest = None
    # Properties
    first_name = None
    last_name = None
    patronymic = None

    def __init__(self, xtest, first_name=None, last_name=None, patronymic=None, random=True):
        self.xtest = xtest

        self.last_name = last_name if last_name else u"Человеков"
        self.first_name = first_name if first_name else u"Иван"
        self.patronymic = patronymic if patronymic else u"Бутусович"

        if random:
            self.last_name += "_" + rc.random_text(5)
            self.first_name += "_" + rc.random_text(3)
            self.patronymic += "_" + rc.random_text(3)

    def input(self, is_student=False, is_teacher=False):
        # FIXME(mvel) non-static crap... f*n SOLYD programming :(
        self.last_name = self.xtest.fillElementById("last_name-input", self.last_name)
        self.first_name = self.xtest.fillElementById("first_name-input", self.first_name)
        self.patronymic = self.xtest.fillElementById("patronymic-input", self.patronymic)

        if is_student:
            self.xtest.clickElementById("is_student-checkbox")

        self.xtest.clickElementById("update-person-submit")

    def back_to_person_view(self):
        # FIXME(mvel) this is a Person control
        self.xtest.gotoBackToPersonView()
        full_alias = self.full_alias()
        # check if person alias is present (person saved correctly)
        self.xtest.checkPersonAliasInPersonView(full_alias)

    def full_alias(self):
        full_alias = self.last_name + " " + self.first_name + " " + self.patronymic
        return full_alias.strip()

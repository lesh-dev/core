#!/usr/bin/python
# -*- coding: utf8 -*-

import logging

import xsm
import xtest_common
import random_crap
import bawlib


class XcmsXsmAnketaTeacherFill(xsm.Manager, xtest_common.XcmsTest):
    """
    This test checks teacher anketa add functional and following person processing steps.
    It does following:
    * navigates to teacher anketa form
    * fill anketa with all correct values
    * submits form
    * login as admin (root)
    * navigates to anketa list
    * clicks on new anketa
    * checks if all entered data match screen form.
    * adds 3 comments to this new person
    * edits 2 of 3 comments
    * changes person status incrementally
    """

    def add_and_check_person_comment(self, person):
        comment_text = person.add_comment()
        logging.info("Added comment %s", comment_text)
        self.assertBodyTextPresent(comment_text)
        return comment_text

    def add_comments_to_person(self, person):
        self.add_and_check_person_comment(person)
        comment_text_2 = self.add_and_check_person_comment(person)
        self.add_and_check_person_comment(person)

        # and now let's edit one of them.
        self.gotoIndexedUrlByLinkText(u"Правка", 0)
        self.gotoBackAfterComment()

        self.gotoIndexedUrlByLinkText(u"Правка", 1)
        self.gotoBackAfterComment()

        # oh, no! we want to use comment link ids!
        comment_text_new_1 = self.editCommentToPerson("comment-edit-1")
        self.assertBodyTextPresent(comment_text_new_1)

        comment_text_new_3 = self.editCommentToPerson("comment-edit-3")
        self.assertBodyTextPresent(comment_text_new_3)

        # check if all new comments are present here, and 2-nd comment left unchanged
        self.assertBodyTextPresent(comment_text_new_1, "Comment 1 must change value. ")
        self.assertBodyTextPresent(comment_text_2, "Comment should remain unchanged. ")
        self.assertBodyTextPresent(comment_text_new_3, "Comment 3 must change value. ")

    def run(self):
        self.ensure_logged_off()

        # anketa fill positive test:
        # all fields are filled with correct values.
        self.gotoRoot()
        self.goto_anketa_teacher()

        person = xsm.Person(self)
        person.input(
            last_name=u"Учитель",
            first_name=u"Алексей",
            patronymic=u"Иваныч",
            birth_date=random_crap.date(),
            school=u"Тестовый ВУЗ им. В.Е.Бдрайвера №",
            ank_class=random_crap.randomDigits(1) + u" курс",
            cellular="+7" + random_crap.randomDigits(9),
            email=random_crap.random_text(10) + "@" + random_crap.random_text(6) + ".ru",
            social_profile=random_crap.randomVkontakte(),
            # favourites=random_crap.randomCrap(20, ["multiline"]),
            # achievements=random_crap.randomCrap(15, ["multiline"]),
            # hobby=random_crap.randomCrap(10, ["multiline"]),
            # lesh_ref=random_crap.randomCrap(10, ["multiline"]),
            control_question=u"пять",
            ank_mode=True,
            random=True,
        )
        self.assertBodyTextPresent(self.get_anketa_success_submit_message())
        inp_social_show = bawlib.cut_http(person.social_profile)

        self.anketa_drilldown(person)

        full_alias = person.full_alias()
        # just check text is on the page.
        logging.info("Checking that all filled fields are displayed on the page")

        self.checkPersonAliasInPersonView(full_alias)

        # TODO(mvel): Extract common checks to module
        self.assertBodyTextPresent(person.birth_date)
        self.assertBodyTextPresent(person.school)
        self.assertBodyTextPresent(person.ank_class)
        self.assertBodyTextPresent(person.cellular)
        self.assertBodyTextPresent(person.email)
        self.assertBodyTextPresent(inp_social_show)
        """
        self.clickElementById("show-extra-person-info")
        self.wait(1)
        self.assertElementSubTextById("extra-person-info", person.favourites)
        self.assertElementSubTextById("extra-person-info", person.achievements)
        self.assertElementSubTextById("extra-person-info", person.hobby)
        self.assertElementSubTextById("extra-person-info", person.lesh_ref)
        """

        self.add_comments_to_person(person)

        # now, let's change anketa status to "Ждет собеседования"

        self.gotoEditPerson()

        # first, check that values in opened form match entered in anketa.
        self.assertElementValueById("last_name-input", person.last_name)
        self.assertElementValueById("first_name-input", person.first_name)
        self.assertElementValueById("patronymic-input", person.patronymic)
        self.assertElementValueById("birth_date-input", person.birth_date)
        self.assertElementValueById("school-input", person.school)
        self.assertElementValueById("ank_class-input", person.ank_class)
        # current_class should now be equal to ank_class (fresh anketa)
        self.assertElementValueById("current_class-input", person.ank_class)
        self.assertElementValueById("cellular-input", person.cellular)
        self.assertElementValueById("email-input", person.email)
        self.assertElementValueById("social_profile-input", person.social_profile)
        # self.assertElementValueById("favourites-text", person.favourites)
        # self.assertElementValueById("achievements-text", person.achievements)
        # self.assertElementValueById("hobby-text", person.hobby)
        # self.assertElementValueById("lesh_ref-text", person.lesh_ref)

        self.assertElementValueById("anketa_status-selector", "new")

        # change anketa status and save it.
        self.setOptionValueByIdAndValue("anketa_status-selector", "progress")

        self.clickElementById("update-person-submit")

        self.assertBodyTextPresent(u"Участник успешно сохранён")
        self.goto_back_to_anketa_view()

        self.assertElementTextById("anketa_status-span", u"Ждёт собес.")

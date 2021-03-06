#!/usr/bin/python
# -*- coding: utf8 -*-

import xtest_common
import random_crap
import xpage

import datetime


def timestamp():
    return datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")


def htmlParagraph(x):
    return "<p>" + x + "</p>"


def linesToHtml(lineArray):
    return "\n".join([htmlParagraph(x) for x in lineArray])


class XcmsContentAddPage(xtest_common.XcmsTest):
    """
    This test checks content editing - page add/edit functional.
    It does following steps:
    * login as root user (in future - site editor)
    * add new subpage
    * edit new subpage some times
    * load previous version
    * sets and changes page alias
    * tests diff engine
    """

    def run(self):
        self.ensure_logged_off()

        # avoid spontaneous HTML tags
        self.specChars = random_crap.specialCharsWoAngle  # without <>
        # here was spike for old version of Chrome - to enter only English words.
        self.wordOptions = []

        self.testBaseEditing()

        self.testVersions()

        self.testDiffAndLongText()

        self.testAlias()
        self.testBadAlias()

    def testBaseEditing(self):

        self.perform_login_as_admin()
        self.gotoAdminPanel()

        self.m_parentPage = u"Главная"

        self.gotoUrlByLinkText(self.m_parentPage)
        self.gotoCreatePage()

        page = xpage.Page(self)
        page.input(
            page_dir="test_page",
            menu_title="menu_title",
            header="page_header",
            alias="new/page/alias/",
            random=True,
        )
        self.page = page

        # edit page - click on menu
        self.gotoUrlByLinkText(page.menu_title)

        page_text = random_crap.randomCrap(10, self.wordOptions, specialChars=self.specChars) + " " + timestamp()
        print "Generated page text: '" + page_text + "'"

        page_text = self.fillAceEditorElement(page_text)
        print "After ins page text: '" + page_text + "'"
        self.clickElementById("commit-submit")

        self.clickElementById("preview-submit")

        preview_element = "content-text-preview"
        self.assertElementTextById(preview_element, page_text, "preview text does not match entered page text. ")

        # add second line
        new_page_text = (
            page_text + "\n" +
            random_crap.randomCrap(10, self.wordOptions, specialChars=self.specChars) + " " + timestamp()
        )

        new_page_text = self.fillAceEditorElement(new_page_text)
        print "Generated 2-line page text: '" + new_page_text + "'"

        self.clickElementById("commit-submit")
        self.clickElementById("preview-submit")

        new_page_text_for_check = (
            new_page_text
            .replace("\n", " ")
            .replace("  ", " ")
            .replace(">>", u"»")
            .replace("<<", u"«")
            .strip()
        )

        self.assertElementTextById(
            preview_element, new_page_text_for_check,
            "preview text on text change does not match entered text. "
        )

        self.gotoCloseEditor()

        self.getElementById("cabinet")

        # click on menu.
        self.logAdd("Clicking on parent menu item. ")
        self.gotoUrlByLinkText(self.m_parentPage, attribute=self.CONTENT)
        self.logAdd("Clicking on new page menu item. ")
        self.gotoUrlByLinkText(page.menu_title, attribute=self.CONTENT)

        self.assertElementTextById(
            "content-text",
            new_page_text_for_check,
            "page text after reopening editor does not match entered text. "
        )
        self.assert_page_header(page.header, reason="Page header does not match entered header. ")

    def loadWait(self):
        self.wait(2, "wait for version load")

    def testVersions(self):

        self.gotoUrlByLinkText(self.m_parentPage, attribute=self.CONTENT)
        self.gotoUrlByLinkText(self.page.menu_title, attribute=self.CONTENT)

        self.gotoEditPageInPlace()

        self.logAdd("Waiting before saving of first version. ")
        timeToWait = 105
        self.wait(timeToWait)

        versionUnoText = "version_0001" + "\n" + timestamp()
        versionUnoText = self.fillAceEditorElement(versionUnoText)
        self.clickElementById("commit-submit")
        self.wait(timeToWait, "waiting after version 1")

        versionDosText = "version_0002" + "\n" + timestamp()
        versionDosText = self.fillAceEditorElement(versionDosText)
        self.clickElementById("commit-submit")
        self.wait(timeToWait, "waiting after version 2")

        versionTresText = "version_0003" + "\n" + timestamp()
        versionTresText = self.fillAceEditorElement(versionTresText)
        self.clickElementById("commit-submit")
        self.wait(timeToWait, "waiting after version 3")

        self.setOptionValueByIdAndIndex("versions-select", 3)
        self.clickElementById("set_version-submit")  # Смотреть версию
        self.loadWait()
        self.assertAceEditorElementText(versionUnoText)

        self.setOptionValueByIdAndIndex("versions-select", 1)
        self.clickElementById("set_version-submit")  # Смотреть версию
        self.loadWait()
        self.assertAceEditorElementText(versionTresText)

        self.setOptionValueByIdAndIndex("versions-select", 2)
        self.clickElementById("set_version-submit")  # Смотреть версию
        self.loadWait()
        self.assertAceEditorElementText(versionDosText)

        self.wait(timeToWait, "Waiting for next test step. ")

        versionLostText = "version_lost" + "\n" + timestamp()
        versionLostText = self.fillAceEditorElement(versionLostText)
        self.clickElementById("commit-submit")
        #
        self.wait(10, "Waiting some small time (less than version interval)")

        versionDoNotLostText = "version_do_not_lost" + "\n" + timestamp()
        versionDoNotLostText = self.fillAceEditorElement(versionDoNotLostText)
        self.clickElementById("commit-submit")

        self.setOptionValueByIdAndIndex("versions-select", 2)
        self.clickElementById("set_version-submit")  # Смотреть версию
        self.loadWait()
        self.assertAceEditorElementText(versionTresText, "Here should be version 3, not lost version 4. ")

        # finally, check head revision
        self.setOptionValueByIdAndIndex("versions-select", 1)
        self.clickElementById("set_version-submit")  # Смотреть версию
        self.loadWait()
        self.assertAceEditorElementText(versionDoNotLostText)

        self.gotoCloseEditor()

    def testDiffAndLongText(self):

        self.logAdd("test diff engine. ")
        self.wait(2)

        self.gotoUrlByLinkText(self.m_parentPage, attribute=self.CONTENT)
        self.gotoUrlByLinkText(self.page.menu_title, attribute=self.CONTENT)
        self.gotoEditPageInPlace()

        wordNumber = 7
        totalLines = 8

        origLines = [
            random_crap.randomCrap(wordNumber, self.wordOptions, specialChars=self.specChars)
            for _ in xrange(0, totalLines)
        ]

        pageText = linesToHtml(origLines)

        pageText = self.fillAceEditorElement(pageText)

        print "diff test page text original: "
        print pageText
        print "-" * 30

        self.clickElementById("commit-submit")

        # insert one line
        insLine = random_crap.randomCrap(wordNumber, self.wordOptions, specialChars=self.specChars)

        # remove some lines inside
        newLines = origLines[:3] + [insLine] + origLines[3:5] + origLines[7:]
        pageText = linesToHtml(newLines)

        pageText = self.fillAceEditorElement(pageText)

        print "diff test page new text: "
        print pageText
        print "-" * 30

        self.clickElementById("commit-submit")

        # cut last line
        newLines = newLines[:-1]

        pageText = linesToHtml(newLines)

        pageText = self.fillAceEditorElement(pageText)
        self.clickElementById("commit-submit")

        pageWords = (" ".join(newLines)).split()

        print "word count ", len(pageWords)

        sampleWords = pageWords[5:9] + pageWords[24:27] + pageWords[30:32]
        for sample in sampleWords:
            print "replacing word: ", sample
            replacement = random_crap.randomCrap(4, self.wordOptions, specialChars=self.specChars)
            print "replacement: ", replacement
            pageText = pageText.replace(sample, replacement)

        self.logAdd("diff test page new text after word-replacement: ")
        self.logAdd(pageText)
        self.logAdd("-" * 30)

        pageText = self.fillAceEditorElement(pageText)

        self.clickElementById("commit-submit")

        self.gotoCloseEditor()

        realPageText = (
            pageText
            .replace("<p>", "")
            .replace("\n", " ")
            .replace("</p> ", "\n")
            .replace("</p>", "\n")
            .strip()
        )

        self.logAdd("real page text: ")
        self.logAdd(realPageText)
        self.logAdd("-" * 30)

        self.assertElementTextById("content-text", realPageText, "real page text does not match entered text. ")

    def updateAliases(self, expected_state=u"Список alias-ов успешно обновлён"):
        self.clickElementByName("change_alias")
        self.assertBodyTextPresent(expected_state)

    def testAlias(self):

        self.getElementById("cabinet")

        self.gotoUrlByLinkText(self.m_parentPage, attribute=self.CONTENT)
        self.gotoUrlByLinkText(self.page.menu_title, attribute=self.CONTENT)
        self.gotoEditPageInPlace()

        # edit alias
        self.gotoUrlByLinkText(self.page.alias)
        self.page.input_alias("changed/newpage/alias/" + random_crap.random_text(8))
        self.updateAliases()
        self.wait(3, "wait for redirection")

        self.goto_alias(self.page.alias)
        self.assert_page_header(self.page.header, reason="Page header does not match entered header. ")

    def testBadAlias(self):

        self.logAdd("test bad aliases")
        self.gotoEditPageInPlace()

        self.gotoUrlByLinkText(self.page.alias)
        self.page.input_alias("../root/alias~")
        self.updateAliases(expected_state=u"Alias может содержать только символы")

        self.page.input_alias("/good/alias/" + random_crap.random_text(6))
        self.updateAliases()
        self.wait(3, "wait for redirection after fixing alias")

        self.gotoCloseEditor()

        self.gotoAdminPanel()
        self.gotoCreatePage(
            reason="We should successfully enter admin panel, but we cannot see button to create new subpage. "
        )
